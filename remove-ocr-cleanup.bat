@echo off
echo ========================================
echo WhatsApp Bot - OCR Removal Cleanup
echo ========================================
echo.
echo This script will:
echo 1. Remove old uploaded images
echo 2. Remove OCR pipeline file
echo 3. Clean up dependencies
echo 4. Update Node.js dependencies
echo.

echo Step 1: Removing old uploaded images...
del /q "whatsapp-bot\wa_upload_*.jpeg" 2>nul
del /q "whatsapp-bot\wa_upload_*.jpg" 2>nul
del /q "whatsapp-bot\wa_upload_*.png" 2>nul
echo Old images removed.

echo.
echo Step 2: Removing OCR pipeline file...
del /q "backend\ocr_pipeline.py" 2>nul
echo OCR pipeline removed.

echo.
echo Step 3: Updating backend dependencies...
cd backend
pip uninstall -y opencv-python pytesseract surya-ocr transformers torch torchvision torchaudio Pillow requests
pip install -r requirements.txt
cd ..

echo.
echo Step 4: Updating WhatsApp bot dependencies...
cd whatsapp-bot
npm uninstall form-data
npm install
cd ..

echo.
echo ========================================
echo Cleanup Complete!
echo ========================================
echo.
echo Your bot now handles TEXT INPUT ONLY:
echo - Send text messages with order details
echo - Use commands like /query and /update
echo - Images will be rejected with helpful message
echo.
echo Next steps:
echo 1. Start your bot with 'start-all.bat'
echo 2. Test by sending a text message like:
echo    "Client: John Doe, Product: Glass panels, Quantity: 5"
echo.
pause