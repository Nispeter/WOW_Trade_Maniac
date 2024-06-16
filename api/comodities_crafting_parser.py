import requests
import networkx as nx
import matplotlib.pyplot as plt

    # Constants
BASE_URL = "https://us.api.blizzard.com"
TOKEN_URL = "https://us.battle.net/oauth/token"
CLIENT_ID = "66334634617f4dc4bf3b48780af2d33e"
CLIENT_SECRET = "cTYlqWp1ZFnpHDQf6hQNmxXrDTLfz6aq"
NAMESPACE = "static-us"
LOCALE = "en_US"

def get_access_token():
    data = {'grant_type': 'client_credentials'}
    response = requests.post(TOKEN_URL, data=data, auth=(CLIENT_ID, CLIENT_SECRET))
    print(response.json())
    return response.json().get('access_token')
import requests
import networkx as nx
import matplotlib.pyplot as plt

# Function to get item details from WoW API
def get_item_details(item_id, api_key):
    url = f"https://us.api.blizzard.com/data/wow/item/{item_id}?namespace=static-us&locale=en_US&access_token={api_key}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# Function to get recipe details from WoW API
def get_recipe_details(recipe_id, api_key):
    url = f"https://us.api.blizzard.com/data/wow/recipe/{recipe_id}?namespace=static-us&locale=en_US&access_token={api_key}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# Function to get crafting dependencies recursively
def get_crafting_dependencies(item_id, api_key, dependencies=None):
    if dependencies is None:
        dependencies = {}
        
    if item_id in dependencies:
        return dependencies
    
    item_data = get_item_details(item_id, api_key)
    dependencies[item_id] = {
        'name': item_data['name'],
        'reagents': {}
    }

    # Check if the item has spells and look for crafting spells
    if 'spells' in item_data:
        for spell in item_data['spells']:
            spell_id = spell['spell']['id']
            spell_details = get_recipe_details(spell_id, api_key)
            if 'reagents' in spell_details:
                for reagent in spell_details['reagents']:
                    reagent_id = reagent['reagent']['id']
                    reagent_name = reagent['reagent']['name']
                    dependencies[item_id]['reagents'][reagent_id] = reagent_name
                    get_crafting_dependencies(reagent_id, api_key, dependencies)
    
    return dependencies

# Function to create a graph from dependencies
def create_graph(dependencies):
    G = nx.DiGraph()
    for item_id, item_info in dependencies.items():
        G.add_node(item_id, label=item_info['name'])
        for reagent_id, reagent_name in item_info.get('reagents', {}).items():
            G.add_node(reagent_id, label=reagent_name)
            G.add_edge(item_id, reagent_id)
    return G

# Function to draw the graph
def draw_graph(G):
    pos = nx.spring_layout(G)
    labels = nx.get_node_attributes(G, 'label')
    nx.draw(G, pos, labels=labels, with_labels=True, node_size=3000, node_color='skyblue', font_size=10, font_weight='bold', edge_color='gray')
    plt.show()

# Main function
def main():
    api_key = get_access_token()
    item_id = 205039  # Example item ID, replace with the desired item ID
    
    dependencies = get_crafting_dependencies(item_id, api_key)
    G = create_graph(dependencies)
    draw_graph(G)

if __name__ == "__main__":
    main()
