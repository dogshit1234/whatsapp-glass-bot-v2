@echo off
setlocal enabledelayedexpansion

echo ==========================================
echo  WhatsApp Glass Bot - Restart All Services
echo ==========================================
echo.

title WhatsApp Glass Bot - Restarting...

REM Stop existing processes
echo [1/4] Stopping existing processes...
taskkill /f /im python.exe 2>nul
taskkill /f /im node.exe 2>nul
taskkill /f /im npm.exe 2>nul
echo ✅ Processes stopped

REM Wait for processes to fully stop
echo [2/4] Waiting for processes to stop...
timeout /t 3 /nobreak >nul

REM Start Backend Server
echo [3/4] Starting Backend Server...
start "Backend Server" cmd /k "cd backend && python app.py"
timeout /t 5 /nobreak >nul

REM Wait for backend to be ready
echo Waiting for backend to start...
:wait_backend
timeout /t 1 /nobreak >nul
curl -s http://localhost:5000/api/health >nul 2>&1
if errorlevel 1 (
    echo Still waiting for backend...
    goto wait_backend
)
echo ✅ Backend is ready

REM Start WhatsApp Bot
echo [4/4] Starting WhatsApp Bot...
start "WhatsApp Bot" cmd /k "cd whatsapp-bot && node index.js"

echo.
echo ==========================================
echo  🔄 All Services Restarted Successfully!
echo ==========================================
echo.
echo 📊 Service Status:
echo   • Backend API: http://localhost:5000 ✅
echo   • WhatsApp Bot: Starting... ⏳
echo.
echo 📱 Next Steps:
echo   1. Check the "WhatsApp Bot" terminal window
echo   2. Scan the QR code with your WhatsApp (if needed)
echo   3. Test commands: /help, /pending, /ready, etc.
echo.
echo 💡 Quick Test:
echo   Send /help to your WhatsApp to test the system
echo.
echo ==========================================
echo  System is now running!
echo  Keep all terminal windows open.
echo ==========================================

echo.
echo Press any key to run system verification...
pause >nul

REM Run verification
echo Running system verification...
python verify_setup.py

echo.
echo Press any key to exit...
pause >nul