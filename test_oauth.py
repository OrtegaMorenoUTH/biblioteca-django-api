import requests
from dotenv import load_dotenv
import os

# Configuración
TOKEN_URL = 'http://127.0.0.1:8000/o/token/'
API_URL = 'http://127.0.0.1:8000/api/libros/'

CLIENT_ID = os.getenv('client_id_1')
CLIENT_SECRET = os.getenv('secret_1')
USERNAME = os.getenv('username')
PASSWORD = os.getenv('password')

print("=== Obteniendo Token OAuth 2.0 ===")

# Obtener token
response = requests.post(TOKEN_URL, data={
    'grant_type': 'password',
    'username': USERNAME,
    'password': PASSWORD,
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'scope': 'read write'
})

if response.status_code == 200:
    token_data = response.json()
    access_token = token_data['access_token']
    
    print(f"✅ Token obtenido: {access_token[:50]}...")
    
    # Usar token para acceder a API
    headers = {'Authorization': f'Bearer {access_token}'}
    api_response = requests.get(API_URL, headers=headers)
    
    print(f"Status Code: {api_response.status_code}")
    print(f"Data: {api_response.json()}")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.json())