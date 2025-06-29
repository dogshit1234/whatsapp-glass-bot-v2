# WhatsApp Glass Bot v2 - Setup Instructions

## Overview
This is a simplified WhatsApp bot that processes glass orders and stores them directly in Google Sheets. No web UI - just WhatsApp messages and Google Sheets integration.

## Quick Setup

### 1. Google Cloud Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google Sheets API and Google Drive API
4. Create a Service Account:
   - Go to "IAM & Admin" > "Service Accounts"
   - Click "Create Service Account"
   - Download the JSON credentials file
   - Rename it to `google-credentials.json` and place it in the `backend/` folder

### 2. Google Sheets Setup
1. Create a new Google Sheet
2. Share it with the service account email (found in the credentials JSON)
3. Note the Sheet ID from the URL (the long string between /d/ and /edit)

### 3. Google Apps Script Setup
1. Go to [Google Apps Script](https://script.google.com/)
2. Create a new project
3. Copy the entire content from `app script.txt` into the script editor
4. Update the `SPREADSHEET_ID` constant with your actual Sheet ID
5. Deploy as a Web App:
   - Click "Deploy" > "New deployment"
   - Choose "Web app"
   - Set access to "Anyone"
   - Copy the Web App URL

### 4. Environment Setup
1. **Backend Environment:**
   - Ensure `google-credentials.json` is in the `backend/` folder
   - Set environment variables if needed (or use defaults)

2. **WhatsApp Bot Environment:**
   - Create `.env` file in `whatsapp-bot/` folder:
   ```
   BACKEND_API_URL=http://localhost:5000
   ```

### 5. Install Dependencies
1. **Backend:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **WhatsApp Bot:**
   ```bash
   cd whatsapp-bot
   npm install
   ```

## Running the System

### Option 1: Quick Start (Windows)
```bash
start-all.bat
```

### Option 2: Manual Start
1. **Start Backend:**
   ```bash
   cd backend
   python app.py
   ```

2. **Start WhatsApp Bot:**
   ```bash
   cd whatsapp-bot
   node index.js
   ```

3. **Scan QR Code:**
   - When the WhatsApp bot starts, it will display a QR code
   - Scan it with your WhatsApp Business app

### Option 3: Docker
```bash
docker-compose up --build
```

## Usage

### Sending Orders via WhatsApp
Send text messages like:
```
Client: John Doe
Product: Glass panels
Quantity: 5
Size: 100x200cm
Notes: Tempered glass
```

### Using Commands
- `/query` - Search for orders
- `/update` - Update order status

### Google Sheets Management
- Orders are automatically added to the "Pending" sheet
- Use the Google Apps Script to move orders between status sheets
- All data is stored in Google Sheets for easy management

## Troubleshooting

### Common Issues
1. **Google Sheets Access Error:**
   - Ensure the service account email has access to your Google Sheet
   - Check that `google-credentials.json` is in the correct location

2. **WhatsApp Bot Not Connecting:**
   - Make sure to scan the QR code with WhatsApp Business app
   - Check that the backend is running on port 5000

3. **Orders Not Being Added:**
   - Check backend logs for errors
   - Verify Google Apps Script is deployed and accessible
   - Ensure the Sheet ID is correct in the Apps Script

### Logs
- Backend logs: Check the backend terminal window
- WhatsApp bot logs: Check the WhatsApp bot terminal window
- Google Apps Script logs: Check the Apps Script execution logs

## Support
If you encounter issues:
1. Check all terminal windows for error messages
2. Verify all setup steps were completed correctly
3. Ensure all services are running (backend and WhatsApp bot) 