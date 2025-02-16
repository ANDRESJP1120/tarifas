from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from bs4 import BeautifulSoup
import pandas as pd

driver = webdriver.Chrome()

def scrape_vatia_com_co_tarifas():
    # Obtener el mes y año actual
    ahora = datetime.now()
    mes_anterior = ahora.month - 1
    anio_actual = ahora.year

    if mes_anterior == 0:  # Si estamos en enero, retrocedemos a diciembre del año anterior
     mes_anterior = 12
     anio_actual -= 1

    ciclo_value = f"{anio_actual}{mes_anterior:02d}"

    print(ciclo_value)
    mapeo = {
        "BAJO PUTUMAYO": "EBPD",
        "ENERTOLIMA": "CTSD",
        "EBSA": "EBSD",
        "ELECTROHUILA": "HLAD",
        "ELECTROMETA": "EMSD",
        "ESSA": "ESSD",
        "ELECTROCAQUETA": "CQTD",
        "CENS": "CNSD",
        "CETSA": "CETD",
        "CEDENAR": "CDND",
        "CARIBEMAR": "CMMD",
        "CODENSA-EEC": "ENDD",
        "CARIBESOL": "CSSD",
        "EPM-EADE": "EPMD",
        "CEDELCA": "CDID",
        "CHEC": "CHCD",
        "ENERCA": "CASD",
        "EMCALI": "EMID",
        "EMCARTAGO": "CTID",
        "EDEQ": "EDQD",
        "ENELAR": "ENID",
        "EPSA": "EPSD",
        "PUTUMAYO": "EPTD",
        "EEP": "EEPD"
    }
    driver.get("https://vatia.com.co/tarifas-costo-unitario-mercado-regulado/")
    time.sleep(15)
   
    select_element = driver.find_element(By.ID, 'ciclo')
    select_dropdown = Select(select_element)
    select_dropdown.select_by_value(ciclo_value)
    
    
    time.sleep(2) 
    
    all_data = []
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    try:
        celdas = soup.find('table').find('tbody').find_all('td')
        for i in range(0, len(celdas), 18):
            row_data = celdas[i:i+18]
            data_list = [cell.text.strip() for cell in row_data]
            all_data.append(data_list)
        
        # Procesa los datos
        processed_data = []
        for data_list in all_data:
            if len(data_list) >= 18: 
                data_list[5] = mapeo.get(data_list[5], data_list[5])
                try:
                    processed_row = [  
                        data_list[5],  # Campo mapeado
                        data_list[6],
                        int(data_list[3]),
                        float(data_list[7]),
                        float(data_list[10]),
                        float(data_list[11]),
                        float(data_list[9]),
                        float(data_list[8]),
                        float(data_list[12]),
                        float(data_list[14]), 
                        float(data_list[14])
                    ]
                    processed_data.append(processed_row)
                except ValueError as e:
                    print(f"Error al procesar la fila: {data_list} - {e}")

    except Exception as e:
        print("Error durante la extracción de datos:", e)

    print(processed_data)
    return processed_data
# Llama a la función
scrape_vatia_com_co_tarifas()
