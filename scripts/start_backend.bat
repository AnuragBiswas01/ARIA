@echo off
echo Starting ARIA Backend...
cd /d "%~dp0..\backend"
call .venv\Scripts\activate.bat
python main.py
