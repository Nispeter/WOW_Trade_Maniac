from dash import Input, Output
import plotly.graph_objs as go
from data import get_item_prices, get_item_statistics, df, create_elements

def register_callbacks(app):
    @app.callback(
        Output('cytoscape', 'elements'),
        Input('search-bar', 'value')
    )
    def update_graph(search_value):
        if search_value:
            filtered_df = df[df['item_name_es'].str.contains(search_value, case=False, na=False)]
            if not filtered_df.empty:
                item_id = filtered_df.iloc[0]['item_id']
                elements = create_elements(item_id)
                return elements
        return []

    @app.callback(
        Output('result', 'children'),
        Input('cytoscape', 'tapNodeData')
    )
    def display_requisites(node_data):
        if node_data:
            try:
                item_id = str(node_data['id'])
                item_rows = df[df['item_id'] == item_id]
                if not item_rows.empty:
                    item_row = item_rows.iloc[0]
                    item_name = item_row['item_name_es']
                    result_str = f"Nombre del ítem: {item_name}<br>"
                    result_str += f"Requiere:<br>"
                    reagent_df = df[df['recipe_id'] == item_row['recipe_id']]
                    for _, reagent_row in reagent_df.iterrows():
                        result_str += f"{reagent_row['reagent_name_es']} - Cantidad: {reagent_row['reagent_quantity']}<br>"
                    return result_str
            except Exception as e:
                print(f"Error processing node data: {e}")
        return "Seleccione un nodo para ver los requisitos de fabricación."

    @app.callback(
        Output('item-title', 'children'),
        Output('current-prices', 'children'),
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
            return "No Item Found", "", empty_layout, empty_layout, empty_layout, empty_layout
        
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
        return item_name, f"${current_price}", lowest_price_figure, price_distribution_figure, quantity_sold_figure, price_quantity_scatter
