"""
Production startup script for FastAPI server on Render.com
"""
import os
import sys
import logging

# Configure logging for production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import after logging setup
import uvicorn
from main import app

if __name__ == "__main__":
    # Get port from environment (Render provides PORT env variable)
    port = int(os.environ.get("PORT", 8000))
    env = os.environ.get("ENV", "development")
    
    logger.info(f"🚀 Starting Green Toolkit Backend")
    logger.info(f"📋 Environment: {env}")
    logger.info(f"🌐 Port: {port}")
    logger.info(f"� Platform: {sys.platform}")
    logger.info(f"🐍 Python: {sys.version}")
    
    # Production-optimized settings for Render free tier
    uvicorn_config = {
        "app": app,
        "host": "0.0.0.0",
        "port": port,
        "reload": False,
        "log_level": "info",
        "access_log": env != "production",  # Disable access logs in production to save memory
        "workers": 1,  # Single worker for free tier memory constraints (512MB)
        "limit_concurrency": 50,  # Allow more concurrent requests
        "timeout_keep_alive": 30,  # Keep connections alive longer for better performance
        "loop": "asyncio",  # Use asyncio for better async performance
    }
    
    # Additional production optimizations
    if env == "production":
        uvicorn_config.update({
            "timeout_keep_alive": 5,  # Shorter timeout in production
            "limit_concurrency": 20,  # Lower concurrency for stability
        })
    
    logger.info("🔧 Uvicorn configuration:")
    for key, value in uvicorn_config.items():
        if key != "app":  # Don't log the app object
            logger.info(f"   {key}: {value}")
    
    try:
        uvicorn.run(**uvicorn_config)
    except Exception as e:
        logger.error(f"❌ Failed to start server: {e}")
        sys.exit(1)
