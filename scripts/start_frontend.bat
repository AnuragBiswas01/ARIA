@echo off
echo Starting ARIA Frontend...
cd /d "%~dp0..\frontend"
call npm run dev
