from dash import Input, Output
import plotly.graph_objs as go
from data import get_item_prices, get_item_statistics

def register_callbacks(app):
    @app.callback(
        Output('item-title', 'children'),
        Output('current-prices', 'children'),
        Output('price-history-graph', 'figure'),
        Output('lowest-price-graph', 'figure'),
        Output('price-distribution-graph', 'figure'),
        Output('quantity-sold-graph', 'figure'),
        Output('price-quantity-scatter', 'figure'),
        Input('search-bar', 'value')
    )
    def update_item_details(search_value):
        if search_value is None:
            search_value = 'Rune Cloth'
        
        item_data = get_item_prices(search_value)
        item_stats = get_item_statistics(search_value)
        if not item_data:
            empty_layout = {
                'data': [],
                'layout': {
                    'plot_bgcolor': '#393433',
                    'paper_bgcolor': '#393433',
                    'font': {
                        'color': '#CD970D'
                    },
                    'title': 'No Data',
                    'xaxis': {
                        'gridcolor': 'rgba(205, 151, 13, 0.2)',
                        'linecolor': '#CD970D',
                        'ticks': 'outside',
                        'tickcolor': '#CD970D',
                        'showgrid': True
                    },
                    'yaxis': {
                        'gridcolor': 'rgba(205, 151, 13, 0.2)',
                        'linecolor': '#CD970D',
                        'ticks': 'outside',
                        'tickcolor': '#CD970D',
                        'showgrid': True
                    }
                }
            }
            return "No Item Found", "", empty_layout, empty_layout, empty_layout, empty_layout, empty_layout
        
        item_name = search_value
        current_price = item_data[-1]['unit_price'] if item_data else 0

        # Prepare data for the price history graph
        x_values = [entry['snapshot_order'] for entry in item_data]
        y_values = [entry['unit_price'] for entry in item_data]
        # Graph layout
        graph_layout = {
            'plot_bgcolor': '#393433',
            'paper_bgcolor': '#393433',
            'font': {
                'color': '#CD970D'
            },
            'xaxis': {
                'gridcolor': 'rgba(205, 151, 13, 0.5)',
                'linecolor': '#CD970D',
                'title': 'Time',
                'ticks': 'outside',
                'tickcolor': '#CD970D',
                'showgrid': True
            },
            'yaxis': {
                'gridcolor': 'rgba(205, 151, 13, 0.5)',
                'linecolor': '#CD970D',
                'title': 'Price',
                'ticks': 'outside',
                'tickcolor': '#CD970D',
                'showgrid': True
            }
        }

        # Price History Graph
        price_history_figure = {
            'data': [go.Scatter(x=x_values, y=y_values, mode='lines', name='Price History')],
            'layout': {
                **graph_layout, 
                'title': 'Price History', 
                'xaxis': {**graph_layout['xaxis'], 'title': 'Time (hours)'}, 
                'yaxis': {**graph_layout['yaxis'], 'title': 'Price'}
            }
        }

        # Lowest Price Over Time Graph
        lowest_price = item_stats.groupby('snapshot_order')['unit_price'].min().reset_index()
        lowest_price_figure = {
            'data': [go.Scatter(x=lowest_price['snapshot_order'], y=lowest_price['unit_price'], mode='lines', name='Lowest Price')],
            'layout': {
                **graph_layout, 
                'title': 'Lowest Price Over Time', 
                'xaxis': {**graph_layout['xaxis'], 'title': 'Time (hours)'}, 
                'yaxis': {**graph_layout['yaxis'], 'title': 'Price'}
            }
        }

        # Price Distribution Over Time Graph
        price_distribution_figure = {
            'data': [go.Box(x=item_stats['snapshot_order'], y=item_stats['unit_price'], name='Price Distribution')],
            'layout': {
                **graph_layout, 
                'title': 'Price Distribution Over Time', 
                'xaxis': {**graph_layout['xaxis'], 'title': 'Time (hours)'}, 
                'yaxis': {**graph_layout['yaxis'], 'title': 'Price'}
            }
        }

        # Quantity Sold Over Time Graph
        quantity_sold_figure = {
            'data': [go.Bar(x=x_values, y=[entry['quantity'] for entry in item_data], name='Quantity Sold')],
            'layout': {
                **graph_layout, 
                'title': 'Quantity Sold Over Time', 
                'xaxis': {**graph_layout['xaxis'], 'title': 'Time (hours)'}, 
                'yaxis': {**graph_layout['yaxis'], 'title': 'Quantity (units)'}
            }
        }

        # Price vs Quantity Sold Scatter Plot
        price_quantity_scatter = {
            'data': [go.Scatter(x=item_stats['quantity'], y=item_stats['unit_price'], mode='markers', name='Price vs Quantity')],
            'layout': {
                **graph_layout, 
                'title': 'Price vs Quantity Sold', 
                'xaxis': {**graph_layout['xaxis'], 'title': 'Quantity (units)'}, 
                'yaxis': {**graph_layout['yaxis'], 'title': 'Price'}
            }
        }
        return item_name, f"${current_price}", price_history_figure, lowest_price_figure, price_distribution_figure, quantity_sold_figure, price_quantity_scatter
