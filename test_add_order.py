import requests
import json

# Test adding an order with multiple sizes
def test_add_order():
    # Simulate a WhatsApp message with multiple sizes
    message = """
    Client Name: Test Multiple Sizes 2
    Glass Specifications: 10mm Clear Glass
    Sizes:
    100x100
    200x200
    Quantities:
    2
    3
    """
    
    # Send to the backend
    response = requests.post(
        'http://localhost:5000/api/whatsapp_in',
        json={
            'body': message,
            'from': 'test_user'
        }
    )
    
    print("Response:", response.status_code)
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    test_add_order()