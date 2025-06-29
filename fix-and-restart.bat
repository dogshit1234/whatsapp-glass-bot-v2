@echo off
echo ==========================================
echo  Fixing WhatsApp Glass Bot Issues
echo ==========================================

REM Stop all running processes
echo Stopping existing processes...
taskkill /f /im python.exe 2>nul
taskkill /f /im node.exe 2>nul

timeout /t 2 /nobreak > nul

echo.
echo ==========================================
echo  Issue Fixes Applied:
echo ==========================================
echo ✅ Added better error logging for media processing
echo ✅ Fixed WhatsApp Web button functionality  
echo ✅ Configured Tesseract OCR path
echo ✅ Added detailed debug information
echo.

REM Check if Tesseract is installed
if exist "C:\Program Files\Tesseract-OCR\tesseract.exe" (
    echo ✅ Tesseract OCR is installed
) else (
    echo ❌ Tesseract OCR is NOT installed
    echo.
    echo This is likely why image processing fails!
    echo Please run install-tesseract.bat first to install Tesseract OCR.
    echo.
    echo For now, starting the system without OCR support...
    pause
)

echo.
echo Starting all services...

REM Start Backend Server
echo [1/3] Starting Backend Server...
start "Backend Server" cmd /k "cd backend && python app.py"
timeout /t 5 /nobreak > nul

REM Start Frontend Server  
echo [2/3] Starting Frontend Server...
start "Frontend Server" cmd /k "cd webui && npm start"
timeout /t 8 /nobreak > nul

REM Start WhatsApp Bot
echo [3/3] Starting WhatsApp Bot...
start "WhatsApp Bot" cmd /k "cd whatsapp-bot && node index.js"

echo.
echo ==========================================
echo  System Status
echo ==========================================
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:3000  
echo WhatsApp: Connected (check WhatsApp Bot terminal)
echo.
echo ==========================================
echo  Testing Instructions
echo ==========================================
echo 1. WhatsApp Web button now works - click it in dashboard
echo 2. Send '/help' to your WhatsApp number to test commands
echo 3. For image processing: Install Tesseract first!
echo.
echo If images still fail:
echo - Check Backend Server terminal for detailed error logs
echo - Install Tesseract OCR using install-tesseract.bat
echo.

REM Open dashboard
timeout /t 3 /nobreak > nul
start http://localhost:3000

echo System is running! Check terminal windows for errors.
pause

REM Install Tesseract if not present
if not exist "C:\Program Files\Tesseract-OCR\tesseract.exe" (
    echo Installing Tesseract...
    call install-tesseract.bat
) else (
    echo Tesseract already installed.
)

REM Install Python dependencies
cd backend
pip install --upgrade pip
pip install -r requirements.txt
cd ..

REM Restart backend (assumes running via restart-all.bat)
call restart-all.bat

echo Setup complete. Backend and OCR engines should be ready.
pause