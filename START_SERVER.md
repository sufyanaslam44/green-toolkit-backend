# 🚀 How to Start the Server

## ⚠️ IMPORTANT: Windows + Python 3.13 Users

You **MUST** start the server using one of these methods. Using `uvicorn` directly will cause `NotImplementedError`!

---

## ✅ CORRECT STARTUP METHODS

### Method 1: Python Script (Recommended for all users)
```bash
python run_server.py
```

### Method 2: Windows Batch File
```bash
start_server.bat
```
Or double-click `start_server.bat` in File Explorer

### Method 3: PowerShell Script
```powershell
.\start_server.ps1
```

---

## ❌ WRONG METHODS - DO NOT USE!

```bash
# ❌ This will FAIL with NotImplementedError
uvicorn main:app --reload

# ❌ This will also FAIL
python -m uvicorn main:app --reload

# ❌ This will also FAIL
uvicorn main:app
```

---

## 🔍 How to Tell If Server Started Correctly

### ✅ Correct Startup - You'll see:
```
✅ Windows ProactorEventLoop policy set correctly
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### ❌ Wrong Startup - You'll see:
```
⚠️  WARNING: Event loop policy not set correctly!
⚠️  PDF generation will FAIL with NotImplementedError
```

---

## 🐛 Troubleshooting

### Problem: Port 8000 already in use

**Solution:**
```powershell
# Kill existing Python processes
Get-Process | Where-Object { $_.ProcessName -eq "python" } | Stop-Process -Force

# Then restart
python run_server.py
```

### Problem: PDF generation fails with NotImplementedError

**Cause:** You used `uvicorn main:app` instead of `python run_server.py`

**Solution:**
1. Stop the server (Ctrl+C)
2. Restart using: `python run_server.py`

### Problem: Module not found errors

**Solution:**
```bash
# Make sure virtual environment is activated
..\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Then start
python run_server.py
```

---

## 📝 Why Is This Necessary?

**Technical Explanation:**

On Windows with Python 3.13, the default event loop (`SelectorEventLoop`) **does not support subprocesses**. Playwright needs to spawn Chromium as a subprocess to generate PDFs.

The solution is to use `WindowsProactorEventLoopPolicy`, which **must be set BEFORE** the event loop is created.

When you use `uvicorn main:app` directly, uvicorn creates its event loop during import, which happens BEFORE our policy can be set in `main.py`.

The `run_server.py` script sets the policy FIRST, then starts uvicorn, ensuring Playwright can spawn subprocesses.

---

## 🎯 Quick Reference

| Command | Result |
|---------|--------|
| `python run_server.py` | ✅ Works |
| `start_server.bat` | ✅ Works |
| `.\start_server.ps1` | ✅ Works |
| `uvicorn main:app` | ❌ Fails |
| `uvicorn main:app --reload` | ❌ Fails |
| `python -m uvicorn main:app` | ❌ Fails |

---

**Always use: `python run_server.py`** 🎉
