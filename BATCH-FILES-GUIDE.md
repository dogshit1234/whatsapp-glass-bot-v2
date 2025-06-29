# WhatsApp Glass Bot - Batch Files Guide

This guide explains all the available batch files for managing your WhatsApp Glass Bot system.

## 🚀 Quick Start Options

### **First Time Setup**
- **`setup-and-start.bat`** - Complete setup for first-time users
  - Checks system requirements (Python, Node.js)
  - Installs all dependencies
  - Starts all services
  - Best for new installations

### **Regular Usage**
- **`start-all.bat`** - Complete startup with verification
  - Checks dependencies and installs if needed
  - Verifies system health
  - Starts all services
  - Runs verification script
  - Best for daily use

- **`quick-start.bat`** - Fast startup for experienced users
  - Assumes dependencies are already installed
  - Starts services quickly
  - Best for regular users

## 🔄 Management Commands

### **Restart Services**
- **`restart-all.bat`** - Restart all services
  - Stops all running processes
  - Starts services fresh
  - Runs verification
  - Best when you need a clean restart

### **Stop Services**
- **`stop-all.bat`** - Stop all services
  - Cleanly stops all processes
  - No restart - just stops everything
  - Best when you're done using the system

## 📋 Detailed File Descriptions

### `setup-and-start.bat`
**Purpose:** Complete first-time setup and start
**When to use:** First time installing the system
**Features:**
- ✅ Checks Python and Node.js installation
- ✅ Installs Python dependencies
- ✅ Installs Node.js dependencies
- ✅ Starts backend and WhatsApp bot
- ✅ Interactive setup process

### `start-all.bat`
**Purpose:** Complete startup with full verification
**When to use:** Daily startup or after system changes
**Features:**
- ✅ Checks system requirements
- ✅ Installs/updates dependencies
- ✅ Waits for backend to be ready
- ✅ Starts WhatsApp bot
- ✅ Runs verification script
- ✅ Comprehensive error handling

### `quick-start.bat`
**Purpose:** Fast startup for experienced users
**When to use:** Regular daily use when system is already set up
**Features:**
- ✅ Stops existing processes
- ✅ Starts services quickly
- ✅ Minimal checks
- ✅ Fast execution

### `restart-all.bat`
**Purpose:** Clean restart of all services
**When to use:** When services are having issues or need refresh
**Features:**
- ✅ Stops all processes cleanly
- ✅ Waits for processes to fully stop
- ✅ Starts services fresh
- ✅ Verifies backend is ready
- ✅ Runs verification script

### `stop-all.bat`
**Purpose:** Stop all running services
**When to use:** When you're done using the system
**Features:**
- ✅ Stops Python processes (backend)
- ✅ Stops Node.js processes (WhatsApp bot)
- ✅ Stops npm processes
- ✅ Clean shutdown

## 🎯 Usage Scenarios

### **First Time Setup**
```bash
# Run the complete setup
setup-and-start.bat
```

### **Daily Startup**
```bash
# For regular use (recommended)
start-all.bat

# For quick startup (if already set up)
quick-start.bat
```

### **Troubleshooting**
```bash
# If services are having issues
restart-all.bat

# If you need to stop everything
stop-all.bat
```

### **Development/Testing**
```bash
# Quick restart during development
restart-all.bat

# Stop before making changes
stop-all.bat
```

## 🔧 What Each File Does

### **System Checks**
- Python installation and version
- Node.js installation and version
- Required directories existence
- Dependencies installation

### **Service Management**
- Backend server (Python Flask)
- WhatsApp bot (Node.js)
- Process cleanup
- Health verification

### **Error Handling**
- Graceful failure messages
- Dependency installation errors
- Service startup failures
- Network connectivity issues

## 📊 Service Status Indicators

The batch files show status with emojis:
- ✅ Success/Ready
- ❌ Error/Failed
- ⏳ In Progress/Waiting
- 🔄 Restarting
- 🛑 Stopped

## 💡 Tips for Best Experience

1. **Use `start-all.bat` for daily use** - It includes verification and error handling
2. **Use `restart-all.bat` for issues** - Clean restart often fixes problems
3. **Keep terminal windows open** - Services need to stay running
4. **Check verification output** - Helps identify any issues
5. **Use `stop-all.bat` when done** - Clean shutdown prevents conflicts

## 🚨 Troubleshooting

### **If services won't start:**
1. Run `stop-all.bat` to clean up
2. Run `start-all.bat` for fresh start
3. Check terminal windows for error messages

### **If dependencies are missing:**
1. Run `setup-and-start.bat` for complete setup
2. Ensure Python and Node.js are installed
3. Check internet connection for downloads

### **If WhatsApp bot won't connect:**
1. Check the "WhatsApp Bot" terminal window
2. Scan QR code if needed
3. Ensure backend is running (check "Backend Server" window)

## 📱 After Starting Services

Once services are running:
1. Check the "WhatsApp Bot" terminal window
2. Scan QR code with your WhatsApp
3. Test with `/help` command
4. Try `/all` to see order summary
5. Use other commands as needed

## 🔄 Integration with WhatsApp Commands

The batch files work with all the WhatsApp commands:
- `/help` - Show all commands
- `/pending` - Show pending orders
- `/ready` - Show ready orders
- `/delivered` - Show delivered orders
- `/completed` - Show completed orders
- `/all` - Show summary of all tabs
- `/search [term]` - Search orders
- `/update [id] [status]` - Update order status 