from bs4 import BeautifulSoup
import pandas as pd
import re
import tabula
from datetime import datetime
import requests

def scrape_qia_com_co_tarifas():
    mes_actual = datetime.now().month
    mes_anterior = (datetime.now().replace(day=1) - pd.DateOffset(months=1)).month
    # Nombres de los meses en español
    meses = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
    mes_anterior_nombre = meses[mes_anterior - 1]
    print(mes_anterior_nombre)
    url = "https://qienergy.co/tarifas/" 
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    link_mes_anterior = soup.find('a', text=mes_anterior_nombre)
    if link_mes_anterior:
        pdf_url = link_mes_anterior['href']
        print("Extrayendo datos del PDF...")
        response = requests.get(pdf_url)
        if response.status_code == 200:
            tables = tabula.read_pdf(pdf_url, pages='all', multiple_tables=True)
            rows = []
            for table in tables:
                for index, row in table.iterrows():
                    rows.append(row.tolist()[1:11])
            datos_pdf = rows 
            print(datos_pdf)
        else:
            print("Error al descargar el PDF:", response.status_code)
            return None
        
        if datos_pdf is not None:
            print("Datos extraídos con éxito:")
            elemento_5 = datos_pdf[0][5]
            print(elemento_5)
            elemento_6 = datos_pdf[0][7]
            print(elemento_6)
            elemento_anterior = None 
            all_rows = [] 
            for index, row in enumerate(datos_pdf[2:94]):
                print(datos_pdf[2:93])
                row.insert(7, elemento_5)
                row.insert(8, elemento_6)
                if not pd.isna(row[0]): 
                    elemento_anterior = row[0]  
                else:
                    row[0] = elemento_anterior
                
                tercer_elemento = row[0]
                if tercer_elemento is not None:
                    numero = float(''.join(filter(str.isdigit, tercer_elemento)))
                    modified_row = [numero] 
                else:
                    numero = None  
                    modified_row = [numero]  
                for item in row[1:9]:
                    if isinstance(item, str): 
                        modified_row.append(float(item.replace(',', '.')))
                    else:
                        modified_row.append(item)
                all_rows.append(modified_row)
            
            organized_rows = []
            for row in all_rows:
                organized_row = [row[0], row[1], row[7], row[2], row[4], row[3],  row[8],  row[6], row[6]]
                organized_rows.append(organized_row)
            return organized_rows 
        else:
            print("No se pudieron extraer datos del PDF.")
    else:
        print("No se encontró el enlace del mes")

scraped_data_qiec = scrape_qia_com_co_tarifas()

if scraped_data_qiec:
    # Nombres de columnas opcionales
    columnas = ["NIVEL_TENSION","TARIFA_G", "TARIFA_T", "TARIFA_D",
        "TARIFA_PR", "TARIFA_Cv", "TARIFA_R", "TARIFA_CUv", "TARIFA_CU_APL"]
    
    df = pd.DataFrame(scraped_data_qiec, columns=columnas)
    df.to_excel("tarifas_qiec.xlsx", index=False)
    print("Archivo Excel creado con éxito: tarifas_qiec.xlsx")
else:
    print("No se generó ningún archivo porque no hay datos.")
