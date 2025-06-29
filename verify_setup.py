#!/usr/bin/env python3
"""
Setup verification script for WhatsApp Glass Bot
This script checks that all components are properly configured and working.
"""

import requests
import json
import os
import sys

def check_backend():
    """Check if the backend is running and responding"""
    print("🔍 Checking backend service...")
    try:
        response = requests.get("http://localhost:5000/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running and healthy")
            return True
        else:
            print(f"❌ Backend responded with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend is not accessible: {e}")
        return False

def check_google_sheets_integration():
    """Check if Google Sheets integration is working"""
    print("\n🔍 Checking Google Sheets integration...")
    try:
        response = requests.post("http://localhost:5000/api/whatsapp_in", 
                               json={"body": "/help", "from": "test_user"}, 
                               timeout=10)
        if response.status_code == 200:
            result = response.json()
            if "WhatsApp Glass Bot Commands" in result.get('reply', ''):
                print("✅ Google Sheets integration is working")
                return True
            else:
                print("❌ Google Sheets integration may have issues")
                return False
        else:
            print(f"❌ Backend error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing Google Sheets integration: {e}")
        return False

def check_environment_variables():
    """Check if required environment variables are set"""
    print("\n🔍 Checking environment variables...")
    
    required_vars = [
        'APPS_SCRIPT_URL',
        'BACKEND_API_URL'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please set these in your .env file or environment")
        return False
    else:
        print("✅ All required environment variables are set")
        return True

def test_basic_commands():
    """Test basic commands to ensure they work"""
    print("\n🔍 Testing basic commands...")
    
    test_commands = [
        ("/help", "Help command"),
        ("/all", "Summary command"),
    ]
    
    success_count = 0
    for command, description in test_commands:
        try:
            response = requests.post("http://localhost:5000/api/whatsapp_in", 
                                   json={"body": command, "from": "test_user"}, 
                                   timeout=10)
            if response.status_code == 200:
                print(f"✅ {description} works")
                success_count += 1
            else:
                print(f"❌ {description} failed")
        except Exception as e:
            print(f"❌ {description} error: {e}")
    
    return success_count == len(test_commands)

def main():
    print("🤖 WhatsApp Glass Bot Setup Verification")
    print("=" * 50)
    
    checks = [
        ("Backend Service", check_backend),
        ("Environment Variables", check_environment_variables),
        ("Google Sheets Integration", check_google_sheets_integration),
        ("Basic Commands", test_basic_commands),
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ Error during {check_name} check: {e}")
            results.append((check_name, False))
    
    print("\n" + "=" * 50)
    print("📊 Verification Results:")
    print("=" * 50)
    
    all_passed = True
    for check_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{check_name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All checks passed! Your WhatsApp Glass Bot is ready to use.")
        print("\nNext steps:")
        print("1. Start the WhatsApp bot: cd whatsapp-bot && npm start")
        print("2. Scan the QR code with your WhatsApp")
        print("3. Test the commands: /help, /pending, /ready, etc.")
    else:
        print("❌ Some checks failed. Please fix the issues above before proceeding.")
        print("\nCommon fixes:")
        print("1. Ensure backend is running: cd backend && python app.py")
        print("2. Check your .env file has correct URLs")
        print("3. Verify Google Apps Script is deployed and accessible")
    
    print("=" * 50)

if __name__ == "__main__":
    main() 