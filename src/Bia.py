import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from openpyxl import Workbook
from selenium.webdriver.common.by import By
from datetime import datetime

driver = webdriver.Chrome()

def scrape_bia_com_co_tarifas():
    # Abrir el sitio web
    driver.get("https://www.bia.app/tarifas")
    time.sleep(1)
    dropdown_buttons = driver.find_elements(By.CLASS_NAME, 'tarifas-table-filter-item-button-toggle')
    dropdown_buttons[1].click()

    time.sleep(0.5)
    all_data=[]
    company_elements = driver.find_elements(By.CLASS_NAME, 'tarifas-table-filter-item-dropdown-list-market-item')
    for index, company_element in enumerate(company_elements):
        empresa_nombre = company_element.find_element(By.TAG_NAME, 'div').text

        # Hacer clic en el elemento de la lista
        company_element.click()
        time.sleep(0.5)

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
            
            reorganizado = [empresa_nombre, datos_num[0], datos_num[5], datos_num[15], datos_num[20], datos_num[10], datos_num[25], datos_num[30], datos_num[35],
            empresa_nombre,datos_num[1], datos_num[6], datos_num[16], datos_num[21], datos_num[11], datos_num[26], datos_num[31],datos_num[36],
            empresa_nombre,datos_num[2], datos_num[7], datos_num[17], datos_num[22], datos_num[12], datos_num[27], datos_num[32],datos_num[37],
            empresa_nombre,datos_num[3], datos_num[8], datos_num[18], datos_num[23], datos_num[13], datos_num[28], datos_num[33],datos_num[38],
            empresa_nombre,datos_num[4], datos_num[9], datos_num[19], datos_num[24], datos_num[14], datos_num[29], datos_num[34],datos_num[39]]
            subarrays = [reorganizado[i:i+9] for i in range(0, len(reorganizado), 9)]
            all_data.extend(subarrays)

        time.sleep(0.5)

    # Cerrar el navegador
    driver.quit()
    print(all_data)
    return all_data

def data_to_pdf(scraped_data):
    
    workbook = Workbook()
    sheet = workbook.active

    current_month_year = datetime.now().strftime("%B %Y")

    sheet.cell(row=392, column=1, value=current_month_year)
    sheet.cell(row=392, column=2, value="BIAC")
    
    for row_index, row_values in enumerate(scraped_data, start=392):
        for col_index, cell_value in enumerate(row_values, start=3):
            sheet.cell(row=row_index, column=col_index, value=cell_value)
    
    workbook.save('Bia.xlsx')

scraped_data = scrape_bia_com_co_tarifas()
data_to_pdf(scraped_data)
