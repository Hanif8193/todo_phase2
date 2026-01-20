"""
FastAPI application entry point.

This module configures:
- FastAPI app instance
- CORS middleware
- Database initialization on startup
- Route registration
- Application lifecycle events
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from config import settings
from db import init_db, close_db
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Validate configuration on startup
settings.validate()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.

    Handles startup and shutdown events:
    - Startup: Initialize database tables
    - Shutdown: Close database connections
    """
    # Startup: Initialize database
    print("Initializing database...")
    await init_db()
    print("Application startup complete")

    yield

    # Shutdown: Close database connections
    print("Shutting down application...")
    await close_db()
    print("Application shutdown complete")


# Create FastAPI application instance
app = FastAPI(
    title="Todo Application API",
    description="Phase II - Multi-user todo application with JWT authentication",
    version="2.0.0",
    lifespan=lifespan,
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Log all incoming requests and responses.

    Logs:
    - Request method and path
    - Response status code
    - Request processing time
    """
    start_time = time.time()

    # Log request
    logger.info(f"Request: {request.method} {request.url.path}")

    # Process request
    response = await call_next(request)

    # Calculate processing time
    process_time = time.time() - start_time

    # Log response
    logger.info(
        f"Response: {request.method} {request.url.path} "
        f"Status: {response.status_code} Time: {process_time:.3f}s"
    )

    # Add custom header with processing time
    response.headers["X-Process-Time"] = str(process_time)

    return response


# Health check endpoint
@app.get("/", tags=["Health"])
async def root():
    """
    Root endpoint for health checks.

    Returns:
        dict: Application status and version
    """
    return {
        "status": "ok",
        "message": "Todo Application API",
        "version": "2.0.0",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.

    Returns:
        dict: Application health status
    """
    return {
        "status": "healthy",
        "database": "connected",
    }


# Import and register route routers
# Note: Import here to avoid circular dependencies
from routes import auth, tasks

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(tasks.router, prefix="/api", tags=["Tasks"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=True,  # Auto-reload on code changes (development only)
    )
