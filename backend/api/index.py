"""
Vercel serverless handler for FastAPI application.

This module wraps the FastAPI app with Mangum to make it compatible
with Vercel's serverless environment.
"""

from mangum import Mangum
import sys
from pathlib import Path

# Add parent directory to path to import main module
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from main import app
from fastapi import Request
from typing import Callable

# Flag to track if database is initialized
_db_initialized = False

# Middleware to ensure database is initialized
@app.middleware("http")
async def ensure_db_middleware(request: Request, call_next: Callable):
    """
    Middleware to ensure database is initialized on first request.
    This is necessary for serverless environments where startup events don't fire.
    """
    global _db_initialized
    if not _db_initialized:
        try:
            from db import init_db
            await init_db()
            _db_initialized = True
            print("Database initialized for serverless function")
        except Exception as e:
            # Tables might already exist - this is fine
            print(f"Database initialization note: {e}")
            _db_initialized = True

    response = await call_next(request)
    return response

# Create Mangum handler for Vercel
handler = Mangum(app, lifespan="off")
