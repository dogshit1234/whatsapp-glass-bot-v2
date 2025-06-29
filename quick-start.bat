@echo off
echo ==========================================
echo  WhatsApp Glass Bot - Quick Start
echo ==========================================
echo.

REM Stop any existing processes
echo Stopping existing processes...
taskkill /f /im python.exe 2>nul
taskkill /f /im node.exe 2>nul
taskkill /f /im npm.exe 2>nul
timeout /t 2 /nobreak >nul

echo Starting services...

REM Start Backend Server
echo [1/2] Starting Backend Server...
start "Backend Server" cmd /k "cd backend && python app.py"
timeout /t 3 /nobreak >nul

REM Start WhatsApp Bot
echo [2/2] Starting WhatsApp Bot...
start "WhatsApp Bot" cmd /k "cd whatsapp-bot && node index.js"

echo.
echo ==========================================
echo  🚀 System Started!
echo ==========================================
echo.
echo 📱 Next Steps:
echo   1. Check the "WhatsApp Bot" terminal window
echo   2. Scan the QR code with your WhatsApp
echo   3. Test commands: /help, /pending, /ready, etc.
echo.
echo 💡 Quick Commands:
echo   • /help - Show all commands
echo   • /all - Show summary of all tabs
echo   • /pending - Show pending orders
echo.
echo ==========================================
echo  System is running! Keep terminal windows open.
echo ==========================================

pause 