# WhatsApp Glass Bot v2

## Overview
A WhatsApp bot for managing glass orders with direct Google Sheets integration. No web UI - just WhatsApp messages and Google Sheets.

---

## Features
- WhatsApp bot with text-based order processing
- Google Sheets as database
- Slash commands for querying and updating orders
- Dockerized for easy deployment
- Simple and focused functionality

---

## Setup Instructions

### 1. Clone the repository
```sh
git clone <your-repo-url>
cd whatsapp-glass-bot-v2
```

### 2. Google Cloud Setup
- Create a Google Cloud project
- Enable Google Sheets & Drive API
- Create a Service Account, download `google-credentials.json` and place it in `backend/`
- Share your Google Sheet (e.g., `WhatsApp Glass Bot Orders`) with the service account email
- Deploy the Google Apps Script from `app script.txt` to your Google account

### 3. Environment Variables
- **Backend:** Set `GOOGLE_CREDS`, `SHEET_NAME` as needed
- **WhatsApp Bot:** Set `BACKEND_API_URL` in `whatsapp-bot/.env`

### 4. Local Development
- **Backend:**
  ```sh
  cd backend
  pip install -r requirements.txt
  python app.py
  ```
- **WhatsApp Bot:**
  ```sh
  cd whatsapp-bot
  npm install
  node index.js
  ```

### 5. Docker Deployment
```sh
docker-compose up --build
```

### 6. Quick Start (Windows)
```sh
start-all.bat
```

---

## Usage

### WhatsApp Commands
- Send order details as text:
  ```
  Client: John Doe
  Product: Glass panels
  Quantity: 5
  Size: 100x200cm
  Notes: Tempered glass
  ```

- Use slash commands:
  - `/query` - Search orders
  - `/update` - Update order status

### Google Sheets
- Orders are automatically added to the "Pending" sheet
- Use the Google Apps Script to move orders between sheets (Pending → Ready → Delivered → Completed)
- All order data is stored in Google Sheets

---

## API Endpoints
- `/api/health` (GET): Health check
- `/api/whatsapp_in` (POST): WhatsApp bot integration
- `/api/orders` (GET): List all orders (for debugging)

---

## Troubleshooting
- Ensure Google Sheet is shared with the service account
- Ensure Google Apps Script is deployed and accessible
- Check backend and bot logs for errors
- Make sure WhatsApp QR code is scanned in the bot terminal

---

## License
MIT 