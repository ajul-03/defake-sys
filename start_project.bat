@echo off
title Deepfake Detection System Launcher
echo ===================================================
echo   STARTING DEEPFAKE DETECTION SYSTEM
echo ===================================================

echo.
echo [1/3] Starting Backend Server (Python/Flask)...
echo     - Creating/Activating Virtual Environment
echo     - Installing Dependencies
echo     - Starting Server on Port 5000
start "Backend Server" cmd /k "cd backend && call .\venv_gpu\Scripts\activate.bat && python app.py"

echo.
echo [2/3] Starting Frontend Server (React/Vite)...
echo     - Installing Node Modules
echo     - Starting Server on Port 5173
start "Frontend Server" cmd /k "cd frontend && npm install && npm run dev"

echo.
echo [3/3] Waiting for servers to initialize...
echo     - Browser will open automatically in 15 seconds.
timeout /t 15 >nul

echo.
echo [SUCCESS] Opening Application...
start http://localhost:5173

echo.
echo Done! You can minimize this window, but DO NOT CLOSE the other two terminal windows.
pause
