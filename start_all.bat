@echo off
echo ============================================================
echo   Launching AutoPace (Resilient Academic Workload OS)
echo ============================================================
echo.
echo 1. Starting Backend Server in background window...
start "AutoPace Backend" cmd /k "start_backend.bat"

echo 2. Starting Frontend Dev Server in background window...
start "AutoPace Frontend" cmd /k "start_frontend.bat"

echo.
echo All services launched!
echo - API Docs: http://127.0.0.1:8000/docs
echo - Web App:  http://localhost:5173
echo.
pause
