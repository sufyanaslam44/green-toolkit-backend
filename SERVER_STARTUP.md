# 🚀 Starting the Server - Windows Fix

## ⚠️ Important: Server Startup on Windows

When using **Windows + Python 3.13 + Playwright**, you **MUST** start the server using one of these methods to ensure proper event loop configuration.

## ❌ DON'T Use (Will Fail)

```bash
# ❌ This will cause NotImplementedError
uvicorn main:app --reload
```

**Why it fails:** The event loop policy must be set BEFORE uvicorn creates its event loop, but uvicorn starts before the policy can be set in `main.py`.

## ✅ DO Use (Will Work)

### Method 1: Python Startup Script (Recommended)

```bash
python run_server.py
```

This script:
- ✅ Sets Windows event loop policy FIRST
- ✅ Then starts uvicorn
- ✅ Ensures Playwright subprocess support

### Method 2: Batch File (Windows)

```bash
start_server.bat
```

Double-click the file or run from command prompt.

### Method 3: PowerShell Script

```powershell
.\start_server.ps1
```

Or right-click → "Run with PowerShell"

### Method 4: Direct Python with Environment Variable

```bash
# Set policy before starting
python -c "import sys, asyncio; sys.platform=='win32' and asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())" & python run_server.py
```

## How It Works

### The Problem

```python
# In main.py - TOO LATE!
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

app = FastAPI()  # Uvicorn already created event loop before this runs
```

### The Solution

```python
# In run_server.py - BEFORE uvicorn starts
import asyncio

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# NOW start uvicorn
import uvicorn
uvicorn.run(app, ...)
```

## Files Created

1. **`run_server.py`** - Python startup script
   ```bash
   python run_server.py
   ```

2. **`start_server.bat`** - Windows batch file
   ```bash
   start_server.bat
   ```

3. **`start_server.ps1`** - PowerShell script
   ```powershell
   .\start_server.ps1
   ```

## Verification

When the server starts correctly, you'll see:

```
[STARTUP] Windows ProactorEventLoop policy set
[STARTUP] Starting FastAPI server with Playwright support...
[STARTUP] Event loop policy: <asyncio.windows_events.WindowsProactorEventLoopPolicy object at 0x...>
INFO:     Started server process [18396]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

The key line is:
```
[STARTUP] Windows ProactorEventLoop policy set
```

## Testing PDF Generation

1. **Start server** using one of the methods above

2. **Open browser**: http://localhost:8000/simulate

3. **Generate PDF**:
   - Click "Load Example"
   - Click "Run Simulation"
   - Click "Generate PDF Report"
   - Check console for debug output
   - PDF should download successfully!

## Console Output When Generating PDF

You should see:

```
[PDF Generation] Received data for: Synthesis of Aspirin
[PDF Generation] Product: aspirin
[PDF Generation] Reactants count: 2
[PDF DEBUG] Starting PDF generation...
[PDF DEBUG] Output path: green_chem_report_Synthesis_of_Aspirin_20251003_230226.pdf
[PDF DEBUG] Generating HTML content...
[PDF DEBUG] HTML generated, length: 11711 chars
[PDF DEBUG] Initializing Playwright...
[PDF DEBUG] Playwright initialized
[PDF DEBUG] Launching Chromium...
[PDF DEBUG] Browser launched
[PDF DEBUG] Page created
[PDF DEBUG] Setting HTML content...
[PDF DEBUG] Content set
[PDF DEBUG] Generating PDF file...
[PDF DEBUG] PDF generated!
[PDF DEBUG] Browser closed
[PDF DEBUG] Success!
```

## Troubleshooting

### Error: NotImplementedError

**Problem:** Event loop policy not set correctly

**Solution:** Make sure you're using `python run_server.py`, NOT `uvicorn main:app`

### Error: ModuleNotFoundError

**Problem:** Virtual environment not activated

**Solution:** Activate venv first:
```bash
# Windows
.\venv\Scripts\Activate.ps1

# Then start
python run_server.py
```

### Can't Execute PowerShell Script

**Problem:** Execution policy restriction

**Solution:**
```powershell
# Run once to allow scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then run
.\start_server.ps1
```

## Development vs Production

### Development (with reload)

Edit `run_server.py` and change:
```python
uvicorn.run(
    app,
    host="0.0.0.0",
    port=8000,
    reload=True,  # Enable auto-reload
    log_level="info"
)
```

### Production (no reload)

Keep as:
```python
uvicorn.run(
    app,
    host="0.0.0.0",
    port=8000,
    reload=False,  # Disable reload for production
    log_level="info"
)
```

## Quick Reference

| Method | Command | Best For |
|--------|---------|----------|
| Python Script | `python run_server.py` | All users (recommended) |
| Batch File | `start_server.bat` | Windows CMD users |
| PowerShell | `.\start_server.ps1` | Windows PowerShell users |
| Direct | `uvicorn main:app` | ❌ DON'T USE on Windows |

## Environment Variables (Optional)

You can also set environment variables in `run_server.py`:

```python
import os

# Set environment variables
os.environ['PLAYWRIGHT_BROWSERS_PATH'] = '/path/to/browsers'

# Then run
uvicorn.run(app, ...)
```

## Port Configuration

To change the port, edit `run_server.py`:

```python
uvicorn.run(
    app,
    host="0.0.0.0",
    port=3000,  # Change port here
    reload=False
)
```

## Summary

✅ **Always use** `python run_server.py` on Windows  
❌ **Never use** `uvicorn main:app` directly on Windows  
🔍 **Check for** `[STARTUP] Windows ProactorEventLoop policy set` message  
📄 **Test with** PDF generation to verify it works  

---

**Status**: 🎉 Server startup configured for Windows  
**Files**: `run_server.py`, `start_server.bat`, `start_server.ps1`  
**Ready**: ✅ Use `python run_server.py` to start!
