import requests
import pandas as pd
from datetime import datetime

# Configuración
client_id = '9eb1cdbc77b344d0b2cf9cae2e67e2e2'
client_secret = 'gNK7131xK3IsLyYC43HuAKL3YulaZGHb'
region = 'us'  # us, eu, kr, tw, cn

# Obtener token de acceso
def obtener_token(client_id, client_secret):
    url = f'https://{region}.battle.net/oauth/token'
    data = {'grant_type': 'client_credentials'}
    response = requests.post(url, data=data, auth=(client_id, client_secret))
    response.raise_for_status()
    return response.json()['access_token']

# Obtener profesiones
def obtener_profesiones(token):
    url = f'https://{region}.api.blizzard.com/data/wow/profession/index'
    headers = {'Authorization': f'Bearer {token}'}
    params = {'namespace': f'static-{region}', 'locale': 'en_US'}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()['professions']

# Obtener skill tiers de una profesión
def obtener_skill_tiers(token, profession_id):
    url = f'https://{region}.api.blizzard.com/data/wow/profession/{profession_id}'
    headers = {'Authorization': f'Bearer {token}'}
    params = {'namespace': f'static-{region}', 'locale': 'en_US'}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    response_json = response.json()
    print(f"Response for profession {profession_id}: {response_json}")  # Debugging line
    return response_json.get('skill_tiers', [])

# Obtener recetas de un skill tier
def obtener_recetas_de_skill_tier(token, skill_tier_url):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(skill_tier_url, headers=headers)
    response.raise_for_status()
    return response.json().get('categories', [])

# Obtener detalles de una receta
def obtener_detalles_receta(token, recipe_url):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(recipe_url, headers=headers)
    response.raise_for_status()
    return response.json()

# Obtener datos de las recetas de profesiones
def obtener_datos_recetas(token):
    profesiones = obtener_profesiones(token)
    recipes = []
    for profesion in profesiones:
        skill_tiers = obtener_skill_tiers(token, profesion['id'])
        if not skill_tiers:
            print(f"No skill tiers found for profession {profesion['name']} (ID: {profesion['id']})")
            continue

        for skill_tier in skill_tiers:
            # Log each skill tier being processed
            print(f"Processing skill tier {skill_tier['id']} for profession {profesion['name']} (ID: {profesion['id']})")
            categories = obtener_recetas_de_skill_tier(token, skill_tier['key']['href'])
            for category in categories:
                for recipe in category['recipes']:
                    recipe_data = obtener_detalles_receta(token, recipe['key']['href'])
                    recipes.append({
                        'id': recipe_data['id'],
                        'name': recipe_data['name'],
                        'reagents': [{'id': reagent['reagent']['id'], 'name': reagent['reagent']['name'], 'quantity': reagent['quantity']} for reagent in recipe_data.get('reagents', [])]
                    })
    return recipes

# Guardar datos en un archivo Excel
def guardar_datos_en_excel(datos, file_path):
    rows = []
    for recipe in datos:
        for reagent in recipe['reagents']:
            rows.append({
                'recipe_id': recipe['id'],
                'recipe_name': recipe['name'],
                'reagent_id': reagent['id'],
                'reagent_name': reagent['name'],
                'reagent_quantity': reagent['quantity']
            })
    df = pd.DataFrame(rows)
    df.to_excel(file_path, index=False)

# Obtener y guardar datos de recetas
def obtener_y_guardar_recetas():
    print("Starting to fetch recipes...")
    token = obtener_token(client_id, client_secret)
    print("Token obtained.")
    recetas = obtener_datos_recetas(token)
    if not recetas:
        print("No recipes found.")
        return

    print("Recipes data obtained.")
    current_date = datetime.now().strftime('%Y-%m-%d-%H')
    file_path = f'data/dragonflight_recipes-{current_date}.xlsx'
    guardar_datos_en_excel(recetas, file_path)
    print(f"Datos almacenados correctamente en '{file_path}'")
    print("Fetching completed.")

if __name__ == '__main__':
    obtener_y_guardar_recetas()  # Run the function immediately
