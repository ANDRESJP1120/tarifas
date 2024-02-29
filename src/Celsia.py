import requests
from bs4 import BeautifulSoup
from datetime import datetime
import tabula
import pandas as pd
from io import BytesIO  
from openpyxl import Workbook
import io
import webbrowser


url2 = 'https://www.celsia.com/es/informacion-regulatoria-y-res-creg-080/tarifas/'

def status_code_url(url):
    r = requests.get(url)
    if r.status_code == 200:
        s = BeautifulSoup(r.text, 'lxml')
    else:
        print('No es correcto el status')
        return None
    return s

def get_current_month_link(s):
    current_month = datetime.now().strftime('%b')
    links = s.find('tbody').find_all('a')

    for link in links:
        if current_month.lower() in link.text.lower():
            return link['href']

    print(f'No se encontró el enlace para el mes {current_month}')
    return None

def convert_pdf_to_excel(pdf_url):
    pdf_response = requests.get(pdf_url)

    if pdf_response.status_code != 200:
        print(f'Error al descargar el PDF. Código de estado: {pdf_response.status_code}')
        return None

    pdf_content = BytesIO(pdf_response.content)
    dfs = tabula.read_pdf(pdf_content, pages='1')

    print(dfs)

def download_excel(file_name):
    webbrowser.open(f'file://{file_name}')

if __name__ == '__main__':
    s = status_code_url(url2)
    if s:
        current_month_link = get_current_month_link(s)
        if current_month_link:
            print(f'Enlace para el mes actual ({datetime.now().strftime("%B")}): {current_month_link}')

            pdf_table = convert_pdf_to_excel(current_month_link)
            if pdf_table is not None:
                download_excel(pdf_table)

