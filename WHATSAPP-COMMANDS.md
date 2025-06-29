# WhatsApp Glass Bot Commands Guide

This guide explains all the available commands for the WhatsApp Glass Bot that integrates with your Google Sheets.

## 📋 View Orders Commands

### `/pending`
Shows all orders in the **Pending** tab with detailed information including dates.

**Example Output:**
```
📋 Pending Tab - 3 orders
========================================

🆔 Order ID: 123456
👤 Client: John Doe
📝 Specs: 10mm Clear Glass
📏 Items:
  • 2000x1000 - Qty: 2
  • 1500x750 - Qty: 1
📅 Created: 2024-01-15 10:30:00
📌 Notes: Urgent order

------------------------------
```

### `/ready`
Shows all orders in the **Ready** tab with delivery dates.

### `/delivered`
Shows all orders in the **Delivered** tab with delivery dates.

### `/completed`
Shows all orders in the **Completed** tab with completion dates.

### `/all`
Shows a summary of all tabs with order counts.

**Example Output:**
```
📊 Order Summary - All Tabs
==============================

⏳ Pending: 5 orders
✅ Ready: 3 orders
🚚 Delivered: 2 orders
🎉 Completed: 8 orders

💡 Use /pending, /ready, /delivered, or /completed to see detailed orders.
```

## 🔍 Search & Status Commands

### `/search [search_term]`
Searches for orders across all tabs by:
- Order ID
- Client name
- Glass specifications

**Examples:**
- `/search John Doe` - Find all orders for client "John Doe"
- `/search 123456` - Find order with ID "123456"
- `/search glass` - Find orders with "glass" in specifications

### `/status [client_name_or_order_id]`
Finds the current status of a specific order or client.

**Examples:**
- `/status John Doe` - Find status of orders for "John Doe"
- `/status 123456` - Find status of order "123456"

## 🔄 Update Orders Commands

### `/update [order_id] [status]`
Updates an order's status and automatically moves it to the appropriate tab.

**Available Statuses:**
- `Pending`
- `Ready`
- `Delivered`
- `Completed`

**Examples:**
- `/update 123456 Ready` - Move order 123456 to Ready tab
- `/update 789012 Delivered` - Move order 789012 to Delivered tab
- `/update 345678 Completed` - Move order 345678 to Completed tab

**Success Response:**
```
✅ Order 123456 status updated to Ready and moved to Ready tab.
```

## 📝 Adding New Orders

To add a new order, simply send the order details as text (no command needed):

```
Client Name: John Doe
Glass Specifications: 10mm Clear Glass
Sizes: 2000x1000
Quantity: 2
Notes: Urgent order for office
```

**Success Response:**
```
✅ Order added successfully!

Client: John Doe
Order ID: 123456
```

## 🆘 Help Commands

### `/help`
Shows comprehensive help with all available commands.

### `/update` (without parameters)
Shows help for the update command.

### `/search` (without parameters)
Shows help for the search command.

## 📊 Data Format

All order data includes:
- **Order ID**: Unique identifier
- **Client Name**: Customer name
- **Specifications**: Glass type and details
- **Sizes**: Dimensions of glass pieces
- **Quantity**: Number of pieces
- **Created Date**: When order was placed
- **Updated Date**: When status was last changed
- **Notes**: Additional information

## 🎯 Tab Workflow

1. **Pending** (Default) - New orders automatically go here
2. **Ready** - Orders that are ready for delivery
3. **Delivered** - Orders that have been delivered
4. **Completed** - Orders that are fully completed

Orders automatically move between tabs when you update their status using `/update`.

## 💡 Tips

- Use `/all` to get a quick overview of all tabs
- Use `/search` to find specific orders across all tabs
- Orders with multiple sizes/quantities are grouped together
- All dates are shown in your local timezone
- Use `/help` anytime to see all available commands

## 🔧 Troubleshooting

If a command doesn't work:
1. Check that you're using the correct syntax
2. Ensure the order ID exists
3. Use `/help` to see the correct command format
4. Contact support if issues persist

## 📱 WhatsApp Formatting

The bot uses WhatsApp's markdown formatting:
- `*bold text*` for headers
- Emojis for visual organization
- Clear separators between orders
- Structured layout for easy reading 