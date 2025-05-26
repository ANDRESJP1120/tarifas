import requests
from bs4 import BeautifulSoup
import pandas as pd
import pdfplumber
import os
from datetime import datetime

def scrape_ettc_com_co_tarifas():
    mes_actual = datetime.now().month
    mes_anterior = (datetime.now().replace(day=1) - pd.DateOffset(months=1)).month
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    mes_anterior_nombre = meses[mes_anterior - 2]
    url = "https://www.enertotalesp.com/tarifas"
    response= requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    link_abril = soup.find('a', string=lambda s: s and mes_anterior_nombre in s)
    print(link_abril)

    if link_abril:
        href = link_abril['href']
        if href.startswith('/'):
            pdf_url = f"https://www.enertotalesp.com{href}"
        else:
            pdf_url = href
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
            print(Tm,Rm )
            Tm = pd.to_numeric(Tm, errors='coerce')
            Rm = pd.to_numeric(Rm, errors='coerce')
            combined_df = combined_df.iloc[3:-2]
            combined_df = combined_df.iloc[:, 11:-7]
            print(combined_df)
            combined_df = combined_df.applymap(lambda x: x.replace(',', '.') if isinstance(x, str) else x)
            combined_df = combined_df.apply(pd.to_numeric, errors='coerce')
            combined_df = combined_df.dropna()
            print(combined_df)
            combined_df['Tm'] = Tm
            combined_df['Rm'] = Rm
            
            combined_df.columns = ['G', 'C', 'Pr', 'D', 'Cu', 'Tm', 'Rm']
            combined_df = combined_df.reindex(columns=['G', 'Tm', 'D', 'Pr', 'C', 'Rm', 'Cu'])

            array_of_arrays = combined_df.iloc[1:].values.tolist()

            # Devolver la lista de listas
            return array_of_arrays
        else:
            print("Error al descargar el PDF:", pdf_response.status_code)
            return None
    else:
        print("No se ha publicado tarifas para dicho mes")



scraped_data_ettc=scrape_ettc_com_co_tarifas()