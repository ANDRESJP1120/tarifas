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

# Function to calculate total consumption per energy type
def calcular_total_por_tipo(response):
    # Verifica si response es una cadena, en cuyo caso, conviértela en un diccionario
    if isinstance(response, str):
        response = json.loads(response)
    
    # Inicializa un diccionario para almacenar los totales
    totales = {
        "activa_total": 0,
        "inductiva_total": 0,
        "liquidada_total": 0,
        "reactiva_total": 0
    }

    # Accede a los consumos diarios detallados
    consumos_diarios = response.get("consumosDiariosDetallados", [])
    
    # Recorre cada día y suma los totales para cada tipo de consumo
    for dia in consumos_diarios:
        consumos = dia.get("consumos", {})
        totales["activa_total"] += consumos.get("activa", {}).get("total", 0)
        totales["inductiva_total"] += consumos.get("inductiva", {}).get("total", 0)
        totales["liquidada_total"] += consumos.get("liquidada", {}).get("total", 0)
        totales["reactiva_total"] += consumos.get("reactiva", {}).get("total", 0)
    
    return totales
# Function to request daily consumption for graphs and calculate totals
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
        print("Calculando totales por tipo de energía...")
        
        # Calculate totals per energy type
        totales = calcular_total_por_tipo(response)
        print("Totales por tipo de energía:")
        for tipo, total in totales.items():
            print(f"{tipo.capitalize()}: {total:.2f}")
    else:
        print("No se pudo obtener los datos de la gráfica de consumos diarios.")

# Example usage
fecha_inicial = "01/07/2024"
fecha_final = "31/07/2024"
codigo_nit = 9013838655
id_clientes = ["1072"]

consultar_grafica_consumos_diarios(fecha_inicial, fecha_final, codigo_nit, id_clientes)
