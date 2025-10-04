# 🚨 CRITICAL: Clear Render Build Cache

## Problem

Chromium is NOT being installed because Render is using **cached build results** from previous deployments.

Your logs show:
```
[PDF] Chromium executable: /opt/render/.cache/ms-playwright/chromium-1140/chrome-linux/chrome
```

But this doesn't exist! You need Chromium for Playwright 1.48.0.

## Solution: Clear Build Cache

### **Step 1: Go to Render Dashboard**
https://dashboard.render.com/

### **Step 2: Select Your Service**
Click on: `green-toolkit-backend`

### **Step 3: Manual Deploy with Cache Clear**
1. Click the **"Manual Deploy"** dropdown button (top right)
2. Select **"Clear build cache & deploy"** ⚠️ THIS IS CRITICAL!
3. Wait 5-10 minutes for full rebuild

### **Step 4: Watch Build Logs**

You should see:
```bash
Installing Python dependencies...
Successfully installed fastapi-0.117.1 playwright-1.48.0 ...

Running: python -m playwright install chromium
Downloading Chromium 133.0.6943.17 (playwright build v1129)
173.7 MiB [====================] 100%
Chromium 133.0.6943.17 downloaded to /opt/render/.cache/ms-playwright/chromium-1129
```

### **Step 5: Verify Runtime Logs**

After deployment:
```bash
🚀 Green Toolkit Backend Starting...
✅ Chromium found at: /opt/render/.cache/ms-playwright/chromium-1129/chrome-linux/chrome
✅ Chromium executable verified
```

## Why This Happens

Render caches:
- Python packages
- Playwright browsers
- Build artifacts

When you update Playwright version or build commands, the cache must be cleared!

## If Still Fails After Cache Clear

Check build logs for:
- Did `python -m playwright install chromium` run?
- Was there a download progress bar?
- Did it say "downloaded to ..." ?

If NO download happened, add this to render.yaml:
```yaml
buildCommand: pip install -r requirements.txt && python -m playwright install --force chromium
```

The `--force` flag ensures re-download even if cached.
