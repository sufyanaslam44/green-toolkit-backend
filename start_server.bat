@echo off
REM Start FastAPI server

echo ========================================
echo Starting Green Toolkit Backend Server
echo ========================================
echo.
echo Platform: Windows
echo Python: 3.13+
echo.

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

echo Starting server...
echo.

REM Start server using the startup script
python run_server.py

pause
