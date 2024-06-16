from dash import Input, Output
from data import get_item_prices

def register_callbacks(app):
    @app.callback(
        Output('item-title', 'children'),
        Output('current-prices', 'children'),
        Output('price-history-graph', 'figure'),
        Input('search-bar', 'value')
    )
    def update_item_details(search_value):
        if search_value is None:
            search_value = 'Rune Cloth'
        
        item_data = get_item_prices(search_value)
        if not item_data:
            return "No Item Found", "", { 'data': [],
                'layout': {
                'plot_bgcolor': '#393433', 
                'paper_bgcolor': '#393433',  
                'font': {
                    'color': '#CD970D'  
                },
                'title': 'Price History',
                'xaxis': {
                    'gridcolor': 'rgba(205, 151, 13, 0.2)',  
                    'linecolor': '#CD970D',                  
                    'title': 'Time',
                    'ticks': 'outside',                      
                    'tickcolor': '#CD970D'                 
                },
                'yaxis': {
                    'gridcolor': 'rgba(205, 151, 13, 0.2)',
                    'linecolor': '#CD970D',                  
                    'title': 'Price',
                    'ticks': 'outside',                     
                    'tickcolor': '#CD970D'   
                }
            }
            }
        
        item_name = search_value
        current_price = item_data[-1]['unit_price'] if item_data else 0

        # Prepare data for the graph
        x_values = list(range(1, len(item_data) + 1))
        y_values = [entry['unit_price'] for entry in item_data]

        return item_name, f"${current_price}", {
            'data': [{'x': x_values, 'y': y_values, 'type': 'line'}],
            'layout': {
                'plot_bgcolor': '#393433',  
                'paper_bgcolor': '#393433',  
                'font': {
                    'color': '#CD970D'  
                },
                'title': 'Price History',
                'xaxis': {
                    'gridcolor': 'rgba(205, 151, 13, 0.2)',  
                    'linecolor': '#CD970D',                  
                    'title': 'Time',
                    'ticks': 'outside',                     
                    'tickcolor': '#CD970D'  
                },       
                'yaxis': {
                    'gridcolor': 'rgba(205, 151, 13, 0.2)',
                    'linecolor': '#CD970D',                  
                    'title': 'Price',
                    'ticks': 'outside',                     
                    'tickcolor': '#CD970D'                   
                }
            }
        }
