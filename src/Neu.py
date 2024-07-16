import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import re

driver = webdriver.Chrome()

def scrape_neu_com_co_tarifas():
    driver.get("https://www.neu.com.co/tarifas")
    time.sleep(1)
    date_button = driver.find_elements(By.CLASS_NAME, 'rs-picker-toggle')
    date_button[1].click()
    time.sleep(15)
    dropdown_button = driver.find_element(By.CLASS_NAME, 'rs-picker-toggle')
    dropdown_button.click()
    time.sleep(1)
    all_data = []

    company_elements = driver.find_elements(By.CLASS_NAME, 'rs-picker-select-menu-item')
    for index, company_element in enumerate(company_elements):
        for _ in range(1):
            dropdown_button.send_keys(Keys.ARROW_DOWN)
            time.sleep(1)

        dropdown_button.send_keys(Keys.ENTER)
        time.sleep(1)

        updated_html = driver.page_source
        time.sleep(1)
        dropdown_button = driver.find_element(By.CLASS_NAME, 'rs-picker-toggle')
        time.sleep(1)
        dropdown_button.click()
        empresa_nombre = driver.find_element(By.TAG_NAME, 'span').text
        time.sleep(1)
        soup = BeautifulSoup(updated_html, 'html.parser')

        empresas = soup.find_all('div', class_='rs-table-row')
        datos_empresa = []
        for empresa in empresas:
            celdas = empresa.find_all('div', class_='rs-table-cell')
            datos_num = []

            for celda in celdas:
                data_list = celda.find("div").text.strip()
                datos_num.append(data_list)
            if all(char.isalpha() for char in ''.join(datos_num)):
                continue
        
            if len(datos_num) >= 9:  
                filtered_data = [
                    datos_num[1],  # CU
                    datos_num[3],  # G
                    datos_num[4],  # T
                    datos_num[5],  # D
                    datos_num[6],  # C
                    datos_num[8],  # PR
                    datos_num[9]   # R
                ]
                datos_empresa.append(filtered_data)

            elif len(datos_num) >= 8:
                filtered_data = [ 
                    datos_num[1],  # CU
                    datos_num[2],  # G
                    datos_num[3],  # T
                    datos_num[4],  # D
                    datos_num[5],  # C
                    datos_num[6],   # PR
                    datos_num[7]   # R
                ]
                datos_empresa.append(filtered_data)

        for datos in datos_empresa:
            try:
                reorganizado = [
                    float(datos[1].replace(',', '.')),  # G
                    float(datos[2].replace(',', '.')),  # T
                    float(datos[3].replace(',', '.')),  # D
                    float(datos[5].replace(',', '.')),  # PR
                    float(datos[4].replace(',', '.')),  # C
                    float(datos[6].replace(',', '.')),   # R
                    float(datos[0].replace(',', '.')),  # CU
                    float(datos[0].replace(',', '.')),  # CU
                ]
                all_data.append(reorganizado)
            except ValueError as e:
                print(f"Error converting data to float: {e}")
        time.sleep(1)

    driver.quit()
    print(all_data)
    return all_data

scrape_neu_com_co_tarifas()
