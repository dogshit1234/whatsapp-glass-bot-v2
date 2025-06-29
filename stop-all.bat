@echo off
echo ==========================================
echo  WhatsApp Glass Bot - Stop All Services
echo ==========================================
echo.

echo Stopping all WhatsApp Glass Bot services...

REM Stop Python processes (backend)
echo Stopping Backend Server...
taskkill /f /im python.exe 2>nul
if errorlevel 1 (
    echo ✅ No Python processes found
) else (
    echo ✅ Python processes stopped
)

REM Stop Node.js processes (WhatsApp bot)
echo Stopping WhatsApp Bot...
taskkill /f /im node.exe 2>nul
if errorlevel 1 (
    echo ✅ No Node.js processes found
) else (
    echo ✅ Node.js processes stopped
)

REM Stop npm processes
echo Stopping npm processes...
taskkill /f /im npm.exe 2>nul
if errorlevel 1 (
    echo ✅ No npm processes found
) else (
    echo ✅ npm processes stopped
)

echo.
echo ==========================================
echo  🛑 All Services Stopped Successfully!
echo ==========================================
echo.
echo All WhatsApp Glass Bot services have been stopped.
echo To restart, run start-all.bat or quick-start.bat
echo.
echo ==========================================

timeout /t 3 /nobreak >nul 