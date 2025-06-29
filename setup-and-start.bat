@echo off
setlocal enabledelayedexpansion

echo ==========================================
echo  WhatsApp Glass Bot - Complete Setup & Start
echo ==========================================
echo.

title WhatsApp Glass Bot - Setup & Start

echo This script will:
echo 1. Check system requirements
echo 2. Install dependencies
echo 3. Verify Google Apps Script setup
echo 4. Start all services
echo.

set /p continue="Do you want to continue? (Y/N): "
if /i not "%continue%"=="Y" (
    echo Setup cancelled.
    pause
    exit /b 0
)

echo.
echo ==========================================
echo  Step 1: System Requirements Check
echo ==========================================

REM Check Python
echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found!
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)
echo ✅ Python found

REM Check Node.js
echo Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js not found!
    echo Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)
echo ✅ Node.js found

echo.
echo ==========================================
echo  Step 2: Installing Dependencies
echo ==========================================

REM Install Python dependencies
echo Installing Python dependencies...
cd backend
pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install Python dependencies!
    cd ..
    pause
    exit /b 1
)
cd ..
echo ✅ Python dependencies installed

REM Install Node.js dependencies
echo Installing Node.js dependencies...
cd whatsapp-bot
npm install
if errorlevel 1 (
    echo ❌ Failed to install Node.js dependencies!
    cd ..
    pause
    exit /b 1
)
cd ..
echo ✅ Node.js dependencies installed

echo.
echo ==========================================
echo  Step 3: Starting Services
echo ==========================================

REM Stop any existing processes
echo Stopping existing processes...
taskkill /f /im python.exe 2>nul
taskkill /f /im node.exe 2>nul
timeout /t 2 /nobreak >nul

REM Start Backend
echo Starting Backend Server...
start "Backend Server" cmd /k "cd backend && python app.py"
timeout /t 5 /nobreak >nul

REM Start WhatsApp Bot
echo Starting WhatsApp Bot...
start "WhatsApp Bot" cmd /k "cd whatsapp-bot && node index.js"

echo.
echo ==========================================
echo  🎉 Setup Complete & System Started!
echo ==========================================
echo.
echo 📱 Next Steps:
echo   1. Check the "WhatsApp Bot" terminal window
echo   2. Scan the QR code with your WhatsApp
echo   3. Test the system with: /help
echo.
echo 💡 Test Commands:
echo   • /help - Show all commands
echo   • /all - Show summary of all tabs
echo   • /pending - Show pending orders
echo.
echo ==========================================
echo  System is now running!
echo ==========================================

pause 