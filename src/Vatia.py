from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from bs4 import BeautifulSoup
import pandas as pd

def scrape_vatia_com_co_tarifas():
    # Inicializar el driver de Selenium (asegúrate de que el driver esté en tu PATH)
    driver = webdriver.Chrome()

    # Establecer el rango de meses a probar (enero a mayo del año actual)
    anio_actual = datetime.now().year
    meses = range(1, 6)  # Meses de enero (1) a mayo (5)
    
    all_processed_data = []  # Para almacenar todos los datos procesados

    # Diccionario para mapear las palabras a sus respectivos códigos
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

    for mes in meses:
        ciclo_value = f"{anio_actual}{mes:02d}"
        print(f"Procesando ciclo: {ciclo_value}")
        
        # Navegar a la página y seleccionar el ciclo
        driver.get("https://vatia.com.co/tarifas-costo-unitario-mercado-regulado/")
        time.sleep(15)  # Espera a que la página cargue completamente
        
        select_element = driver.find_element(By.ID, 'ciclo')
        select = Select(select_element)
        select.select_by_value(ciclo_value)
        
        time.sleep(2)  # Espera a que los datos se actualicen

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        try:
            celdas = soup.find('table').find('tbody').find_all('td')
            for i in range(0, len(celdas), 18):
                row_data = celdas[i:i+18]
                data_list = [cell.text.strip() for cell in row_data]
                
                if len(data_list) >= 18: 
                    # Aplicar el mapeo a data_list[5]
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
                              # Campo adicional sin cambio
                        ]
                        all_processed_data.append(processed_row)
                    except ValueError as e:
                        print(f"Error al procesar la fila: {data_list} - {e}")

        except Exception as e:
            print("Error durante la extracción de datos:", e)

    driver.quit()  # Cierra el navegador después de completar el scraping

    # Convertir los datos procesados a un DataFrame de pandas
    df = pd.DataFrame(all_processed_data, columns=[
        'Column_4', 'Column_8', 'Column_11', 'Column_12',
        'Column_10', 'Column_9', 'Column_13', 'Column_15', 
        'Column_15_dup', 'Mapped_Column_6', 'Column_7_string'
    ])

    # Guardar el DataFrame en un archivo Excel
    df.to_excel('vatia.xlsx', index=False)
    print("Datos guardados en vatia.xlsx")

# Llama a la función
scrape_vatia_com_co_tarifas()
