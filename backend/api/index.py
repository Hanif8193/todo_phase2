"""
Vercel serverless handler for FastAPI application.
"""

import sys
from pathlib import Path

# Add parent directory to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from main import app as fastapi_app
from mangum import Mangum

# Initialize database on first import
_initialized = False

def init_database():
    """Initialize database tables if not already initialized."""
    global _initialized
    if not _initialized:
        try:
            import asyncio
            from db import init_db
            asyncio.run(init_db())
            _initialized = True
            print("Database initialized successfully")
        except Exception as e:
            print(f"Database initialization: {e}")
            _initialized = True

# Initialize on module load
init_database()

# Create the handler
app = Mangum(fastapi_app, lifespan="off")
