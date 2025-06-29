from backend.extraction import extract_order_info

# Test the extraction function with multiple sizes
def test_extraction():
    # Test message with multiple sizes in the format we expect
    message = """
    Client Name: Test Multiple Sizes 3
    Glass Specifications: 10mm Clear Glass
    
    Sizes:
    100x100
    200x200
    
    Quantities:
    2
    3
    """
    
    # Extract order info
    order_info = extract_order_info(message)
    
    # Print the extracted info
    print("Client Name:", order_info['client_name'])
    print("Glass Specs:", order_info['glass_specs'])
    print("Sizes:", order_info['sizes'])
    print("Quantities:", order_info['quantities'])

if __name__ == "__main__":
    test_extraction()