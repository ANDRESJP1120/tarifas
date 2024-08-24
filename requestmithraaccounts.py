import requests
import base64
import json
import time

base_url = "https://enelx.empsii.com/api/"
client_id = "enelx-api"
client_secret = "eg589sdf-42p5-85we-8eWq"
timeout_seconds = 15

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

def post_data_to_endpoint(endpoint, token, body):
    url = f"{base_url}{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        start_time = time.time()
        response = requests.post(url, headers=headers, data=json.dumps(body), timeout=timeout_seconds)
        elapsed_time = time.time() - start_time
        response.raise_for_status()
        return response.json(), elapsed_time
    except requests.exceptions.ReadTimeout:
        print(f"Request to {url} timed out after {timeout_seconds} seconds.")
        return None, elapsed_time
    except requests.exceptions.RequestException as e:
        print(f"Error with request to {url}: {e}")
        return None, None

# Función para consultar consumos diarios para gráficos
def consultar_grafica_consumos_diarios(fecha_inicial, fecha_final, codigo_nit, id_clientes):
    token = get_access_token()
    if not token:
        print("No se pudo obtener el token de acceso.")
        return
    
    endpoint = "consumos/grafica-diaria"
    
    body = {
        "fechaInicial": fecha_inicial,
        "fechaFinal": fecha_final,
        "codigoNit": codigo_nit,
        "idClientes": id_clientes
    }
    
    response, elapsed_time = post_data_to_endpoint(endpoint, token, body)
    
    if response:
        print(f"Respuesta recibida en {elapsed_time:.2f} segundos.")
        print("Datos obtenidos:")
        print(json.dumps(response, indent=4, ensure_ascii=False))
    else:
        print("No se pudo obtener los datos de la gráfica de consumos diarios.")

# Ejemplo de uso
fecha_inicial = "01/05/2024"
fecha_final = "31/05/2024"
codigo_nit =8300332063
id_clientes = ["1196"]

consultar_grafica_consumos_diarios(fecha_inicial, fecha_final, codigo_nit, id_clientes)
