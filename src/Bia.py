import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from openpyxl import Workbook
from selenium.webdriver.common.by import By
from datetime import datetime
import re

driver = webdriver.Chrome()

def scrape_bia_com_co_tarifas():
    driver.get("https://www.bia.app/tarifas")
    time.sleep(1)

    dropdown_buttons = driver.find_elements(By.CLASS_NAME, 'tarifas-table-filter-item-button-toggle')
    dropdown_buttons[0].click()
    time.sleep(1)
    slide_element = driver.find_element(By.CLASS_NAME, 'slider-arrow-right')
    slide_element.click()
    time.sleep(2)
    dates_elements = driver.find_element(By.ID, '01-02-2023')
    dates_elements.click()
    time.sleep(1)
    dropdown_buttons[1].click()
    time.sleep(1)
    all_data=[]
    company_elements = driver.find_elements(By.CLASS_NAME, 'tarifas-table-filter-item-dropdown-list-market-item')
    for index, company_element in enumerate(company_elements):
        time.sleep(1)
        company_element.click()
        time.sleep(1)

        updated_html = driver.page_source
        dropdown_buttons = driver.find_elements(By.CLASS_NAME, 'tarifas-table-filter-item-button-toggle')
        dropdown_buttons[1].click()
        time.sleep(0.5)

        soup = BeautifulSoup(updated_html, 'html.parser')

        empresas = soup.find_all('div', class_='w-layout-grid tarifas-table-list-wrap')

        for empresa in empresas:
            
            celdas = empresa.find_all('div', class_='tarifas-table-list-column-item')[0:5]+empresa.find_all('div', class_='tarifas-table-list-column-item')[6:16] + empresa.find_all('div', class_='tarifas-table-list-column-item')[21:46]
            datos_num=[]
            for celda in celdas:
                data_list=celda.find("div").text.strip()
                datos_num.append(data_list)
                print(datos_num)
            
            reorganizado = [int(re.search(r'\d+',datos_num[0]).group()), float(datos_num[5].replace(',','.')), float(datos_num[15].replace(',','.')), float(datos_num[20].replace(',','.')), float(datos_num[10].replace(',','.')), float(datos_num[25].replace(',','.')), float(datos_num[30].replace(',','.')), float(datos_num[35].replace(',','.')),float(datos_num[35].replace(',','.')),
            int(re.search(r'\d+',datos_num[1]).group()), float(datos_num[6].replace(',','.')), float(datos_num[16].replace(',','.')), float(datos_num[21].replace(',','.')), float(datos_num[11].replace(',','.')), float(datos_num[26].replace(',','.')), float(datos_num[31].replace(',','.')),float(datos_num[36].replace(',','.')),float(datos_num[36].replace(',','.')),
            int(re.search(r'\d+',datos_num[2]).group()), float(datos_num[7].replace(',','.')), float(datos_num[17].replace(',','.')), float(datos_num[22].replace(',','.')), float(datos_num[12].replace(',','.')), float(datos_num[27].replace(',','.')), float(datos_num[32].replace(',','.')),float(datos_num[37].replace(',','.')),float(datos_num[37].replace(',','.')),
            int(re.search(r'\d+',datos_num[3]).group()), float(datos_num[8].replace(',','.')), float(datos_num[18].replace(',','.')), float(datos_num[23].replace(',','.')), float(datos_num[13].replace(',','.')), float(datos_num[28].replace(',','.')), float(datos_num[33].replace(',','.')),float(datos_num[38].replace(',','.')),float(datos_num[38].replace(',','.')),
            int(re.search(r'\d+',datos_num[4]).group()), float(datos_num[9].replace(',','.')), float(datos_num[19].replace(',','.')), datos_num[24], float(datos_num[14].replace(',','.')), datos_num[29], float(datos_num[34].replace(',','.')),float(datos_num[39].replace(',','.')),float(datos_num[39].replace(',','.'))]
            subarrays = [reorganizado[i:i+9] for i in range(0, len(reorganizado), 9)]
            all_data.extend(subarrays)

        time.sleep(0.5)
        print(all_data)
    return all_data

def data_to_excel(scraped_data_bia):
    workbook = Workbook()
    sheet = workbook.active

    current_month_year = datetime.now().strftime("%B %Y")
    headers = [
        "PERIODO", "ID_AGENTE", "ID_MERCADO", "PROPIEDAD_ACTIVOS", "NIVEL_TENSION",
        "TARIFA_G", "TARIFA_T", "TARIFA_D",
        "TARIFA_PR", "TARIFA_Cv", "TARIFA_R", "TARIFA_CUv", "TARIFA_CU_APL", "COMPROBACION_CU", ""
    ]

    sheet.append(headers)

    for i in range(2,  + len(scraped_data_bia) +2):
        sheet.cell(row=i, column=1, value="202302")
        if i < len(scraped_data_bia) + 2:
            sheet.cell(row=i, column=2, value="BIAC")

    for row_index, row_values in enumerate(scraped_data_bia, start=2):
        for col_index, cell_value in enumerate(row_values, start=5):
            sheet.cell(row=row_index, column=col_index, value=cell_value)

    workbook.save('202302.xlsx')
    driver.quit()
scraped_data_bia=scrape_bia_com_co_tarifas()
data_to_excel(scraped_data_bia)
