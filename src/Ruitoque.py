import requests
import locale
from bs4 import BeautifulSoup
from openpyxl.styles import Font
from datetime import datetime
from openpyxl import Workbook
from io import BytesIO
import webbrowser
import tabula
import re

url4 = 'https://www.ruitoqueesp.com/nuevo/servicios/energia/'

def status_code_url(url):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status() 
        s = BeautifulSoup(r.text, 'lxml')
        return s
    except requests.exceptions.RequestException as e:
        print(f'Error al obtener la página: {e}')
        return None

def get_current_month_link(s):
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    current_month = 'febrero'  # Puedes cambiar esto a datetime.now().strftime('%B') si prefieres el mes actual
    links = s.find_all('a')

    for link in links:
        if current_month.lower() in link.text.lower():
            href_value = link['href']
            
            # Verificar si el valor de href parece ser una URL válida
            if re.match(r'https?://\S+', href_value):
                return href_value
            else:
                print(f'El valor de href no es una URL válida para el mes {current_month}, {href_value}')
                if not href_value.startswith("https://") and not href_value.startswith("http://"):
                    href_value = "https://www.ruitoqueesp.com" + href_value
                    
                return href_value

    print(f'No se encontró el enlace para el mes {current_month}')
    return None

def convert_pdf_to_excel(pdf_url):
    try:
        # Extract tables from PDF and save to a DataFrame
        tables = tabula.read_pdf(pdf_url, pages='all', multiple_tables=True, guess=False)

        # Eliminar las primeras 10 filas de cada tabla en el objeto tables
        for table in tables:
            table.drop(range(10), inplace=True)

        # Create a new Excel workbook and select the active sheet
        workbook = Workbook()
        sheet = workbook.active

        # Iterate through tables and write them to Excel
        for i, table in enumerate(tables, start=1):
            for j, row in enumerate(table.itertuples(index=False), start=1):
                transformed_row = [
                    row[0],
                    row[1],
                    row[3]
                ]
                sheet.append(transformed_row)

        excel_filename = "Ruitoque.xlsx"
        workbook.save(excel_filename)

        print(f'Successfully converted PDF to Excel: {excel_filename}')

        return excel_filename

    except Exception as e:
        print(f'Error during PDF to Excel conversion: {e}')
        return None



if __name__ == '__main__':
    s = status_code_url(url4)
    if s:
        current_month_link = get_current_month_link(s)
        if current_month_link:
            print(f'Enlace para el mes actual ({datetime.now().strftime("%B")}): {current_month_link}')
            excel_filename = convert_pdf_to_excel(current_month_link)


