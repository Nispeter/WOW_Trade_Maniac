from dash import html

# Function to format the prices with gold and silver icons
def format_price_with_images(current_price):
    # Assuming current_price is a float
    integer_part, decimal_part = str(current_price).split('.')
    
    # Create the component for the integer part and its image
    integer_component = html.Span([
        html.Span(f"{integer_part}"),
        html.Img(src='../assets/coin-gold.png', style={'width': '20px', 'height': '20px'})
    ])
    
    # Initialize an empty list for components
    components = [integer_component]
    
    # Conditionally create and add the decimal component if decimal_part is not '0'
    if decimal_part != '0':
        decimal_component = html.Span([
            html.Span(f"{decimal_part}"),  # No decimal point prepended
            html.Img(src='../assets/coin-silver.png', style={'width': '20px', 'height': '20px'})
        ])
        components.append(decimal_component)
    
    # Combine everything into a single component
    price_with_images = html.Div(components)
    
    return price_with_images