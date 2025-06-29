import requests
import pandas as pd
from datetime import datetime
import os
import random
import json

try:
    from app import GOOGLE_CREDS, SHEET_NAME
except ImportError:
    GOOGLE_CREDS = os.environ.get('GOOGLE_CREDS', 'google-credentials.json')
    SHEET_NAME = os.environ.get('SHEET_NAME', 'Pending')

# Google Apps Script Web App URL - Update this with your deployed web app URL
APPS_SCRIPT_URL = os.environ.get('APPS_SCRIPT_URL', '')

# Column mapping to match Google Apps Script structure
COLUMNS = [
    'ID', 'Client Name', 'Specifications', 'Sizes', 'Quantity', 'Status',
    'Notes', 'Created At', 'Updated At', 'Sync Status'
]

def call_apps_script(action, data=None):
    """Make a request to the Google Apps Script web app"""
    try:
        payload = {
            'action': action,
            'data': data or {}
        }
        
        response = requests.post(APPS_SCRIPT_URL, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        if not result.get('success'):
            raise Exception(f"Apps Script error: {result.get('message', 'Unknown error')}")
        
        return result
    except Exception as e:
        print(f"Error calling Apps Script ({action}): {e}")
        raise

def get_sheet():
    """Get orders from the default sheet (Pending)"""
    try:
        result = call_apps_script('getOrders')
        return result.get('data', [])
    except Exception as e:
        print(f"Error getting sheet data: {e}")
        return []

def format_date_only(dt_str):
    try:
        if not dt_str:
            return ''
        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        return dt.strftime('%d %B %Y')  # e.g., '28 June 2025'
    except Exception:
        return dt_str  # fallback to original if parsing fails

def get_tab_data(tab_name):
    """Get orders from a specific tab with formatted output (robust grouping for all sizes, no emojis)"""
    try:
        # Get orders from the specified tab
        result = call_apps_script('getOrdersFromSheet', {'sheetName': tab_name})
        orders = result.get('data', [])
        
        if not orders:
            return f"📋 *{tab_name} Tab*\nNo orders found in {tab_name} tab."
        
        # Try to get raw sheet data to capture rows without IDs
        try:
            raw_result = call_apps_script('getRawSheetData', {'sheetName': tab_name})
            raw_data = raw_result.get('data', [])
        except Exception as e:
            print(f"Error getting raw sheet data: {e}")
            raw_data = []

        # --- Robust grouping logic ---
        grouped_orders = {}
        current_id = None
        for row in raw_data:
            # Skip header row
            if not row or row[0] in ('ID', 'id'):
                continue
            row_id = row[0]
            client_name = row[1] if len(row) > 1 else ''
            specs = row[2] if len(row) > 2 else ''
            size = row[3] if len(row) > 3 else ''
            qty = row[4] if len(row) > 4 else ''
            status = row[5] if len(row) > 5 else ''
            notes = row[6] if len(row) > 6 else ''
            created_at = row[7] if len(row) > 7 else ''
            updated_at = row[8] if len(row) > 8 else ''

            # If this row has an ID, start a new order
            if row_id:
                current_id = row_id
                if current_id not in grouped_orders:
                    grouped_orders[current_id] = {
                        'id': current_id,
                        'clientName': client_name,
                        'specifications': specs,
                        'createdAt': created_at,
                        'updatedAt': updated_at,
                        'status': status,
                        'notes': notes,
                        'items': []
                    }
            # Only add items if we have a current order
            if current_id and (size or qty):
                # Normalize size for duplicate checking
                norm_size = str(size).strip().lower()
                already_exists = any(str(item['sizes']).strip().lower() == norm_size for item in grouped_orders[current_id]['items'])
                if size and qty and not already_exists:
                    grouped_orders[current_id]['items'].append({
                        'sizes': size,
                        'quantity': qty
                    })

        # Format output
        tab_display_names = {
            'Pending': 'Pending Orders',
            'Ready': 'Ready Orders', 
            'Delivered': 'Glass Delivered',
            'Completed': 'Completed Orders'
        }
        display_name = tab_display_names.get(tab_name, f"{tab_name} Orders")
        
        output = f"*{display_name} - {len(grouped_orders)} orders*\n"
        output += "*" + "=" * 40 + "*\n\n"
        for order_id, order in grouped_orders.items():
            output += f"*Order ID:* {order_id}\n"
            output += f"*Client:* {order['clientName']}\n"
            output += f"*Specs:* {order['specifications']}\n"
            # Add line items
            if order['items']:
                output += "*Glass Sizes:*\n"
                for item in order['items']:
                    if item['sizes'] and item['quantity']:
                        output += f"  • {item['sizes']} - Qty: {item['quantity']}\n"
            # Add dates (formatted)
            if order['createdAt']:
                output += f"*Created:* {format_date_only(order['createdAt'])}\n"
            # Only show Updated for non-Pending tabs
            if tab_name.lower() != 'pending' and order['updatedAt'] and order['updatedAt'] != order['createdAt']:
                output += f"*Updated:* {format_date_only(order['updatedAt'])}\n"
            # Only show Notes for Delivered tab
            if tab_name.lower() == 'delivered' and order['notes']:
                output += f"*Notes:* {order['notes']}\n"
            output += "\n*" + "-" * 30 + "*\n\n"
        return output
    except Exception as e:
        print(f"Error getting tab data for {tab_name}: {e}")
        return f"❌ Error retrieving {tab_name} data: {str(e)}"

def get_all_tabs_data():
    """Get summary data from all tabs"""
    try:
        tabs = ['Pending', 'Ready', 'Delivered', 'Completed']
        all_data = {}
        
        for tab in tabs:
            result = call_apps_script('getOrdersFromSheet', {'sheetName': tab})
            orders = result.get('data', [])
            # Count unique orders (by ID)
            unique_orders = set()
            for order in orders:
                if order.get('id'):
                    unique_orders.add(order.get('id'))
            all_data[tab] = len(unique_orders)
        
        # Format summary
        output = "📊 *Order Summary - All Tabs*\n"
        output += "=" * 30 + "\n\n"
        
        for tab, count in all_data.items():
            emoji = {
                'Pending': '⏳',
                'Ready': '✅',
                'Delivered': '🚚',
                'Completed': '🎉'
            }.get(tab, '📋')
            
            output += f"{emoji} *{tab}:* {count} orders\n"
        
        output += "\n💡 Use /pending, /ready, /delivered, or /completed to see detailed orders."
        
        return output
        
    except Exception as e:
        print(f"Error getting all tabs data: {e}")
        return f"❌ Error retrieving summary data: {str(e)}"

def search_all_tabs(search_term):
    """Search for orders across all tabs"""
    try:
        tabs = ['Pending', 'Ready', 'Delivered', 'Completed']
        all_orders = {}  # Dictionary to store all orders by tab
        raw_data_by_tab = {}  # Dictionary to store raw data by tab
        
        # First, collect all orders from all tabs
        for tab in tabs:
            result = call_apps_script('getOrdersFromSheet', {'sheetName': tab})
            orders = result.get('data', [])
            if orders:
                all_orders[tab] = orders
            
            # Try to get raw sheet data to capture rows without IDs
            try:
                raw_result = call_apps_script('getrawsheetdata', {'sheetName': tab})
                raw_data = raw_result.get('data', [])
                if raw_data:
                    raw_data_by_tab[tab] = raw_data
            except Exception as e:
                print(f"Error getting raw sheet data for {tab}: {e}")
                raw_data_by_tab[tab] = []
        
        # Find orders matching the search term and collect their IDs
        found_orders = {}
        found_order_ids = set()
        
        for tab, orders in all_orders.items():
            tab_found_orders = []
            for order in orders:
                # Search in ID, client name, and specifications
                searchable_text = f"{order.get('id', '')} {order.get('clientName', '')} {order.get('specifications', '')}".lower()
                if search_term.lower() in searchable_text:
                    order['source_tab'] = tab
                    tab_found_orders.append(order)
                    found_order_ids.add(order.get('id', ''))
            
            if tab_found_orders:
                found_orders[tab] = tab_found_orders
        
        if not found_orders:
            return f"🔍 *Search Results*\nNo orders found matching '{search_term}'"
        
        # Group by order ID
        grouped_orders = {}
        
        # For each found order ID, collect all sizes from all tabs
        for tab, orders in found_orders.items():
            for order in orders:
                order_id = order.get('id', '')
                if not order_id:  # Skip rows without an ID
                    continue
                
                # If this is a new order ID, initialize its entry
                if order_id not in grouped_orders:
                    grouped_orders[order_id] = {
                        'id': order_id,
                        'clientName': order.get('clientName', ''),
                        'specifications': order.get('specifications', ''),
                        'createdAt': order.get('createdAt', ''),
                        'updatedAt': order.get('updatedAt', ''),
                        'status': order.get('status', ''),
                        'notes': order.get('notes', ''),
                        'source_tab': tab,
                        'items': []
                    }
                
                # Add size/quantity if present
                size = order.get('sizes', '')
                qty = order.get('quantity', '')
                
                if size and qty:
                    # Check if this size is already in the items list
                    size_exists = False
                    for item in grouped_orders[order_id]['items']:
                        if item['sizes'] == size:
                            size_exists = True
                            break
                    
                    # Only add if this size isn't already in the items list
                    if not size_exists:
                        grouped_orders[order_id]['items'].append({
                            'sizes': size,
                            'quantity': qty
                        })
        
        # Process raw data to find additional sizes for found orders
        for tab, raw_data in raw_data_by_tab.items():
            if not raw_data:
                continue
                
            current_id = None
            for row in raw_data:
                # Skip header row
                if len(row) == 0 or row[0] == 'ID' or row[0] == 'id':
                    continue
                
                # Get values from the row
                row_id = row[0] if len(row) > 0 else ''
                size = row[3] if len(row) > 3 else ''  # SIZES column (index 3)
                qty = row[4] if len(row) > 4 else ''   # QUANTITY column (index 4)
                
                # If this row has an ID, update current_id
                if row_id:
                    current_id = row_id
                    continue  # Skip processing as we already handled rows with IDs
                
                # If we have a current ID and this row has size/quantity but no ID
                # AND the current ID is one of our found order IDs
                if current_id and current_id in found_order_ids and current_id in grouped_orders and (size or qty):
                    if size and qty:
                        # Check if this size is already in the items list
                        size_exists = False
                        for item in grouped_orders[current_id]['items']:
                            if item['sizes'] == size:
                                size_exists = True
                                break
                        
                        # Only add if this size isn't already in the items list
                        if not size_exists:
                            grouped_orders[current_id]['items'].append({
                                'sizes': size,
                                'quantity': qty
                            })
        
        # Format results
        output = f"*Search Results for '{search_term}'*\n"
        output += f"*Found {len(grouped_orders)} orders*\n"
        output += "*" + "=" * 40 + "*\n\n"
        
        for order_id, order in grouped_orders.items():
            tab_display_names = {
                'Pending': 'Pending Orders',
                'Ready': 'Ready Orders', 
                'Delivered': 'Glass Delivered',
                'Completed': 'Completed Orders'
            }
            display_name = tab_display_names.get(order['source_tab'], f"{order['source_tab']} Orders")
            
            output += f"*{display_name}*\n"
            output += f"*Order ID:* {order_id}\n"
            output += f"*Client:* {order['clientName']}\n"
            output += f"*Specs:* {order['specifications']}\n"
            
            if order['items']:
                output += "*Items:*\n"
                for item in order['items']:
                    if item['sizes'] and item['quantity']:
                        output += f"  • {item['sizes']} - Qty: {item['quantity']}\n"
            
            if order['createdAt']:
                output += f"*Created:* {format_date_only(order['createdAt'])}\n"
            if order['updatedAt'] and order['updatedAt'] != order['createdAt']:
                output += f"*Updated:* {format_date_only(order['updatedAt'])}\n"
            
            output += "\n*" + "-" * 30 + "*\n\n"
        
        return output
        
    except Exception as e:
        print(f"Error searching all tabs: {e}")
        return f"❌ Error searching orders: {str(e)}"

def show_help():
    """Show help message with all available commands"""
    help_text = """🤖 *WhatsApp Glass Bot Commands*

📋 *View Orders:*
• `/pending` - Show all pending orders
• `/ready` - Show all ready orders  
• `/delivered` - Show all delivered orders
• `/completed` - Show all completed orders
• `/all` - Show summary of all tabs

🔍 *Search & Status:*
• `/search [term]` - Search orders by ID, client name, or specs
• `/status [client/ID]` - Find specific order status

🔄 *Update Orders:*
• `/update [order_id] [status]` - Update order status
  Example: `/update 123456 Ready`

📝 *Add New Order:*
Just send your order details as text:
```
Client Name: John Doe
Glass Specifications: 10mm Clear Glass
Sizes: 2000x1000
Quantity: 2
```

💡 *Status Options:* Pending, Ready, Delivered, Completed
"""
    return help_text

def show_update_help():
    """Show help for update command"""
    return """🔄 *Update Order Status*

Usage: `/update [order_id] [status]`

Examples:
• `/update 123456 Ready`
• `/update 789012 Delivered`
• `/update 345678 Completed`

Available statuses: Pending, Ready, Delivered, Completed

💡 The order will automatically move to the appropriate tab.
"""

def show_search_help():
    """Show help for search command"""
    return """🔍 *Search Orders*

Usage: `/search [search_term]`

Examples:
• `/search John Doe` - Find orders for client "John Doe"
• `/search 123456` - Find order with ID "123456"
• `/search glass` - Find orders with "glass" in specifications

💡 Searches across all tabs (Pending, Ready, Delivered, Completed)
"""

def add_order(order_info):
    """Add a new order to the Pending sheet via Apps Script"""
    try:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        client_name = order_info.get('client_name', '')
        glass_specs = order_info.get('glass_specs', '')
        sizes = order_info.get('sizes', [])
        quantities = order_info.get('quantities', [])
        # Use invoice number as order ID if present, else generate random
        order_id = order_info.get('invoice_number') or str(random.randint(100000, 999999))
        
        # Prepare order data in Apps Script format
        orders = []
        
        # If there are no sizes or quantities, add a single row with just the client and specs
        if not sizes and not quantities:
            order_data = {
                'id': order_id,
                'clientName': client_name,
                'specifications': glass_specs,
                'sizes': '',
                'quantity': '',
                'status': 'Pending',
                'notes': '',
                'createdAt': now,
                'updatedAt': now
            }
            orders.append(order_data)
        else:
            # Add a row for each size/quantity pair
            for i in range(max(len(sizes), len(quantities))):
                size = sizes[i] if i < len(sizes) else ''
                qty = quantities[i] if i < len(quantities) else ''
                
                order_data = {
                    'id': order_id,  # Use invoice number or generated ID
                    'clientName': client_name,  # Include client name on every row
                    'specifications': glass_specs,  # Include specs on every row
                    'sizes': size,
                    'quantity': qty,
                    'status': 'Pending',
                    'notes': '',
                    'createdAt': now,
                    'updatedAt': now
                }
                orders.append(order_data)
        
        # Sync to Apps Script, always specify Pending as the target sheet
        result = call_apps_script('syncToSheets', {'orders': orders, 'targetSheetName': 'Pending'})
        return order_id
        
    except Exception as e:
        print(f"Error adding order: {e}")
        raise

def query_orders(query):
    """Query orders from the default sheet"""
    try:
        data = get_sheet()
        if not data:
            return 'No orders found.'
        
        # Filter based on query parameters
        filtered_data = data
        if 'status' in query:
            filtered_data = [order for order in filtered_data if order.get('status', '').lower() == query['status'].lower()]
        if 'client_name' in query:
            filtered_data = [order for order in filtered_data if query['client_name'].lower() in order.get('clientName', '').lower()]
        
        if not filtered_data:
            return 'No orders found matching the criteria.'
        
        # Return a summary string for WhatsApp
        summary = f"Found {len(filtered_data)} orders:\n"
        for order in filtered_data:
            summary += f"\nClient: {order.get('clientName', 'N/A')}\n"
            summary += f"Specs: {order.get('specifications', 'N/A')}\n"
            summary += f"Sizes: {order.get('sizes', 'N/A')}\n"
            summary += f"Qty: {order.get('quantity', 'N/A')}\n"
            summary += f"Status: {order.get('status', 'N/A')}\n---"
        
        return summary
        
    except Exception as e:
        print(f"Error querying orders: {e}")
        return f"Error querying orders: {str(e)}"

def update_order_status(params):
    """Update order status via Apps Script"""
    try:
        if 'order_id' in params:
            # Normalize status to match sheet names
            status = params['status'].strip().capitalize()
            result = call_apps_script('updateOrderStatusAndMove', {
                'orderId': params['order_id'],
                'newStatus': status
            })
            return True
        else:
            print("Warning: update_order_status called without order_id")
            return False
    except Exception as e:
        print(f"Error updating order status: {e}")
        return False

def get_orders_json():
    """Get all orders from the default sheet as JSON"""
    try:
        return get_sheet()
    except Exception as e:
        print(f"Error getting orders JSON: {e}")
        return []

def get_orders_from_sheet(sheet_name):
    """Get all orders from a specific sheet as JSON"""
    try:
        result = call_apps_script('getOrdersFromSheet', {'sheetName': sheet_name})
        return result.get('data', [])
    except Exception as e:
        print(f"Error getting orders from sheet {sheet_name}: {e}")
        return []

def get_available_sheet_names():
    """Get list of available sheet names"""
    try:
        result = call_apps_script('getAvailableSheets')
        return result.get('data', ['Pending', 'Ready', 'Delivered', 'Completed', 'Orders'])
    except Exception as e:
        print(f"Error getting available sheets: {e}")
        return ['Pending', 'Ready', 'Delivered', 'Completed', 'Orders']

def update_order_details(order):
    """Update order details - this would need to be implemented in Apps Script"""
    try:
        # For now, we'll use the status update mechanism
        if 'ID' in order and 'Status' in order:
            result = call_apps_script('updateOrderStatusAndMove', {
                'orderId': order['ID'],
                'newStatus': order['Status']
            })
            return True
        return False
    except Exception as e:
        print(f"Error updating order details: {e}")
        return False

def create_order(order):
    """Create a new order via Apps Script"""
    try:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        order_id = order.get('ID') or str(random.randint(100000, 999999))
        
        order_data = {
            'id': order_id,
            'clientName': order.get('Client Name', ''),
            'specifications': order.get('Glass Specifications', ''),
            'sizes': order.get('Sizes', ''),
            'quantity': order.get('Quantities', ''),
            'status': order.get('Status', 'Pending'),
            'notes': '',
            'createdAt': now,
            'updatedAt': now
        }
        
        result = call_apps_script('syncToSheets', {'orders': [order_data]})
        return True
    except Exception as e:
        print(f"Error creating order: {e}")
        return False

def delete_order(order):
    """Delete order - this would need to be implemented in Apps Script"""
    try:
        # This functionality would need to be added to the Apps Script
        print("Delete order functionality not yet implemented in Apps Script")
        return False
    except Exception as e:
        print(f"Error deleting order: {e}")
        return False 