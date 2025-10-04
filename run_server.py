"""
Startup script for FastAPI server
"""
import sys
import os

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
