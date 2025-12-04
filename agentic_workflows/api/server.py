"""FastAPI server for Agentic Workflows."""
import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import structlog
import time

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
    
    # Include routers
    app.include_router(health.router, prefix="/api", tags=["Health"])
    app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
    app.include_router(workflows.router, prefix="/api/workflows", tags=["Workflows"])
    app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
    app.include_router(plugins.router, prefix="/api/plugins", tags=["Plugins"])
    
    # AI-powered endpoints
    from .routes import llm
    app.include_router(llm.router, prefix="/api/llm", tags=["AI & LLM"])
    
    @app.on_event("startup")
    async def startup_event():
        logger.info("application_starting", version=settings.app_version, port=settings.api_port)
        logger.info("startup_complete", message="App ready to accept requests")
        
        # Initialize database in background (non-blocking)
        import asyncio
        asyncio.create_task(init_database_async())
    
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
