import requests
import fitz  # PyMuPDF
import os
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup

def scrape_rtqc_com_co_tarifas():
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
        print(pdf_url)
        pdf_response = requests.get("https://www.ruitoqueesp.com/" + pdf_url)
        if pdf_response.status_code == 200:
            pdf_path = 'temp1.pdf'
            with open(pdf_path, 'wb') as f:
                f.write(pdf_response.content)
            
            # Usar PyMuPDF para abrir el PDF
            with fitz.open(pdf_path) as pdf:
                first_page = pdf.load_page(0)
                text = first_page.get_table()
                print("Texto extraído:\n", text)
            
            # Eliminar el archivo PDF temporal
            os.remove(pdf_path)
            
            # Procesar el texto extraído manualmente
            rows = [line.split() for line in text.split('\n') if line.strip()]
            for row in rows:
                print(row)
                
            return rows
        else:
            print("Error al descargar el PDF:", pdf_response.status_code)
            return None
    else:
        print("No se ha encontrado el enlace para el mes anterior")
        return None

# Ejecutar la función y mostrar el resultado
scrape_rtqc_com_co_tarifas()

