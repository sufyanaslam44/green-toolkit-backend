# 🎯 Render Deployment - Quick Reference

## 🚀 Quick Start (2 Minutes)

### 1. Push Files to GitHub
Ensure these files are in your repo:
- ✅ `build.sh` (browser installation script)
- ✅ `render.yaml` (Render configuration)
- ✅ `requirements.txt` (Python dependencies)
- ✅ All other project files

### 2. Deploy on Render
**Option A: Using Blueprint (Easiest)**
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Blueprint"**
3. Connect GitHub repository
4. Click **"Apply"**
5. ✅ Done! Wait 5-10 minutes for build

**Option B: Manual Setup**
1. Click **"New +"** → **"Web Service"**
2. Connect GitHub repository
3. Configure:
   - Build Command: `bash build.sh`
   - Start Command: `python run_server.py`
4. Click **"Create Web Service"**
5. ✅ Done! Wait 5-10 minutes for build

### 3. Test
Visit: `https://your-app.onrender.com/simulate`

---

## ⚙️ Critical Configuration

### Build Command
```bash
bash build.sh
```
☝️ This installs Playwright browsers!

### Start Command
```bash
python run_server.py
```

### Environment Variables (Optional)
```
PLAYWRIGHT_BROWSERS_PATH=/opt/render/.cache/ms-playwright
```

---

## 🐛 If PDF Generation Fails

### Check Build Logs
Look for:
```
✓ Downloaded Chromium 1187 (chromium-1187) - 147 Mb
```

### If Missing, Verify:
1. ✅ Build command is `bash build.sh` (not just `pip install`)
2. ✅ `build.sh` file exists in repo
3. ✅ File has correct content with `playwright install chromium`

### Redeploy:
1. Go to your service
2. Click **"Manual Deploy"** → **"Deploy latest commit"**
3. Watch build logs

---

## 📋 Troubleshooting Checklist

- [ ] `build.sh` pushed to GitHub
- [ ] Build command is `bash build.sh`
- [ ] Start command is `python run_server.py`
- [ ] Build logs show "Downloaded Chromium"
- [ ] Service is deployed (not failed)
- [ ] Health check endpoint `/api/health` works
- [ ] Try PDF generation from `/simulate`

---

## 💡 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| `Executable doesn't exist` | Build script not running → Check build command |
| `playwright: command not found` | Order issue → Ensure pip install runs before playwright install |
| PDF timeout | Add `timeout=60000` to browser launch |
| Memory errors | Add `--disable-dev-shm-usage` flag (already added) |
| Service sleeps | Normal on free tier → Upgrade to Starter ($7/mo) |

---

## 🎯 Success Indicators

### ✅ Successful Deployment
```
Build logs show:
✓ Installing Python dependencies...
✓ Installing Playwright browsers...
✓ Downloaded Chromium 1187
✓ Build completed successfully!

Service shows:
🟢 Live
```

### ✅ Working PDF Generation
1. Open `/simulate`
2. Load example
3. Run simulation
4. Click "Generate PDF Report"
5. **PDF downloads** 🎉

---

## 📞 Need Help?

1. **Check build logs** - Most issues show here
2. **Check deployment logs** - Runtime errors appear here
3. **Check Render Community** - [community.render.com](https://community.render.com)
4. **Read full guide** - See `RENDER_DEPLOYMENT.md`

---

**Quick Fix:** Delete service and redeploy with correct build command! 🔄
