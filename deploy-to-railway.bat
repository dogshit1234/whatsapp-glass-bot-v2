@echo off
echo ========================================
echo   WhatsApp Glass Bot - Railway Setup
echo ========================================
echo.

echo Step 1: Prepare Google Credentials
echo ----------------------------------
echo 1. Open your google-credentials.json file
echo 2. Copy the entire content
echo 3. You'll paste this in Railway environment variables
echo.

echo Step 2: Deploy to Railway
echo -------------------------
echo 1. Go to https://railway.app
echo 2. Sign up with GitHub
echo 3. Create new project
echo 4. Connect your GitHub repository
echo 5. Set root directory to 'backend' for backend service
echo 6. Set root directory to 'whatsapp-bot' for WhatsApp bot service
echo.

echo Step 3: Set Environment Variables
echo --------------------------------
echo In Railway, add these environment variables:
echo.
echo For Backend Service:
echo - GOOGLE_CREDS: [paste your full JSON content]
echo - SHEET_NAME: [your sheet name]
echo - APPS_SCRIPT_URL: [your apps script URL]
echo - PORT: 5000
echo.
echo For WhatsApp Bot Service:
echo - BACKEND_API_URL: [your backend Railway URL]
echo.

echo Step 4: Deploy
echo --------------
echo 1. Railway will auto-deploy when you push to GitHub
echo 2. Or click "Deploy Now" in Railway
echo 3. Get your backend URL from Railway
echo 4. Update BACKEND_API_URL in WhatsApp bot service
echo.

echo ========================================
echo   Setup Complete!
echo ========================================
pause 