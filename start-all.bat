@echo off
setlocal enabledelayedexpansion

echo ==========================================
echo  WhatsApp Glass Bot - Complete Startup
echo ==========================================
echo.

REM Set title for the window
title WhatsApp Glass Bot - Starting...

REM Check if required directories exist
echo [1/6] Checking directories...
if not exist "backend" (
    echo ❌ ERROR: Backend directory not found!
    echo Please ensure you're running this from the project root directory.
    pause
    exit /b 1
)
if not exist "whatsapp-bot" (
    echo ❌ ERROR: WhatsApp bot directory not found!
    echo Please ensure you're running this from the project root directory.
    pause
    exit /b 1
)
echo ✅ Directories found

REM Check Python installation
echo.
echo [2/6] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.7+ and add it to your PATH.
    pause
    exit /b 1
)
echo ✅ Python found

REM Check Node.js installation
echo.
echo [3/6] Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Node.js is not installed or not in PATH!
    echo Please install Node.js and add it to your PATH.
    pause
    exit /b 1
)
echo ✅ Node.js found

REM Install Python dependencies
echo.
echo [4/6] Installing Python dependencies...
cd backend
echo Installing backend requirements...
pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ ERROR: Failed to install Python dependencies!
    echo Please check your internet connection and try again.
    cd ..
    pause
    exit /b 1
)
cd ..
echo ✅ Python dependencies installed

REM Install Node.js dependencies
echo.
echo [5/6] Installing Node.js dependencies...
cd whatsapp-bot
echo Installing WhatsApp bot dependencies...
npm install
if errorlevel 1 (
    echo ❌ ERROR: Failed to install Node.js dependencies!
    echo Please check your internet connection and try again.
    cd ..
    pause
    exit /b 1
)
cd ..
echo ✅ Node.js dependencies installed

REM Stop any existing processes
echo.
echo [6/6] Stopping existing processes...
taskkill /f /im python.exe 2>nul
taskkill /f /im node.exe 2>nul
taskkill /f /im npm.exe 2>nul
timeout /t 2 /nobreak >nul

echo.
echo ==========================================
echo  Starting Services
echo ==========================================

REM Start Backend Server
echo [1/2] Starting Backend Server...
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
echo [2/2] Starting WhatsApp Bot...
start "WhatsApp Bot" cmd /k "cd whatsapp-bot && node index.js"

echo.
echo ==========================================
echo  🎉 System Started Successfully!
echo ==========================================
echo.
echo 📊 Service Status:
echo   • Backend API: http://localhost:5000 ✅
echo   • WhatsApp Bot: Starting... ⏳
echo.
echo 📱 Next Steps:
echo   1. Check the "WhatsApp Bot" terminal window
echo   2. Scan the QR code with your WhatsApp
echo   3. Test commands: /help, /pending, /ready, etc.
echo.
echo 💡 Available Commands:
echo   • /help - Show all commands
echo   • /pending - Show pending orders
echo   • /ready - Show ready orders
echo   • /delivered - Show delivered orders
echo   • /completed - Show completed orders
echo   • /all - Show summary of all tabs
echo   • /search [term] - Search orders
echo   • /update [id] [status] - Update order status
echo.
echo 🔧 Troubleshooting:
echo   • If backend fails: Check the "Backend Server" terminal
echo   • If WhatsApp fails: Check the "WhatsApp Bot" terminal
echo   • Run verify_setup.py to check system status
echo.
echo ==========================================
echo  System is now running!
echo  Keep all terminal windows open.
echo  Close this window when you want to stop all services.
echo ==========================================

REM Keep this window open
echo.
echo Press any key to open the verification script...
pause >nul

REM Run verification script
echo Running system verification...
python verify_setup.py

echo.
echo Press any key to exit...
pause >nul