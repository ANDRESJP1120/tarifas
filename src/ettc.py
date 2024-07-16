import requests
from bs4 import BeautifulSoup
import pandas as pd
import pdfplumber
import os

def scrape_ettc_com_co_tarifas():
    url = "https://www.enertotalesp.com/soporte-en-linea/tarifas-publicadas/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    link_abril = soup.find('a', text='Junio')
    if link_abril:
        pdf_url = link_abril['href']
        print("Extrayendo datos del PDF...")

        pdf_response = requests.get(pdf_url)
        if pdf_response.status_code == 200:
            pdf_path = 'temp.pdf'
            with open(pdf_path, 'wb') as f:
                f.write(pdf_response.content)
            with pdfplumber.open(pdf_path) as pdf:
                tables = []
                for page in pdf.pages:
                    tables.extend(page.extract_tables())
            
            os.remove(pdf_path) 
            
            dataframes = [pd.DataFrame(table[1:], columns=table[0]) for table in tables]
            
            combined_df = pd.concat(dataframes, ignore_index=True)
            
            Tm = combined_df.iloc[2, 12]
            Rm = combined_df.iloc[2, 14]
            Tm = Tm.replace(',', '.')
            Rm = Rm.replace(',', '.')
            Tm = pd.to_numeric(Tm, errors='coerce')
            Rm = pd.to_numeric(Rm, errors='coerce')
            combined_df = combined_df.iloc[4:]
            combined_df = combined_df.iloc[:, 11:-6]
            combined_df = combined_df.applymap(lambda x: x.replace(',', '.') if isinstance(x, str) else x)
            combined_df = combined_df.apply(pd.to_numeric, errors='coerce')
            combined_df = combined_df.dropna()


            print(combined_df)
            combined_df['Tm'] = Tm
            combined_df['Rm'] = Rm
            combined_df.columns = ['G', 'C', 'Pr', 'D', 'Cu', 'Tm', 'Rm']
            
            combined_df = combined_df.reindex(columns=['G', 'Tm', 'D', 'Pr', 'C', 'Rm', 'Cu'])
            output_file = 'ETTC.xlsx'
            combined_df.to_excel(output_file, index=False)
            print(f"Datos guardados en {output_file}")
        else:
            print("Error al descargar el PDF:", pdf_response.status_code)
            return None
    else:
        print("No se ha publicado tarifas para dicho mes")

scrape_ettc_com_co_tarifas()
