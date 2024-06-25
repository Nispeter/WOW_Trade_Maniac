import dash 
from dash import Input, Output, State, ALL, callback_context, html
import plotly.graph_objs as go
from data import get_item_prices, get_item_statistics, get_lowest_price, df, create_elements, get_category_dict, merged_df, create_initial_search_options
from components import create_selected_filter_card, format_price_with_images
import dash_bootstrap_components as dbc

def register_callbacks(app):
    @app.callback(
        Output('cytoscape', 'elements'),
        Output('cytoscape', 'stylesheet'),
        Input('search-bar', 'value')
    )
    def update_graph(search_value):
        if search_value:
            filtered_df = df[df['item_name_es'].str.contains(search_value, case=False, na=False)]
            if not filtered_df.empty:
                item_id = filtered_df.iloc[0]['item_id']
                elements = create_elements(item_id)
                
                # Define stylesheet
                stylesheet = [
                    {
                        'selector': 'node',
                        'style': {
                            'label': 'data(label)',
                            'background-color': 'data(color)',  # Use the color data property
                            'color': '#FFFFFF'  # Label color
                        }
                    },
                    {
                        'selector': 'edge',
                        'style': {
                            'line-color': '#A3C4DC',
                            'width': 2
                        }
                    }
                ]
                return elements, stylesheet

        return [], []
    
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
                        price_data = get_item_prices(reagent_row['reagent_name_es'])
                        if price_data is not None and len(price_data) > 0:
                            unit_price = price_data[1]['unit_price']
                            result_str += f"{reagent_row['reagent_name_es']} - Cantidad: {reagent_row['reagent_quantity']}, Precio: {unit_price}<br>"
                        else:
                            result_str += f"{reagent_row['reagent_name_es']} - Cantidad: {reagent_row['reagent_quantity']}, Precio: No disponible<br>"
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
            empty_graph_layout = go.Layout(
            plot_bgcolor='#393433',
            paper_bgcolor='#393433',
            font={'color': '#CD970D'},
            xaxis={'showgrid': False, 'zeroline': False},
            yaxis={'showgrid': False, 'zeroline': False}
            )
            empty_graph = go.Figure(layout=empty_graph_layout)
            return "No item selected", "",empty_graph,empty_graph,empty_graph,empty_graph
        
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
            empty_graph_layout = go.Layout(
            plot_bgcolor='#393433',
            paper_bgcolor='#393433',
            font={'color': '#CD970D'},
            xaxis={'showgrid': False, 'zeroline': False},
            yaxis={'showgrid': False, 'zeroline': False}
            )
            empty_graph = go.Figure(layout=empty_graph_layout)
            return "No item selected", "",empty_graph,empty_graph,empty_graph,empty_graph
        item_name = search_value
        current_price = get_lowest_price(item_name)

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
        return item_name, format_price_with_images(current_price), lowest_price_figure, price_distribution_figure, quantity_sold_figure, price_quantity_scatter

    @app.callback(
        Output('selected-category-name', 'children'),  
        Output('search-bar', 'options'),
        Output('clear-filter-button', 'style'),
        [Input({'type': 'category-dropdown-item', 'index': ALL}, 'n_clicks'),
        Input('clear-filter-button', 'n_clicks')],
        prevent_initial_call=True
    )
    def update_output(category_clicks, clear_clicks):
        ctx = callback_context
        if not ctx.triggered:
            return create_selected_filter_card(), dash.no_update, {'display': 'none'}
        
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if triggered_id == 'clear-filter-button':
            return html.Div(style={'display': 'none'}), create_initial_search_options(),  {'display': 'none'}
        
        item_id = ctx.triggered[0]['prop_id'].split('.')[0]
        item_id = eval(item_id)['index']  # Convert string representation of dict back to dict
        
        filtered_df = merged_df[merged_df['subcategory'] == item_id]
        filtered_items = filtered_df['item_name'].unique().tolist()
        search_options = [{'label': item, 'value': item} for item in filtered_items]
        
        return create_selected_filter_card(item_id=item_id), search_options, {'display': 'block'}


