# 🚨 URGENT: Fix Render Build Command

## Problem:
Render is trying to run `bash build.sh` even though we deleted the file. This is because the build command is **hardcoded in Render's dashboard settings** and overriding `render.yaml`.

---

## ✅ Solution: Update Build Command in Render Dashboard

### Step 1: Go to Render Dashboard Settings

1. Go to: https://dashboard.render.com/
2. Click your service: **"green-toolkit-backend"**
3. Click **"Settings"** tab (left sidebar)
4. Scroll down to **"Build & Deploy"** section

---

### Step 2: Update Build Command

Find the **"Build Command"** field. It currently says:
```bash
bash build.sh
```

**Change it to:**
```bash
pip install -r requirements.txt && python -m playwright install chromium
```

---

### Step 3: Save and Clear Cache

1. Click **"Save Changes"** button
2. Go back to the main service page
3. Click **"Manual Deploy"** dropdown ▼
4. Select **"Clear build cache & deploy"** ⚠️
5. Wait 5-10 minutes

---

## 📋 Expected Build Logs (After Fix):

```bash
==> Installing dependencies
==> Running: pip install -r requirements.txt && python -m playwright install chromium

Successfully installed playwright-1.48.0 ✓

Downloading Chromium 133.0.6943.17 (playwright build v1129)
173.7 MiB [====================] 100%
Chromium 133.0.6943.17 (playwright build v1129) downloaded to /opt/render/.cache/ms-playwright/chromium-1129 ✓

==> Build successful ✅
```

---

## 🎯 Why This Happened:

- **render.yaml** → Used for NEW services created from YAML
- **Dashboard Settings** → Overrides YAML for EXISTING services
- **Solution** → Update dashboard settings to match render.yaml

---

## ⚡ Quick Screenshot Guide:

**Where to find it:**
```
Dashboard → Your Service → Settings (left sidebar) → Build & Deploy section
```

**What to change:**
```
OLD: bash build.sh
NEW: pip install -r requirements.txt && python -m playwright install chromium
```

**Then:**
- Click "Save Changes"
- Manual Deploy → "Clear build cache & deploy"

---

## ✅ After Successful Deployment:

Your runtime logs should show:
```
✅ Chromium found at: /opt/render/.cache/ms-playwright/chromium-1129/chrome-linux/chrome
✅ Chromium executable verified
INFO: Application startup complete
```

Then test PDF generation at:
```
https://green-toolkit-backend.onrender.com/simulate
```

---

**Your code is 100% correct. Just need to update this one dashboard setting!** 🚀
