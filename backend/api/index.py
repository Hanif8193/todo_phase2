"""
Vercel serverless handler for FastAPI application.
Creates a serverless-optimized app without lifespan events.
"""

import sys
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time
import logging

# Add parent directory to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

# Import configuration and database
from config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app WITHOUT lifespan for serverless
app = FastAPI(
    title="Todo Application API",
    description="Phase II - Multi-user todo application with JWT authentication",
    version="2.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests and responses."""
    start_time = time.time()
    logger.info(f"Request: {request.method} {request.url.path}")

    response = await call_next(request)

    process_time = time.time() - start_time
    logger.info(
        f"Response: {request.method} {request.url.path} "
        f"Status: {response.status_code} Time: {process_time:.3f}s"
    )
    response.headers["X-Process-Time"] = str(process_time)

    return response

# Database initialization middleware (runs on first request)
_db_initialized = False

@app.middleware("http")
async def ensure_db_initialized(request: Request, call_next):
    """Initialize database on first request in serverless environment."""
    global _db_initialized
    if not _db_initialized:
        try:
            from db import init_db
            await init_db()
            _db_initialized = True
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.warning(f"Database initialization: {e}")
            _db_initialized = True  # Prevent retry on every request

    response = await call_next(request)
    return response

# Health check endpoints
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint for health checks."""
    return {
        "status": "ok",
        "message": "Todo Application API",
        "version": "2.0.0",
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "database": "connected",
    }

# Import and register route routers
from routes import auth, tasks

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(tasks.router, prefix="/api", tags=["Tasks"])
