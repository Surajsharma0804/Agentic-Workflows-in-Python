"""FastAPI server for Agentic Workflows."""
import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
import structlog
import time
from pathlib import Path

from ..config import get_settings
from ..core.exceptions import AgenticWorkflowsError
from .routes import workflows, tasks, plugins, health, auth

logger = structlog.get_logger()
settings = get_settings()


async def init_database_async():
    """Initialize database asynchronously (non-blocking)."""
    import time
    import asyncio
    max_retries = 5
    for attempt in range(max_retries):
        try:
            from ..db.database import init_db, engine
            from ..db.models import Base
            logger.info("initializing_database_tables", attempt=attempt + 1)
            # Test connection first
            await asyncio.to_thread(engine.connect)
            # Initialize tables
            await asyncio.to_thread(init_db)
            logger.info("database_initialized_successfully", tables=list(Base.metadata.tables.keys()))
            break
        except Exception as e:
            if attempt < max_retries - 1:
                logger.warning("database_init_retry", attempt=attempt + 1, error=str(e))
                await asyncio.sleep(2)
            else:
                logger.error("database_initialization_failed", error=str(e))
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
    
    # Middleware
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
    
    # Include API routers FIRST (before static files)
    app.include_router(health.router, prefix="/api", tags=["Health"])
    app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
    app.include_router(workflows.router, prefix="/api/workflows", tags=["Workflows"])
    app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
    app.include_router(plugins.router, prefix="/api/plugins", tags=["Plugins"])
    
    # AI-powered endpoints
    from .routes import llm
    app.include_router(llm.router, prefix="/api/llm", tags=["AI & LLM"])
    
    # Serve React frontend (if built)
    ui_dist_path = Path(__file__).parent.parent.parent / "ui" / "dist"
    logger.info("checking_frontend_path", 
                path=str(ui_dist_path), 
                exists=ui_dist_path.exists(),
                absolute_path=str(ui_dist_path.absolute()))
    
    if ui_dist_path.exists():
        # List contents for debugging
        try:
            contents = list(ui_dist_path.iterdir())
            logger.info("serving_react_frontend", 
                       path=str(ui_dist_path),
                       files=[f.name for f in contents])
        except Exception as e:
            logger.error("error_listing_frontend", error=str(e))
        
        # Root path - serve index.html
        @app.get("/")
        async def root():
            """Serve React app root."""
            index_file = ui_dist_path / "index.html"
            logger.info("serving_root", index_exists=index_file.exists())
            if index_file.exists():
                return FileResponse(index_file)
            return JSONResponse(status_code=404, content={"error": "Frontend not built"})
        
        # Mount static files (JS, CSS, images)
        assets_path = ui_dist_path / "assets"
        if assets_path.exists():
            app.mount("/assets", StaticFiles(directory=str(assets_path)), name="assets")
            logger.info("mounted_assets", path=str(assets_path))
        else:
            logger.warning("assets_not_found", path=str(assets_path))
        
        # Serve index.html for all non-API routes (SPA routing)
        @app.get("/{full_path:path}")
        async def serve_react_app(full_path: str):
            """Serve React app for all non-API routes."""
            logger.info("catch_all_route", path=full_path)
            
            # If path starts with /api, let it 404 naturally
            if full_path.startswith("api/"):
                return JSONResponse(status_code=404, content={"error": "Not Found"})
            
            # Serve index.html for all other routes (React Router handles routing)
            index_file = ui_dist_path / "index.html"
            if index_file.exists():
                return FileResponse(index_file)
            return JSONResponse(status_code=404, content={"error": "Frontend not built"})
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
                "note": "Frontend UI not built. Build with: cd ui && npm install && npm run build"
            }
    
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
