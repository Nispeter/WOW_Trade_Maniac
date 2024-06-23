
import dash_bootstrap_components as dbc
from dash import html

def create_selected_filter_card(item_id=None):
    if item_id is None:
        return html.Div(style={'display': 'none'})
    else:
        card_content = dbc.Card(
            dbc.CardBody(
                f"Selected Filter: {item_id}", 
                className='selected-filter-card-body'
            ),
            color="dark", 
            inverse=True, 
            className='selected-filter-card'
        )
        return card_content