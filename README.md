# Green Chemistry Toolkit Backend

FastAPI backend for the Green Chemistry Toolkit.

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

### Running the Server

### Running the Server

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

**Alternative: Direct Uvicorn**
```bash
uvicorn main:app --reload
```


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

#### Web Pages
- `GET /` - Home page
- `GET /simulate` - Simulation interface
- `GET /tools` - Tools & calculators
- `GET /gamification` - Gamification page



## 🏗️ Project Structure

```
green-toolkit-backend/
├── main.py                 # FastAPI application and endpoints
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

### Issue: Port 8000 already in use

**Solution:**
```bash
# Kill existing Python processes
Get-Process | Where-Object { $_.ProcessName -eq "python" } | Stop-Process -Force

# Then restart
python run_server.py
```



## 📚 API Examples

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
