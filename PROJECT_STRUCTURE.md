# 📁 Project Structure - Important Information

**Last Updated:** October 4, 2025

---

## ✅ Correct Directory Structure

### **Your Git Repository (What Render Deploys):**
```
D:\Webtool\VS project\green-toolkit-backend\green-toolkit-backend\
├── main.py                    ✅ Main FastAPI application
├── pdf_generator.py           ✅ PDF generation module
├── run_server.py              ✅ Server startup script
├── requirements.txt           ✅ Python dependencies
├── render.yaml                ✅ Render deployment config
├── templates/                 ✅ HTML templates
│   ├── index.html
│   ├── sim.html
│   ├── tools.html
│   └── gamification.html
├── venv/                      ⚠️ Virtual environment (not in git)
├── __pycache__/               ⚠️ Python cache (not in git)
└── ... other files
```

### **Git Repository Info:**
- **GitHub Repo:** `sufyanaslam44/green-toolkit-backend`
- **Branch:** `main`
- **Working Directory:** `D:\Webtool\VS project\green-toolkit-backend\green-toolkit-backend\`

---

## 🚨 Common Mistakes to Avoid

### ❌ **Don't Work in the Wrong Directory**

**WRONG Directory (outer folder):**
```
D:\Webtool\VS project\green-toolkit-backend\
```
☝️ This is NOT your git repository!

**CORRECT Directory (inner folder):**
```
D:\Webtool\VS project\green-toolkit-backend\green-toolkit-backend\
```
☝️ This IS your git repository! Always work here.

---

## 🔍 How to Tell You're in the Right Place

### **Method 1: Check for `.git` folder**
```powershell
cd "D:\Webtool\VS project\green-toolkit-backend\green-toolkit-backend"
Test-Path .git
# Should return: True
```

### **Method 2: Run git status**
```powershell
cd "D:\Webtool\VS project\green-toolkit-backend\green-toolkit-backend"
git status
# Should show: "On branch main" (not "fatal: not a git repository")
```

### **Method 3: Check for key files**
```powershell
cd "D:\Webtool\VS project\green-toolkit-backend\green-toolkit-backend"
Get-ChildItem main.py, pdf_generator.py, requirements.txt
# Should show all three files
```

---

## 📝 What Was Fixed

### **Issue Discovered:**
You had a **duplicate `pdf_generator.py`** in the outer folder that was NOT tracked by git:
```
D:\Webtool\VS project\green-toolkit-backend\pdf_generator.py  ❌ (deleted)
```

### **Solution Applied:**
- ✅ Deleted the duplicate `pdf_generator.py` from outer folder
- ✅ Confirmed correct `pdf_generator.py` in git repository
- ✅ Verified all critical files are in the correct location

---

## 🚀 Render.com Deployment Structure

### **What Render Sees (From GitHub):**
```
/ (repo root)
├── main.py
├── pdf_generator.py
├── requirements.txt
├── render.yaml
└── templates/
```

### **Render's Build Command (from render.yaml):**
```yaml
buildCommand: pip install -r requirements.txt && python -m playwright install chromium
```

### **Render's Start Command:**
```yaml
startCommand: python run_server.py
```

### **Render's File Paths:**
- **Repository:** `/opt/render/project/src/`
- **Chromium:** `/opt/render/.cache/ms-playwright/chromium-1140/`
- **Python venv:** `/opt/render/project/src/.venv/`

---

## 🛠️ Working with the Project

### **Always Start Here:**
```powershell
# Navigate to the CORRECT directory
cd "D:\Webtool\VS project\green-toolkit-backend\green-toolkit-backend"

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Now you can run commands
python run_server.py
```

### **Git Commands (Always from Correct Directory):**
```powershell
cd "D:\Webtool\VS project\green-toolkit-backend\green-toolkit-backend"

# Check status
git status

# Add changes
git add .

# Commit
git commit -m "Your message"

# Push to GitHub (triggers Render deployment)
git push origin main
```

---

## 📊 File Status

| File | Location | Status | Purpose |
|------|----------|--------|---------|
| `main.py` | Inner folder | ✅ Tracked | FastAPI app |
| `pdf_generator.py` | Inner folder | ✅ Tracked | PDF generation |
| `requirements.txt` | Inner folder | ✅ Tracked | Dependencies |
| `render.yaml` | Inner folder | ✅ Tracked | Render config |
| `run_server.py` | Inner folder | ✅ Tracked | Server starter |
| `venv/` | Inner folder | ⚠️ Not tracked | Local Python env |
| `__pycache__/` | Inner folder | ⚠️ Not tracked | Python cache |
| `*.pdf` | Inner folder | ⚠️ Not tracked | Generated PDFs |

---

## ✅ Verification Checklist

Before pushing to GitHub/Render:

- [ ] Working in correct directory: `green-toolkit-backend\green-toolkit-backend\`
- [ ] Git status shows tracked files only
- [ ] No duplicate files in outer folder
- [ ] Virtual environment activated (for local testing)
- [ ] Local testing successful (`python run_server.py`)
- [ ] PDF generation works locally
- [ ] All changes committed to git
- [ ] Ready to push to GitHub

---

## 🔗 Quick Links

- **GitHub Repo:** https://github.com/sufyanaslam44/green-toolkit-backend
- **Render Dashboard:** https://dashboard.render.com/
- **Local Server:** http://localhost:8000
- **Health Check:** http://localhost:8000/api/health

---

## 💡 Pro Tips

1. **Always use absolute paths** when navigating in PowerShell
2. **Check `git status`** before committing to avoid accidental files
3. **Test locally first** before pushing to GitHub
4. **Clear Render cache** when changing dependencies or build process
5. **Keep this structure clean** - don't create duplicate files

---

**Remember:** The inner `green-toolkit-backend\green-toolkit-backend\` folder is your git repository and matches what Render deploys. Always work from there!

