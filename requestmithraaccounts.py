import requests
import base64
import json
from datetime import datetime, timedelta
import time
import numpy as np
import openpyxl
from openpyxl import Workbook

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

# Función para realizar una solicitud POST con cuerpo JSON a cualquier endpoint
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
        return response, elapsed_time
    except requests.exceptions.ReadTimeout:
        print(f"Request to {url} timed out after {timeout_seconds} seconds.")
        return None, elapsed_time
    except requests.exceptions.RequestException as e:
        print(f"Error with request to {url}: {e}")
        return None, None

# Función para consultar la lista de clientes
def consultar_clientes(access_token, id_cliente_nit=None):
    body = {}
    if id_cliente_nit:
        body["idClienteNit"] = id_cliente_nit

    endpoint = "cliente/asesor"
    response, _ = post_data_to_endpoint(endpoint, access_token, body)
    
    if response and response.status_code == 200:
        data = response.json()
        if "listaClienteNitAsesor" in data:
            return data["listaClienteNitAsesor"]
        else:
            print("No se encontró 'listaClienteNitAsesor' en la respuesta.")
            return []
    else:
        print("No se pudieron consultar los clientes.")
        return None

# Función para consultar consumos de un cliente
def consultar_consumos(access_token, fecha, codigo_sic, id_cliente):
    body = {
        "fecha": fecha,
        "codigoSic": codigo_sic
    }
    
    endpoint = "consumos/consultar"
    response, elapsed_time = post_data_to_endpoint(endpoint, access_token, body)
    
    if response and response.status_code == 200:
        consumos = response.json()
        if any(value is (isinstance(value, float) and np.isnan(value)) for value in consumos.values()):
            print(f"{codigo_sic}-{id_cliente}-error: Datos nulos o no válidos en la respuesta de consumos.")
        print(f"Tiempo de la solicitud de consumos para {codigo_sic}-{id_cliente}: {elapsed_time:.2f} segundos")
        return consumos
    else:
        print(f"Error consulting consumos for {codigo_sic}-{id_cliente}.")
        return None

# Función para guardar tiempos de espera en un archivo Excel
def save_timeout_data(timeout_data):
    wb = Workbook()
    ws = wb.active
    ws.title = "Timeouts"
    ws.append(["Nombre Facturación", "Timeout (segundos)"])
    
    for item in timeout_data:
        ws.append(item)
    
    wb.save("timeout_data.xlsx")

# Función para guardar errores de datos nulos en un archivo Excel
def save_nan_data(nan_data):
    wb = Workbook()
    ws = wb.active
    ws.title = "Datos Nulos"
    ws.append(["Nombre Facturación", "Datos Nulos"])
    
    for item in nan_data:
        ws.append(item)
    
    wb.save("nan_data.xlsx")

# Obtener el token de acceso
token = get_access_token()

# Listas para almacenar los datos que se guardarán en los archivos Excel
timeout_data = []
nan_data = []

if token:
    # Consultar la lista de clientes
    clientes = consultar_clientes(token)
    
    if clientes:
        for cliente in clientes:
            codigo_sic = cliente.get("codigoSic")
            id_cliente = cliente.get("idCliente")
            nombre_facturacion = cliente.get("nombreFacturacion")

            if codigo_sic and id_cliente:
                fecha_actual = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
                
                consumos = consultar_consumos(token, fecha_actual, codigo_sic, id_cliente)
                if consumos is None:
                    timeout_data.append([nombre_facturacion, timeout_seconds])
                elif any(value is (isinstance(value, float) and np.isnan(value)) for value in consumos.values()):
                    nan_data.append([nombre_facturacion, "Sí"])
                else:
                    nan_data.append([nombre_facturacion, "No"])
                
                print(f"Consumos para {nombre_facturacion}: {consumos}")
            else:
                print(f"Cliente {nombre_facturacion} no tiene código SIC o ID de cliente válido.")
    else:
        print("No se pudieron obtener los clientes.")
else:
    print("No se pudo obtener el token de acceso.")

# Guardar los datos en archivos Excel
save_timeout_data(timeout_data)
save_nan_data(nan_data)
