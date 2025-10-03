# Green Chemistry Toolkit Backend

FastAPI backend for the Green Chemistry Toolkit with PDF report generation.

## 🚀 Quick Start

### Prerequisites
- Python 3.13
- Virtual environment at `../venv/` (one level up from this folder)

### Installation

1. **Activate virtual environment:**
```bash
# PowerShell
..\venv\Scripts\Activate.ps1

# Command Prompt
..\venv\Scripts\activate.bat
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Install Playwright browsers:**
```bash
python -m playwright install chromium
```

### Running the Server

**⚠️ CRITICAL for Windows + Python 3.13:**

You **MUST** use the provided startup script to ensure Playwright works correctly.

#### ✅ CORRECT METHODS:

**Option 1: Python Script (Recommended)**
```bash
python run_server.py
```

**Option 2: Windows Batch File**
```bash
start_server.bat
```

**Option 3: PowerShell Script**
```powershell
.\start_server.ps1
```

#### ❌ WRONG METHODS (WILL FAIL):

```bash
# ❌ DO NOT USE - Will cause NotImplementedError
uvicorn main:app --reload

# ❌ DO NOT USE - Will cause NotImplementedError
python -m uvicorn main:app --reload
```

**Why?** These commands create the event loop BEFORE the Windows compatibility policy can be set, causing `NotImplementedError` when Playwright tries to spawn subprocess.

**Error you'll see if using wrong method:**
```
NotImplementedError
  File "C:\Program Files\Python313\Lib\asyncio\base_events.py", line 539
    raise NotImplementedError
```

**Solution:** Kill the server and restart using `python run_server.py`


### Access the Application

- **Home:** http://localhost:8000/
- **Simulation Tool:** http://localhost:8000/simulate
- **API Docs:** http://localhost:8000/docs

## 📋 Features

### API Endpoints

#### Calculators
- `POST /api/atom-economy` - Calculate atom economy
- `POST /api/e-factor` - Calculate E-factor
- `POST /api/e-factor-direct` - Calculate E-factor from waste
- `POST /api/pmi` - Calculate Process Mass Intensity
- `POST /api/rme` - Calculate Reaction Mass Efficiency
- `POST /api/carbon-efficiency` - Calculate carbon efficiency

#### Comprehensive Analysis
- `POST /api/impact/compute` - Compute all green chemistry metrics
- `POST /api/generate-pdf` - Generate PDF report

#### Web Pages
- `GET /` - Home page
- `GET /simulate` - Simulation interface
- `GET /tools` - Tools & calculators
- `GET /gamification` - Gamification page

### PDF Report Generation

Generate professional PDF reports with:
- Reaction details (name, product, reactants, solvents, catalysts)
- All computed metrics (Atom Economy, PMI, E-factor, RME, Carbon Efficiency, Safety Factor)
- Water intensity and energy metrics
- Detailed breakdown of masses
- AI improvement suggestions
- Professional formatting with color-coded metrics

## 🏗️ Project Structure

```
green-toolkit-backend/
├── main.py                 # FastAPI application and endpoints
├── pdf_generator.py        # PDF generation using Playwright
├── run_server.py          # Server startup script (USE THIS!)
├── start_server.bat       # Windows batch startup
├── start_server.ps1       # PowerShell startup
├── requirements.txt       # Python dependencies
├── SERVER_STARTUP.md      # Detailed startup guide
├── templates/             # HTML templates
│   ├── index.html        # Home page
│   ├── sim.html          # Simulation interface
│   ├── tools.html        # Tools page
│   └── gamification.html # Gamification page
└── vite_project_1/       # Frontend project (if applicable)
```

## 🔧 Configuration

### Server Settings

Edit `run_server.py` to change:
- **Port:** Change `port=8000` to your desired port
- **Host:** Change `host="0.0.0.0"` to restrict access
- **Reload:** Set `reload=True` for development mode

### Environment Variables

- `FRONTEND_DIST` - Path to frontend dist folder (optional)

## 🐛 Troubleshooting

### Issue: `NotImplementedError` when generating PDF

**Cause:** Using `uvicorn` directly on Windows with Python 3.13

**Solution:** Use `python run_server.py` instead

### Issue: Port 8000 already in use

**Solution:**
```bash
# Kill existing Python processes
Get-Process | Where-Object { $_.ProcessName -eq "python" } | Stop-Process -Force

# Then restart
python run_server.py
```

### Issue: Playwright browsers not found

**Solution:**
```bash
python -m playwright install chromium
```

## 📚 API Examples

### Generate PDF Report

```bash
curl -X POST http://localhost:8000/api/generate-pdf \
  -H "Content-Type: application/json" \
  -d '{
    "reaction_name": "Synthesis of Aspirin",
    "product": {
      "name": "aspirin",
      "mw": 180.16,
      "actual_mass_g": 10.0
    },
    "reactants": [
      {
        "name": "salicylic acid",
        "mw": 138.12,
        "mass_g": 12.0
      }
    ],
    "atom_economy_pct": 85.5,
    "pmi": 2.5,
    "e_factor": 1.5
  }'
```

### Compute All Metrics

```bash
curl -X POST http://localhost:8000/api/impact/compute \
  -H "Content-Type: application/json" \
  -d '{
    "product": {
      "mw": 180.16,
      "actual_mass_g": 10.0
    },
    "reactants": [
      {
        "mw": 138.12,
        "mass_g": 12.0
      }
    ]
  }'
```

## 🔐 Security Notes

- CORS is currently set to allow all origins (`allow_origins=["*"]`)
- For production, restrict CORS to specific domains
- Consider adding authentication for sensitive endpoints

## 📝 License

[Your License Here]

## 🤝 Contributing

[Your Contributing Guidelines Here]

---

**Version:** 1.0.0  
**Last Updated:** October 3, 2025
