@echo off
echo ========================================
echo        Starting ARIA System
echo ========================================
echo.

:: Create data directories if they don't exist
if not exist "..\data\memory" mkdir ..\data\memory
if not exist "..\data\logs" mkdir ..\data\logs

:: Start Backend in a new window
echo Starting Backend...
start "ARIA Backend" cmd /k "%~dp0start_backend.bat"

:: Wait a moment for backend to initialize
timeout /t 3 /nobreak > nul

:: Start Frontend in a new window
echo Starting Frontend...
start "ARIA Frontend" cmd /k "%~dp0start_frontend.bat"

echo.
echo ========================================
echo ARIA is starting!
echo - Backend: http://localhost:8000
echo - Frontend: http://localhost:5173
echo - API Docs: http://localhost:8000/docs
echo ========================================
echo.
pause
