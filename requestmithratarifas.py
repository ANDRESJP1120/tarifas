import requests
import base64
import json
from datetime import datetime
import concurrent.futures
import time

# Configuración de la URL base y las credenciales
base_url = "https://enelx.empsii.com/api/"
client_id = "enelx-api"
client_secret = "eg589sdf-42p5-85we-8eWq"
timeout_seconds = 15

# Función para obtener el token de acceso
def get_access_token():
    url = f"{base_url}oauth/token"
    data = {
        "grant_type": "client_credentials"
    }
    
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    try:
        response = requests.post(url, headers=headers, data=data, timeout=timeout_seconds)
        response.raise_for_status()
        return response.json()["access_token"]
    except requests.exceptions.RequestException as e:
        print(f"Error obtaining token: {e}")
        return None

# Función para realizar la solicitud POST con el periodo especificado
def post_data(period, mercadoComerc, idAgente, token):
    url = f"{base_url}/tarifas/consultar/otros"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    body = {
        "periodo": period,
        'mercadoComerc':mercadoComerc,
        'idAgente':idAgente,
    }
    
    try:
        start_time = time.time()
        response = requests.post(url, headers=headers, data=json.dumps(body), timeout=timeout_seconds)
        elapsed_time = time.time() - start_time
        response.raise_for_status()
        return response.json(), elapsed_time
    except requests.exceptions.RequestException as e:
        print(f"Error with request to {url}: {e}")
        return None, None

# Función para realizar solicitudes en paralelo
def perform_parallel_requests(num_requests, period, mercadoComerc, idAgente,):
    token = get_access_token()
    if not token:
        print("Could not obtain access token. Exiting.")
        return
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = [executor.submit(post_data, period, mercadoComerc, idAgente, token) for _ in range(num_requests)]
        
        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            response, elapsed_time = future.result()
            if response:
                business_code = response.get("codigo", "No business code found")
                print(f"Request {i+1}: Business Code: {business_code}, Time: {elapsed_time:.2f} seconds")
            else:
                print(f"Request {i+1} failed.")

# Ejecutar las solicitudes paralelas para el periodo 202409
perform_parallel_requests(1500, 202409, "ENDD", 'ENDC')
