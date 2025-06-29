import re

def extract_order_info(text):
    # Extract client name
    client_match = re.search(r'Client Name[:\-]?\s*(.+)', text, re.IGNORECASE)
    client_name = client_match.group(1).strip() if client_match else 'UNKNOWN'

    # Extract glass specifications
    specs_match = re.search(r'Glass Specifications[:\-]?\s*(.+)', text, re.IGNORECASE)
    glass_specs = specs_match.group(1).strip() if specs_match else ''

    # Extract proforma invoice/order id if present
    order_id_match = re.search(r'Proforma Invoice No\.?[:\-]?\s*([A-Za-z0-9\-/]+)', text, re.IGNORECASE)
    order_id = order_id_match.group(1).strip() if order_id_match else None

    # Extract all size/quantity lines with multiple patterns
    size_qty_lines = []
    
    # Pattern 1: Numbered list (e.g., 1. 83 x 72 1/8 - 1)
    size_qty_lines = re.findall(r'\d+\.\s*([\d\s\./x]+)\s*-\s*(\d+)', text)
    
    # Pattern 2: Without numbering (e.g., 83 x 72 1/8 - 1)
    if not size_qty_lines:
        size_qty_lines = re.findall(r'([\d\s\./x]+)\s*-\s*(\d+)', text)
    
    # Pattern 3: Look for "Sizes:" and "Quantities:" sections
    if not size_qty_lines:
        sizes_section = re.search(r'Sizes[:\-]?\s*(.+?)(?=Quantities|\Z)', text, re.IGNORECASE | re.DOTALL)
        quantities_section = re.search(r'Quantities[:\-]?\s*(.+)', text, re.IGNORECASE | re.DOTALL)
        
        if sizes_section and quantities_section:
            # Extract sizes and quantities, filtering out empty lines and headers
            sizes_text = sizes_section.group(1).strip()
            quantities_text = quantities_section.group(1).strip()
            
            # Split by newlines and filter out empty lines and any lines containing "Sizes:" or "Quantities:"
            sizes_list = [s.strip() for s in sizes_text.split('\n') 
                         if s.strip() and not re.search(r'Sizes[:\-]?', s, re.IGNORECASE)]
            quantities_list = [q.strip() for q in quantities_text.split('\n') 
                              if q.strip() and not re.search(r'Quantities[:\-]?', q, re.IGNORECASE)]
            
            print(f"Debug - Sizes list: {sizes_list}")
            print(f"Debug - Quantities list: {quantities_list}")
            
            # Create pairs from the two lists
            size_qty_lines = list(zip(sizes_list, quantities_list))
    
    # Pattern 4: Look for "Actual Size and Quantity:" section
    if not size_qty_lines:
        actual_size_qty_section = re.search(r'Actual Size and Quantity[:\-]?\s*(.+)', text, re.IGNORECASE | re.DOTALL)
        if actual_size_qty_section:
            section_text = actual_size_qty_section.group(1).strip()
            # Try to find numbered list format in this section
            numbered_items = re.findall(r'\d+\.\s*([\d\s\./x]+)\s*-\s*(\d+)', section_text)
            if numbered_items:
                size_qty_lines = numbered_items
            else:
                # Try non-numbered format
                non_numbered_items = re.findall(r'([\d\s\./x]+)\s*-\s*(\d+)', section_text)
                if non_numbered_items:
                    size_qty_lines = non_numbered_items
    
    # Pattern 5: If glass specs is found but no sizes, use glass specs as the size
    if not size_qty_lines and glass_specs:
        # Look for quantity after glass specs
        qty_match = re.search(r'Quantity[:\-]?\s*(\d+)', text, re.IGNORECASE)
        qty = qty_match.group(1).strip() if qty_match else '1'  # Default to 1 if no quantity found
        size_qty_lines = [(f"Glass Specifications: {glass_specs}", qty)]
    
    # Process the extracted lines
    sizes = [s.strip() for s, q in size_qty_lines] if size_qty_lines else []
    quantities = [q.strip() for s, q in size_qty_lines] if size_qty_lines else []
    
    # Debug print
    print(f"Extracted sizes: {sizes}")
    print(f"Extracted quantities: {quantities}")

    return {
        'client_name': client_name,
        'glass_specs': glass_specs,
        'sizes': sizes,
        'quantities': quantities,
        'order_id': order_id
    }

def parse_command(text):
    # WhatsApp slash command parser
    text = text.strip().lower()
    
    # New enhanced commands for different tabs
    if text.startswith('/pending'):
        return {'action': 'get_tab_data', 'params': {'tab': 'Pending'}}
    elif text.startswith('/ready'):
        return {'action': 'get_tab_data', 'params': {'tab': 'Ready'}}
    elif text.startswith('/delivered'):
        return {'action': 'get_tab_data', 'params': {'tab': 'Delivered'}}
    elif text.startswith('/completed'):
        return {'action': 'get_tab_data', 'params': {'tab': 'Completed'}}
    elif text.startswith('/all'):
        return {'action': 'get_all_tabs_data', 'params': {}}
    elif text.startswith('/help'):
        return {'action': 'show_help', 'params': {}}
    elif text.startswith('/status'):
        # /status [client name or order id]
        parts = text.split(maxsplit=1)
        if len(parts) > 1:
            return {'action': 'query', 'params': {'client_name': parts[1]}}
        else:
            return {'action': 'query', 'params': {}}
    elif text.startswith('/update'):
        # /update [order id] [status]
        parts = text.split()
        if len(parts) >= 3:
            return {'action': 'update', 'params': {'order_id': parts[1], 'status': parts[2]}}
        else:
            return {'action': 'show_update_help', 'params': {}}
    elif text.startswith('/search'):
        # /search [client name or order id]
        parts = text.split(maxsplit=1)
        if len(parts) > 1:
            return {'action': 'search_all_tabs', 'params': {'search_term': parts[1]}}
        else:
            return {'action': 'show_search_help', 'params': {}}
    
    # Legacy commands for backward compatibility
    elif text.startswith('/query'):
        return {'action': 'query', 'params': {}}
    
    return None 