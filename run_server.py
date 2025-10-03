"""
Startup script for FastAPI server with Windows compatibility
This must be run BEFORE uvicorn to set the correct event loop policy
"""
import sys
import asyncio

# CRITICAL: Set Windows event loop policy BEFORE importing FastAPI/uvicorn
if sys.platform == 'win32':
    # Use ProactorEventLoop for subprocess support (needed by Playwright)
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# Now import and run uvicorn
import uvicorn
from main import app

if __name__ == "__main__":
    # Run uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,  # Set to True for development
        log_level="info"
    )
