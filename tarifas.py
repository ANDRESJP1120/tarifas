import requests
import base64
import json
import time

# Configuración de la URL base y credenciales
base_url = "https://enelx.empsii.com/api/"
client_id = "enelx-api"
client_secret = "eg589sdf-42p5-85we-8eWq"
timeout_seconds = 15

# Función para obtener el token de acceso
def get_access_token():
    url = f"{base_url}oauth/token"
    data = {"grant_type": "client_credentials"}
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    headers = {"Authorization": f"Basic {encoded_credentials}", "Content-Type": "application/x-www-form-urlencoded"}
    
    try:
        response = requests.post(url, headers=headers, data=data, timeout=timeout_seconds)
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.exceptions.RequestException as e:
        print(f"Error obteniendo token: {e}")
        return None

# Función para hacer POST a un endpoint
def post_data_to_endpoint(endpoint, token, body):
    url = f"{base_url}{endpoint}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    try:
        start_time = time.time()
        response = requests.post(url, headers=headers, json=body, timeout=timeout_seconds)
        elapsed_time = time.time() - start_time
        response.raise_for_status()
        return response.json(), elapsed_time
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud a {url}: {e}")
        return None, None

# Función para consultar tarifas
def consultar_tarifas(access_token):
    endpoint = "tarifas/consultar/otros"
    for mercado, periodos in mercados.items():
        id_agente = mercado[:-1] + "D"
        for periodo in periodos:
            body = {
                "periodo": periodo.replace("-", ""),
                "mercadoComerc": mercado,
                "idAgente": id_agente,
                "nivelTension": 1,
                "propiedadActivos": "100% OPERADOR"
            }
            response, elapsed_time = post_data_to_endpoint(endpoint, access_token, body)
            if response:
                print(f"Consulta para {mercado} - {periodo}: {response}")
            else:
                print(f"Error en la consulta para {mercado} - {periodo}")

# Configuración de mercados y períodos
mercados = {
    "CASC": ["2023-07", "2024-02", "2025-01"],
    "CDNC": ["2024-10", "2025-01"],
    "CETC": ["2024-02", "2024-06", "2025-01"],
    "CHCC": ["2023-02", "2025-01"],
    "CMMC": ["2023-10", "2025-01"],
}

# Obtener token y ejecutar la consulta
token = get_access_token()
if token:
    consultar_tarifas(token)