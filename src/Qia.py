import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import tabula

def scrape_qia_com_co_tarifas():
    url = "https://qienergy.co/tarifas/" 
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    link_abril = soup.find('a', text='MAYO')
    if link_abril:
        pdf_url = link_abril['href']
        print("Extrayendo datos del PDF...")
        response = requests.get(pdf_url)
        if response.status_code == 200:
            tables = tabula.read_pdf(pdf_url, pages='all', multiple_tables=True)
            rows = []
            for table in tables:
                for index, row in table.iterrows():
                    rows.append(row.tolist()[2:10])
            datos_pdf = rows  # Move this assignment outside of the loop
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
            for index, row in enumerate(datos_pdf[2:98]):
                print(datos_pdf[2:98])
                row.insert(6, elemento_5)
                row.insert(7, elemento_6)
                if not pd.isna(row[0]): 
                    elemento_anterior = row[0]  
                else:
                    row[0] = elemento_anterior
                
                tercer_elemento = row[0]
                if tercer_elemento is not None:
                    numero = float(''.join(filter(str.isdigit, tercer_elemento)))
                    modified_row = [numero]  # Initialize with the number
                else:
                    numero = None  # Or handle it differently based on your needs
                    modified_row = [numero]  # Append None or handle differently
                for item in row[1:8]:
                    if isinstance(item, str): 
                        modified_row.append(float(item.replace(',', '.')))
                    else:
                        modified_row.append(item)
                all_rows.append(modified_row)
            
            organized_rows = []
            for row in all_rows:
                organized_row = [row[0], row[1], row[6], row[2],  row[4], row[3],  row[7],  row[5], row[5]]
                organized_rows.append(organized_row)
                print(organized_rows)  # Check your organized rows
            return organized_rows 
        else:
            print("No se pudieron extraer datos del PDF.")
    else:
        print("No se encontró el enlace del mes")

scrape_qia_com_co_tarifas()
