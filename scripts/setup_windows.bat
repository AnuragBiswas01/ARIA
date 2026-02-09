@echo off
echo ========================================
echo    ARIA - Backend Setup (Windows)
echo ========================================

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.11+
    pause
    exit /b 1
)

:: Create virtual environment
if not exist "backend\.venv" (
    echo Creating virtual environment...
    cd backend
    python -m venv .venv
    cd ..
)

:: Activate venv and install dependencies
echo Installing backend dependencies...
call backend\.venv\Scripts\activate.bat
pip install -r backend\requirements.txt

:: Create data directories
if not exist "data\memory" mkdir data\memory
if not exist "data\logs" mkdir data\logs

echo.
echo Setup complete! Run start_all.bat to launch ARIA.
pause
