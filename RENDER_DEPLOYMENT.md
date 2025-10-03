# 🚀 Deploying to Render.com

This guide explains how to deploy the Green Chemistry Toolkit to Render.com with Playwright support.

## 📋 Prerequisites

- GitHub repository with your code
- Render.com account (free tier works)
- Python 3.13 selected in Render

## 🔧 Files Added for Deployment

### 1. `build.sh` - Build Script
This script runs during deployment to:
- Install Python dependencies from `requirements.txt`
- Install Playwright Chromium browser
- Install system dependencies for Chromium

### 2. `render.yaml` - Render Configuration
Defines the service configuration:
- Python environment
- Build and start commands
- Environment variables
- Health check endpoint

## 📝 Deployment Steps

### Option A: Using render.yaml (Recommended)

1. **Push these files to your GitHub repository:**
   - `build.sh`
   - `render.yaml`
   - All other project files

2. **In Render Dashboard:**
   - Click "New +"
   - Select "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml`
   - Click "Apply"

### Option B: Manual Configuration

1. **In Render Dashboard:**
   - Click "New +"
   - Select "Web Service"
   - Connect your GitHub repository

2. **Configure the service:**
   ```
   Name: green-toolkit-backend
   Region: Oregon (or your choice)
   Branch: main
   Root Directory: green-toolkit-backend (if nested)
   Runtime: Python 3
   Build Command: bash build.sh
   Start Command: python run_server.py
   Plan: Free
   ```

3. **Add Environment Variables:**
   ```
   PYTHON_VERSION = 3.13.0
   PLAYWRIGHT_BROWSERS_PATH = /opt/render/.cache/ms-playwright
   ```

4. **Click "Create Web Service"**

## ⚙️ Important Configuration Notes

### Build Command
**Must be:** `bash build.sh`

This runs the build script that installs Playwright browsers. DO NOT use just `pip install -r requirements.txt` - it won't install the browsers!

### Start Command
**Must be:** `python run_server.py`

This ensures the Windows event loop policy compatibility (though not needed on Linux, it doesn't hurt).

### Python Version
**Recommended:** Python 3.11 or 3.13

Playwright works on both. If you have issues, try 3.11.

### Health Check
The service uses `/api/health` endpoint for health checks. This is already configured in `render.yaml`.

## 🐛 Troubleshooting

### Problem: "Executable doesn't exist at /opt/render/.cache/ms-playwright/..."

**Cause:** Playwright browsers not installed during build.

**Solution:**
1. Make sure `build.sh` is executable (should be by default)
2. Check that Build Command is: `bash build.sh`
3. Check build logs for errors in browser installation
4. Try manual redeploy

### Problem: Build fails with "playwright: command not found"

**Cause:** Playwright not installed yet when trying to run `playwright install`.

**Solution:** The `build.sh` script already handles this correctly:
```bash
pip install -r requirements.txt  # This installs playwright
playwright install chromium      # Now this works
```

### Problem: PDF generation timeout

**Cause:** Chromium takes longer to start on slower servers.

**Solution:** Increase timeout in `pdf_generator.py` (if needed):
```python
browser = await p.chromium.launch(
    headless=True,
    args=['--disable-gpu', '--no-sandbox', '--disable-dev-shm-usage'],
    timeout=60000  # 60 seconds
)
```

### Problem: Memory issues on free tier

**Cause:** Chromium is memory-intensive.

**Solution:**
1. Use the `--disable-dev-shm-usage` flag (already added)
2. Consider upgrading to Starter plan ($7/month)
3. Reduce number of concurrent PDF generations

## 📊 Expected Build Output

During deployment, you should see:

```
Installing Python dependencies...
✓ Successfully installed fastapi, playwright, etc.

Installing Playwright browsers...
✓ Downloaded Chromium 1187 (chromium-1187) - 147 Mb

Installing system dependencies for Playwright...
✓ Installing dependencies for Chromium...

Build completed successfully!
```

## ✅ Verification

After deployment, test PDF generation:

1. **Visit your Render URL:** `https://your-app.onrender.com/simulate`
2. **Load example data**
3. **Run simulation**
4. **Click "Generate PDF Report"**
5. **PDF should download** ✅

## 🔐 Security Notes

### CORS Settings
The current configuration allows all origins:
```python
allow_origins=["*"]
```

For production, update in `main.py`:
```python
allow_origins=[
    "https://your-frontend.com",
    "https://www.your-frontend.com"
]
```

### Environment Variables
Add sensitive data as environment variables in Render dashboard, not in code.

## 📈 Performance Tips

### 1. Keep Chromium Warm
Consider adding a warmup endpoint that generates a dummy PDF on startup to keep Chromium cached.

### 2. Use CDN for Static Files
Serve static files through a CDN to reduce load on the server.

### 3. Enable Caching
Add caching headers for static assets.

### 4. Monitor Memory
Watch memory usage in Render dashboard. If consistently high, upgrade plan.

## 🔄 Continuous Deployment

Render automatically deploys when you push to GitHub:
1. Push changes to GitHub
2. Render detects changes
3. Runs build script
4. Deploys automatically

## 💰 Cost Estimates

### Free Tier
- **Cost:** $0/month
- **Memory:** 512 MB
- **Sleeps after inactivity:** Yes (30 min)
- **Good for:** Testing, demos

### Starter Tier
- **Cost:** $7/month
- **Memory:** 512 MB - 2 GB
- **Always on:** Yes
- **Good for:** Production with moderate traffic

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [Playwright on Render](https://render.com/docs/playwright)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)

## 🎯 Quick Checklist

Before deploying:
- [ ] `build.sh` exists and has browser installation
- [ ] `render.yaml` or manual config is set up
- [ ] Build Command: `bash build.sh`
- [ ] Start Command: `python run_server.py`
- [ ] Environment variables configured
- [ ] Code pushed to GitHub
- [ ] Render service created
- [ ] Health check endpoint working
- [ ] PDF generation tested

---

**Deployment Status:** 🟢 Ready for Render.com deployment!

**Last Updated:** October 3, 2025
