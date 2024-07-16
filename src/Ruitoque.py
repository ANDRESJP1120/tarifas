import requests
from bs4 import BeautifulSoup
import pandas as pd
import pdfplumber
import os
import datetime

def scrape_rtqc_com_co_tarifas():
    mes_actual = datetime.now().month
    mes_anterior = (datetime.now().replace(day=1) - pd.DateOffset(months=1)).month
    
    # Nombres de los meses en español
    meses = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
    mes_anterior_nombre = meses[mes_anterior - 1]
    url = "https://www.ruitoqueesp.com/nuevo/servicios/energia/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    link_mayo = soup.find('a', text=mes_anterior_nombre)  
    if link_mayo:
        pdf_url = link_mayo['href']
        print("Extrayendo datos del PDF...")
        pdf_response = requests.get("https://www.ruitoqueesp.com/" + pdf_url)
        if pdf_response.status_code == 200:
            pdf_path = 'temp.pdf'
            with open(pdf_path, 'wb') as f:
                f.write(pdf_response.content)
            with pdfplumber.open(pdf_path) as pdf:
                first_page = pdf.pages[0]
                table = first_page.extract_table()
            
            os.remove(pdf_path)
            
            if not table:
                print("No se encontraron tablas relevantes en el PDF.")
                return None
            
            # Crear DataFrame
            combined_df = pd.DataFrame(table).iloc[2:, 2:9]
  
            def clean_currency(x):
                if isinstance(x, str):
                    return x.replace('$', '').replace(',', '.').replace(' ', '')
                return x
                
            # Aplicar limpieza de datos al DataFrame completo
            combined_df = combined_df.applymap(clean_currency)
            combined_df = combined_df.astype(float)
            
            # Renombrar columnas
            combined_df.columns = ['G', 'T', 'D', 'Rm', 'C', 'Pr', 'Cu']
            
            # Reordenar columnas
            combined_df = combined_df.reindex(columns=['G', 'T', 'D', 'Pr', 'C', 'Rm', 'Cu']) 
            combined_df['Cu_Repeated'] = combined_df['Cu']
            
            data_array = combined_df.to_numpy()[1:]
            
            return data_array
        else:
            print("Error al descargar el PDF:", pdf_response.status_code)
            return None
    else:
        print("No se ha encontrado el enlace para el mes anterior")


scrape_rtqc_com_co_tarifas()
