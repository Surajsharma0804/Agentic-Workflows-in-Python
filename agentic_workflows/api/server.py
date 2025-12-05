"""FastAPI server for Agentic Workflows."""
import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
import structlog
import time
from pathlib import Path

from ..config import get_settings
from ..core.exceptions import AgenticWorkflowsError

# Import routes with error handling
try:
    from .routes import workflows, tasks, plugins, health, auth, llm, audit
    ROUTES_AVAILABLE = True
except Exception as e:
    import sys
    print(f"WARNING: Failed to import routes: {e}", file=sys.stderr)
    ROUTES_AVAILABLE = False
    # Create minimal health router as fallback
    from fastapi import APIRouter
    health = type('obj', (object,), {'router': APIRouter()})()
    @health.router.get("/health")
    async def health_check():
        return {"status": "healthy", "note": "minimal mode"}

logger = structlog.get_logger()
settings = get_settings()


async def init_database_async():
    """Initialize database asynchronously (non-blocking)."""
    import asyncio
    max_retries = 3
    for attempt in range(max_retries):
        try:
            from ..db.database import init_db, get_engine
            from ..db.models import Base
            logger.info("initializing_database_tables", attempt=attempt + 1)
            # Initialize tables (lazy engine creation)
            await asyncio.to_thread(init_db)
            logger.info("database_initialized_successfully")
            break
        except Exception as e:
            if attempt < max_retries - 1:
                logger.warning("database_init_retry", attempt=attempt + 1, error=str(e))
                await asyncio.sleep(1)
            else:
                logger.warning("database_initialization_skipped", error=str(e), note="App will work without database")
                # Continue anyway - app will work without DB for health checks


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Enterprise-grade agentic workflow automation platform",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )
    
    # Middleware (order matters - SessionMiddleware must be added before others)
    # Add SessionMiddleware for OAuth support
    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.secret_key,
        session_cookie="agentic_session",
        max_age=3600,  # 1 hour
        same_site="lax",
        https_only=settings.environment == "production"
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    # Request logging middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        
        logger.info(
            "request_started",
            method=request.method,
            path=request.url.path,
            client=request.client.host if request.client else None
        )
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        logger.info(
            "request_completed",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            process_time=f"{process_time:.3f}s"
        )
        
        response.headers["X-Process-Time"] = str(process_time)
        return response
    
    # Exception handlers
    @app.exception_handler(AgenticWorkflowsError)
    async def agentic_workflows_exception_handler(request: Request, exc: AgenticWorkflowsError):
        logger.error(
            "agentic_workflows_error",
            error=exc.error_code,
            message=exc.message,
            details=exc.details
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=exc.to_dict()
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.error("validation_error", errors=exc.errors())
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"error": "ValidationError", "details": exc.errors()}
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error("unhandled_exception", error=str(exc), exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "InternalServerError",
                "message": "An unexpected error occurred"
            }
        )
    
    # Include API routers FIRST (before static files and catch-all)
    app.include_router(health.router, prefix="/api", tags=["Health"])
    
    if ROUTES_AVAILABLE:
        try:
            app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
            app.include_router(workflows.router, prefix="/api/workflows", tags=["Workflows"])
            app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
            app.include_router(plugins.router, prefix="/api/plugins", tags=["Plugins"])
            app.include_router(llm.router, prefix="/api/llm", tags=["AI & LLM"])
            app.include_router(audit.router, prefix="/api/audit", tags=["Audit Logs"])
            logger.info("all_routes_loaded_successfully")
        except Exception as e:
            logger.warning("some_routes_failed_to_load", error=str(e))
    else:
        logger.warning("routes_not_available", note="Running in minimal mode")
    
    # Debug endpoint to check filesystem
    @app.get("/api/debug/filesystem")
    async def debug_filesystem():
        """Debug endpoint to check filesystem structure."""
        import os
        ui_dist_path = Path(__file__).parent.parent.parent / "ui" / "dist"
        app_root = Path(__file__).parent.parent.parent
        
        return {
            "app_root": str(app_root.absolute()),
            "ui_dist_path": str(ui_dist_path.absolute()),
            "ui_dist_exists": ui_dist_path.exists(),
            "ui_dist_contents": [f.name for f in ui_dist_path.iterdir()] if ui_dist_path.exists() else [],
            "cwd": os.getcwd(),
            "file_location": str(Path(__file__).absolute())
        }
    
    # Serve React frontend (if built)
    ui_dist_path = Path(__file__).parent.parent.parent / "ui" / "dist"
    logger.info("checking_frontend_path", 
                path=str(ui_dist_path), 
                exists=ui_dist_path.exists(),
                absolute_path=str(ui_dist_path.absolute()))
    
    # Check if frontend is built
    frontend_available = ui_dist_path.exists() and (ui_dist_path / "index.html").exists()
    
    if frontend_available:
        # List contents for debugging
        try:
            contents = list(ui_dist_path.iterdir())
            logger.info("serving_react_frontend", 
                       path=str(ui_dist_path),
                       files=[f.name for f in contents])
        except Exception as e:
            logger.error("error_listing_frontend", error=str(e))
        
        # Mount static assets
        assets_path = ui_dist_path / "assets"
        if assets_path.exists():
            app.mount("/assets", StaticFiles(directory=str(assets_path)), name="assets")
            logger.info("mounted_assets", path=str(assets_path))
        
        # Serve static files from ui/dist
        @app.get("/manifest.json")
        async def manifest():
            return FileResponse(ui_dist_path / "manifest.json")
        
        @app.get("/robots.txt")
        async def robots():
            return FileResponse(ui_dist_path / "robots.txt")
        
        @app.get("/sw.js")
        async def service_worker():
            return FileResponse(ui_dist_path / "sw.js")
        
        # Root path - serve index.html
        @app.get("/")
        async def root():
            """Serve React app root."""
            return FileResponse(ui_dist_path / "index.html")
    else:
        logger.warning("react_frontend_not_found", path=str(ui_dist_path))
        # Fallback root endpoint if UI not built
        @app.get("/")
        async def root():
            """Root endpoint - API info."""
            return {
                "status": "ok",
                "message": "Agentic Workflows API",
                "health": "/api/health",
                "docs": "/api/docs",
                "note": "Frontend UI not built"
            }
    
    # Custom 404 handler for SPA routing (registered at app level, not conditionally)
    @app.exception_handler(404)
    async def custom_404_handler(request: Request, exc):
        """Handle 404s by serving React app for non-API routes."""
        # If it's an API route, return JSON 404
        if request.url.path.startswith("/api"):
            return JSONResponse(
                status_code=404,
                content={"error": "Not Found", "path": request.url.path}
            )
        
        # For frontend routes, serve index.html if available
        if frontend_available:
            return FileResponse(ui_dist_path / "index.html")
        
        # Otherwise return JSON 404
        return JSONResponse(
            status_code=404,
            content={"error": "Not Found", "path": request.url.path}
        )
    
    @app.on_event("startup")
    async def startup_event():
        logger.info("application_starting", version=settings.app_version, port=settings.api_port)
        logger.info("startup_complete", message="App ready to accept requests")
        
        # Skip database init for now - will initialize on first request
        # import asyncio
        # asyncio.create_task(init_database_async())
    
    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("application_shutting_down")
    
    return app


app = create_app()


def main():
    """Run the FastAPI server."""
    uvicorn.run(
        "agentic_workflows.api.server:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
        workers=settings.api_workers if not settings.api_reload else 1,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    main()
