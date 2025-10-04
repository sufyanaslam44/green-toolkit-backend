# 🔄 How to Update Render.com Deployment

## Method 1: Automatic Deployment (When You Make Code Changes)

Render automatically deploys when you push to GitHub:

```bash
# 1. Make your code changes
# 2. Stage and commit
git add .
git commit -m "Your descriptive commit message"

# 3. Push to GitHub
git push origin main

# 4. Render automatically detects the push and deploys
# Watch the build logs in Render Dashboard
```

**Deployment Time:** ~5-10 minutes

---

## Method 2: Manual Deploy (Force Redeploy Without Code Changes)

### Option A: Quick Deploy (Uses Cache)
1. Go to: https://dashboard.render.com/
2. Click your service: `green-toolkit-backend`
3. Click **"Manual Deploy"** dropdown
4. Select **"Deploy latest commit"**
5. Wait ~3-5 minutes

### Option B: Clean Deploy (Clears Cache) ⚠️
1. Go to: https://dashboard.render.com/
2. Click your service: `green-toolkit-backend`
3. Click **"Manual Deploy"** dropdown
4. Select **"Clear build cache & deploy"**
5. Wait ~5-10 minutes

> **When to use Clear Cache:**
> - Playwright/browser version issues
> - Dependency conflicts
> - Mysterious build failures
> - After changing build commands

---

## Method 3: Rollback to Previous Version

If new deployment breaks something:

1. Go to: https://dashboard.render.com/
2. Click your service: `green-toolkit-backend`
3. Go to **"Events"** tab
4. Find the working deployment
5. Click **"Rollback to this version"**

---

## 🔍 Monitoring Deployment Status

### View Build Logs
1. Go to Render Dashboard
2. Click your service
3. Click **"Logs"** tab
4. Select **"Build"** filter

### View Runtime Logs
1. Go to Render Dashboard
2. Click your service
3. Click **"Logs"** tab
4. Select **"Service"** filter

### Check Health Status
- Green circle = Healthy
- Yellow circle = Starting
- Red circle = Failed

---

## 📝 Common Update Scenarios

### Scenario 1: Changed Python Code
```bash
git add main.py pdf_generator.py
git commit -m "Fixed PDF generation logic"
git push origin main
# Render auto-deploys ✓
```

### Scenario 2: Updated Dependencies
```bash
git add requirements.txt
git commit -m "Updated playwright to 1.48.0"
git push origin main
# ⚠️ THEN: Clear build cache in Render dashboard
```

### Scenario 3: Changed Build Process
```bash
git add render.yaml
git commit -m "Updated build command"
git push origin main
# ⚠️ THEN: Clear build cache in Render dashboard
```

### Scenario 4: Changed Environment Variables
1. No code push needed
2. Go to Render Dashboard
3. Click **"Environment"** tab
4. Update variables
5. Click **"Save Changes"**
6. Service automatically restarts

---

## ⚡ Quick Checklist Before Pushing

- [ ] Code runs locally without errors
- [ ] PDF generation works on localhost
- [ ] All files committed to git
- [ ] Pushed to GitHub
- [ ] Build command in render.yaml is correct
- [ ] Environment variables set in Render dashboard
- [ ] Health check endpoint returns 200

---

## 🐛 Troubleshooting Failed Deployments

### Build Fails
1. Check build logs for error message
2. Verify `requirements.txt` has no conflicts
3. Try clearing build cache
4. Check Python version (3.11 or 3.13 recommended)

### Deployment Succeeds But Service Crashes
1. Check runtime logs
2. Verify start command: `python run_server.py`
3. Check if PORT environment variable is used
4. Verify Chromium installed correctly

### PDF Generation Fails
1. Check runtime logs for Chromium path
2. Verify Playwright version matches Chromium build
3. Clear build cache if needed
4. Check memory usage (may need to upgrade plan)

---

## 📊 Expected Timeline

| Action | Time | Notes |
|--------|------|-------|
| Git push to GitHub | ~1 second | Fast |
| Render detects change | ~10 seconds | Auto-detect |
| Build (with cache) | ~3-5 minutes | Quick |
| Build (clean, no cache) | ~5-10 minutes | Downloads everything |
| Service restart | ~30 seconds | After build |
| Total deployment | ~4-11 minutes | End to end |

---

## 💡 Pro Tips

1. **Always test locally first** before pushing
2. **Use descriptive commit messages** to track changes
3. **Watch build logs** during first deployment
4. **Set up Slack/Discord notifications** in Render for deployment alerts
5. **Keep a deployment checklist** for complex changes

---

## 🔗 Useful Links

- Render Dashboard: https://dashboard.render.com/
- Your Service URL: Check in Render dashboard
- GitHub Repo: https://github.com/sufyanaslam44/green-toolkit-backend
- Render Docs: https://render.com/docs

---

**Last Updated:** October 4, 2025
