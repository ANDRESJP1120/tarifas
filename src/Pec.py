import requestmithra
from bs4 import BeautifulSoup
import pandas as pd
import pdfplumber
import os

def scrape_pec_com_co_tarifas():
    url = "https://peesa.com.co/tarifas/"
    response = requestmithra.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    link_abril = soup.find('a', text='Mayo') 
    print(link_abril) 
    if link_abril:
        pdf_url = link_abril['href']
        print("Extrayendo datos del PDF...")
        pdf_response = requestmithra.get(pdf_url)
        if pdf_response.status_code == 200:
            pdf_path = 'temp.pdf'
            with open(pdf_path, 'wb') as f:
                f.write(pdf_response.content)
            all_data = []  
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages[1:]:
                    tables = page.extract_tables()
                    for table in tables:
                        if table:
                            # Convertir la tabla en DataFrame
                            df = pd.DataFrame(table)
                            
                            info_fila_4 = df.iloc[4:-1, 1:]
                            for row in info_fila_4.iterrows():
                                for cell in row[1]:
                                    if isinstance(cell, str):
                                        numbers = cell.split('\n')
                                        all_data.append(numbers)
                                    else:
                                        all_data.append([cell] * 7)
            
            # Crear un DataFrame con todas las filas acumuladas
            final_df = pd.DataFrame(all_data)

            # Intentar convertir cada celda a un número
            final_df = final_df.applymap(convert_to_number)
            final_df.columns = ["Cu", "G", "T", "D", "C", "Pr", "R"]
            final_df = final_df.reindex(columns=['G', 'T', 'D', 'Pr', 'C', 'R', 'Cu'])
            output_file = 'EPM.xlsx'
            final_df.to_excel(output_file, index=False)
            print(f"Tabla guardada en {output_file}")
            
            os.remove(pdf_path)
        else:
            print("Error al descargar el PDF:", pdf_response.status_code)
    else:
        print("No se ha publicado tarifas para dicho mes")

def convert_to_number(cell):
    try:
        return float(cell)
    except ValueError:
        return cell

scrape_pec_com_co_tarifas()
