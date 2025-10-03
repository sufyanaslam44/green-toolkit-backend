# Start FastAPI server with Windows compatibility for Playwright

Write-Host "========================================" -ForegroundColor Green
Write-Host "Starting Green Toolkit Backend Server" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Platform: Windows" -ForegroundColor Cyan
Write-Host "Python: 3.13+" -ForegroundColor Cyan
Write-Host "Playwright: Enabled" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists and activate
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & "venv\Scripts\Activate.ps1"
}

Write-Host "Starting server..." -ForegroundColor Yellow
Write-Host ""

# Start server using the startup script
python run_server.py
