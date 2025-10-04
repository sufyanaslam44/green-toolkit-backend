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
    # Get port from environment (Render provides PORT env variable)
    import os
    port = int(os.environ.get("PORT", 8000))
    
    print(f"🚀 Starting server on port {port}")
    print(f"📋 Platform: {sys.platform}")
    
    # Run uvicorn with production-optimized settings
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info",
        access_log=False,  # Reduce memory usage
        workers=1,  # Single worker for free tier memory constraints
        limit_concurrency=10,  # Limit concurrent requests
        timeout_keep_alive=5  # Close idle connections faster
    )
