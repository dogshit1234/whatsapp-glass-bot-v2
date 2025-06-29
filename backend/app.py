from flask import Flask, request, jsonify
from flask_cors import CORS
from extraction import extract_order_info, parse_command
from sheets import add_order, query_orders, update_order_status, get_tab_data, get_all_tabs_data, search_all_tabs, show_help, show_update_help, show_search_help
import logging
import os
from datetime import datetime, timezone

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

GOOGLE_CREDS = os.environ.get('GOOGLE_CREDS', 'google-credentials.json')
SHEET_NAME = os.environ.get('SHEET_NAME', 'WhatsApp Glass Bot Orders')
PORT = int(os.environ.get('BACKEND_PORT', 5000))

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'WhatsApp Glass Bot Backend is running'})

@app.route('/api/text_health', methods=['GET'])
def text_health():
    return jsonify({'status': 'OK', 'message': 'Text processing is active'})

@app.route('/api/whatsapp_in', methods=['POST'])
def whatsapp_in():
    """Handle WhatsApp text input - Core functionality for order processing"""
    try:
        # Parse request data
        data = request.json or {}
        user_msg = data.get('body', '').strip()
        from_user = data.get('from', 'unknown')
        
        print(f"=== TEXT MESSAGE RECEIVED ===")
        print(f"From: {from_user}")
        print(f"Message: {user_msg}")
        print(f"================================")
        
        if not user_msg:
            return jsonify({'reply': 'Please send your order details as text.'})
        
        # Check if it's a command (starts with /)
        command = parse_command(user_msg)
        if command:
            print(f"Processing command: {command['action']}")
            
            # Handle different command actions
            if command['action'] == 'get_tab_data':
                tab_name = command['params']['tab']
                result = get_tab_data(tab_name)
                return jsonify({'reply': result})
                
            elif command['action'] == 'get_all_tabs_data':
                result = get_all_tabs_data()
                return jsonify({'reply': result})
                
            elif command['action'] == 'search_all_tabs':
                search_term = command['params']['search_term']
                result = search_all_tabs(search_term)
                return jsonify({'reply': result})
                
            elif command['action'] == 'show_help':
                result = show_help()
                return jsonify({'reply': result})
                
            elif command['action'] == 'show_update_help':
                result = show_update_help()
                return jsonify({'reply': result})
                
            elif command['action'] == 'show_search_help':
                result = show_search_help()
                return jsonify({'reply': result})
                
            elif command['action'] == 'query':
                result = query_orders(command['params'])
                return jsonify({'reply': result})
                
            elif command['action'] == 'update':
                # Handle order status update
                order_id = command['params'].get('order_id')
                status = command['params'].get('status')
                
                if order_id and status:
                    success = update_order_status({'order_id': order_id, 'status': status})
                    if success:
                        return jsonify({'reply': f'✅ Order {order_id} status updated to {status} and moved to {status} tab.'})
                    else:
                        return jsonify({'reply': f'❌ Failed to update order {order_id}. Please check the order ID and try again.'})
                else:
                    return jsonify({'reply': '❌ Invalid update command. Use: /update [order_id] [status]'})
            else:
                return jsonify({'reply': 'Unknown command. Type /help for available commands.'})
        else:
            # Process as order data
            print("Processing as order data...")
            order_info = extract_order_info(user_msg)
            print(f"Extracted order info: {order_info}")
            
            # Add order to Google Sheets
            order_id_used = add_order(order_info)
            print("Order added to sheet successfully")
            
            # Create success message
            client_name = order_info.get('client_name', 'UNKNOWN')
            
            success_msg = f"✅ Order added successfully!\n\n"
            success_msg += f"Client: {client_name}\n"
            success_msg += f"Order ID: {order_id_used}\n"
            
            # Add extracted details if available
            if order_info.get('product'):
                success_msg += f"Product: {order_info['product']}\n"
            if order_info.get('quantity'):
                success_msg += f"Quantity: {order_info['quantity']}\n"
            if order_info.get('price'):
                success_msg += f"Price: {order_info['price']}\n"
            
            return jsonify({'reply': success_msg})
            
    except Exception as e:
        error_msg = f"Error processing your order: {str(e)}"
        print(f"Error in whatsapp_in: {error_msg}")
        return jsonify({'reply': 'Sorry, there was an error processing your order. Please try again or contact support.'})

@app.route('/api/orders', methods=['GET'])
def get_orders():
    """Simple endpoint to get all orders - for debugging/testing"""
    return jsonify(query_orders({}))

if __name__ == '__main__':
    print(f"Starting WhatsApp Glass Bot Backend on port {PORT}")
    print(f"Google Sheets integration active")
    app.run(host='0.0.0.0', port=PORT, debug=False) 