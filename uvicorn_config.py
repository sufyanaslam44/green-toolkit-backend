# Uvicorn Configuration for Windows + Python 3.13 + Playwright
# This ensures the correct event loop policy is set

import sys
import asyncio

# Set event loop policy BEFORE uvicorn starts
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# Uvicorn will import this and use the configured policy
loop = "asyncio"
