"""
Vercel serverless handler for FastAPI application.
Vercel's Python runtime natively supports ASGI apps - no adapter needed.
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import from backend/
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

# Initialize database on cold start
import asyncio

_db_initialized = False

async def init_database_async():
    """Initialize database tables."""
    global _db_initialized
    if not _db_initialized:
        try:
            from db import init_db
            await init_db()
            _db_initialized = True
            print("✓ Database initialized for serverless")
        except Exception as e:
            # Tables might already exist - this is fine
            print(f"Database init: {e}")
            _db_initialized = True

# Run initialization synchronously on module load
try:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(init_database_async())
    loop.close()
except Exception as e:
    print(f"Init error: {e}")

# Import the FastAPI app
from main import app

# Export the FastAPI app directly - Vercel supports ASGI natively
# No Mangum wrapper needed!
