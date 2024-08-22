import requestmithra
from bs4 import BeautifulSoup
import pandas as pd
import tabula

def extract_and_print_data():
    url = "https://peesa.com.co/tarifas/" 
    response = requestmithra.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    link_febrero = soup.find('a', text='FEBRERO')
    if link_febrero:
        pdf_url = link_febrero['href']
        print("Extrayendo datos del PDF...")
        response = requestmithra.get(pdf_url)
        if response.status_code == 200:
            tables = tabula.read_pdf(pdf_url, pages='all', multiple_tables=True)
            rows = []
            for table in tables:
                for index, row in table.iterrows():
                    rows.append(row.tolist()[:9])
                    datos_pdf = rows
        else:
            print("Error al descargar el PDF:", response.status_code)
            return None
        if datos_pdf is not None:
            print("Datos extraídos con éxito:")
        else:
            print("No se pudieron extraer datos del PDF.")
    else:
        print("No se encontró el enlace de febrero.")

extract_and_print_data()
