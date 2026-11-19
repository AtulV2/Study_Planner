@echo off
echo ============================================================
echo   Launching Study Planner
echo ============================================================
echo.
echo 1. Starting Backend Server in background window...
start "Study Planner Backend" cmd /k "start_backend.bat"

echo 2. Starting Frontend Dev Server in background window...
start "Study Planner Frontend" cmd /k "start_frontend.bat"

echo.
echo All services launched!
echo - API Docs: http://127.0.0.1:8000/docs
echo - Web App:  http://localhost:5173
echo.
pause
