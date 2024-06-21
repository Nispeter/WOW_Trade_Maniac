import dash
from dash import dcc, html, Input, Output
import dash_cytoscape as cyto
import pandas as pd

# Load the Excel file
df = pd.read_excel('../api/data/wow_recipes.xlsx')

# Function to safely extract 'es_MX' names
def get_es_mx_name(name):
    try:
        name_dict = eval(name)
        return name_dict.get('es_MX', 'Nombre no disponible')
    except:
        return 'Nombre no disponible'

# Apply the function to the columns
df['item_name_es'] = df['recipe_name'].apply(get_es_mx_name)
df['reagent_name_es'] = df['reagent_name'].apply(get_es_mx_name)

# Initialize the Dash app
app = dash.Dash(__name__)

# Helper function to create nodes and edges for cytoscape
def create_elements(item_id):
    elements = []
    visited = set()
    
    def add_elements(item_id):
        if item_id in visited:
            return
        visited.add(item_id)
        
        item_rows = df[df['item_id'] == item_id]
        if item_rows.empty:
            print(f"No item found for ID: {item_id}")
            return
        
        item_row = item_rows.iloc[0]
        item_name = item_row['item_name_es']
        print(f"Adding item: {item_name} (ID: {item_id})")
        elements.append({'data': {'id': str(item_id), 'label': item_name}})
        
        reagents = df[df['recipe_id'] == item_row['recipe_id']]
        for _, reagent in reagents.iterrows():
            reagent_id = reagent['reagent_id']
            reagent_name = reagent['reagent_name_es']
            reagent_quantity = reagent['reagent_quantity']
            print(f"Adding reagent: {reagent_name} (ID: {reagent_id}, Quantity: {reagent_quantity})")
            elements.append({'data': {'id': str(reagent_id), 'label': f"{reagent_name} ({reagent_quantity})"}})
            elements.append({'data': {'source': str(item_id), 'target': str(reagent_id)}})
            add_elements(reagent_id)
    
    add_elements(item_id)
    return elements

app.layout = html.Div([
    dcc.Input(id='search-bar', type='text', placeholder='Buscar ítem...'),
    html.Button('Buscar', id='search-button', n_clicks=0),
    html.Div(id='result'),
    cyto.Cytoscape(
        id='cytoscape',
        layout={'name': 'breadthfirst'},
        style={'width': '100%', 'height': '600px'},
        elements=[],
    )
])

@app.callback(
    Output('cytoscape', 'elements'),
    [Input('search-button', 'n_clicks')],
    [Input('search-bar', 'value')]
)
def update_graph(n_clicks, search_value):
    if n_clicks > 0 and search_value:
        filtered_df = df[df['item_name_es'].str.contains(search_value, case=False, na=False)]
        if not filtered_df.empty:
            item_id = filtered_df.iloc[0]['item_id']
            elements = create_elements(item_id)
            return elements
    return []

@app.callback(
    Output('result', 'children'),
    [Input('cytoscape', 'tapNodeData')]
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

if __name__ == '__main__':
    app.run_server(debug=True)
