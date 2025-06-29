#!/usr/bin/env python3
"""
Test script for WhatsApp Glass Bot commands
This script tests all the new commands to ensure they work correctly.
"""

import requests
import json
import time

# Configuration
BACKEND_URL = "http://localhost:5000"

def test_command(command, description):
    """Test a WhatsApp command and print the result"""
    print(f"\n{'='*60}")
    print(f"Testing: {description}")
    print(f"Command: {command}")
    print(f"{'='*60}")
    
    try:
        response = requests.post(f"{BACKEND_URL}/api/whatsapp_in", 
                               json={"body": command, "from": "test_user"})
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Success!")
            print(f"Reply: {result.get('reply', 'No reply')}")
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    time.sleep(1)  # Small delay between requests

def main():
    print("🤖 WhatsApp Glass Bot Command Tester")
    print("Testing all available commands...")
    
    # Test all the new commands
    test_commands = [
        ("/help", "Help command"),
        ("/pending", "Get pending orders"),
        ("/ready", "Get ready orders"),
        ("/delivered", "Get delivered orders"),
        ("/completed", "Get completed orders"),
        ("/all", "Get summary of all tabs"),
        ("/search test", "Search for 'test'"),
        ("/status test", "Search status for 'test'"),
        ("/update 123456 Ready", "Update order status"),
        ("/update", "Update command without parameters (should show help)"),
        ("/search", "Search command without parameters (should show help)"),
    ]
    
    for command, description in test_commands:
        test_command(command, description)
    
    print(f"\n{'='*60}")
    print("🎉 Testing completed!")
    print("Check the results above to ensure all commands work correctly.")
    print(f"{'='*60}")

if __name__ == "__main__":
    main() 