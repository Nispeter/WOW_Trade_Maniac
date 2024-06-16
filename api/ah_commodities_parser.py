import requests
import json
import pandas as pd
import schedule
import time
from datetime import datetime

# Configuración
# Añadir sus keys desde https://develop.battle.net
client_id = ''
client_secret = ''
region = 'us'  # us, eu, kr, tw, cn (cn es medio raro)
realm_id = '1428' # Quel'Thalas ID

# Obtener token de acceso
def obtener_token(client_id, client_secret):
    url = f'https://{region}.battle.net/oauth/token'
    data = {'grant_type': 'client_credentials'}
    response = requests.post(url, data=data, auth=(client_id, client_secret))
    response.raise_for_status()
    return response.json()['access_token']

# Obtener datos de la subasta de commodities
def obtener_datos_commodities(token):
    url = f'https://{region}.api.blizzard.com/data/wow/auctions/commodities'
    headers = {'Authorization': f'Bearer {token}'}
    params = {'namespace': f'dynamic-{region}', 'locale': 'en_US'}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

# Guardar datos en un archivo Excel
def guardar_datos_en_excel(datos, file_path):
    df = pd.DataFrame(datos)
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    df['date'] = fecha_actual
    df.to_excel(file_path, index=False)

# Para dejar mientras duermo xd
def take_snapshot():
    print("Starting snapshot...")
    token = obtener_token(client_id, client_secret)
    print("Token obtained.")
    datos_commodities = obtener_datos_commodities(token)
    print("Commodities data obtained.")

    all_items = []

    for commodity in datos_commodities['auctions']:
        item_id = commodity['item']['id']
        unit_price = commodity['unit_price'] / 10000
        quantity = commodity['quantity']

        all_items.append({
            'item_id': item_id,
            'unit_price': unit_price,
            'quantity': quantity,
        })

    print("Data processed.")
    df = pd.DataFrame(all_items)
    current_date = datetime.now().strftime('%Y-%m-%d-%H')
    df.to_excel(f'data/commodities_snapshot-{current_date}.xlsx', index=False)

    print(f"Datos almacenados correctamente en 'commodities_snapshot-{current_date}.xlsx'")
    print("Snapshot completed.")

if __name__ == '__main__':
    take_snapshot()  # Run the function immediately
    schedule.every(1).hours.do(take_snapshot)  # Then schedule it to run every hour

    while True:
        schedule.run_pending()
        time.sleep(1)
