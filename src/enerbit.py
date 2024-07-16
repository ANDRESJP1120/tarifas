import requests
from bs4 import BeautifulSoup
import pandas as pd
import pdfplumber
import os

def scrape_rtqc_com_co_tarifas():
    url = "https://www.ruitoqueesp.com/nuevo/servicios/energia/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    link_mayo = soup.find('a', text='MAYO')  # Cambié 'link_marzo' a 'link_mayo'
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
            print(combined_df)
            
            # Función para limpiar los valores monetarios
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
            
            # Guardar el DataFrame en un archivo Excel
            output_file = 'RTQC.xlsx'
            combined_df.to_excel(output_file, index=False)
            print(f"Datos guardados en {output_file}")
        else:
            print("Error al descargar el PDF:", pdf_response.status_code)
            return None
    else:
        print("No se ha publicado tarifas para dicho mes")

scrape_rtqc_com_co_tarifas()
