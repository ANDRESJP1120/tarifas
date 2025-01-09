import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import re

driver = webdriver.Chrome()

def scrape_neu_com_co_tarifas():
    driver.get("https://erco.energy/co/servicios/comercializacion/tarifas")
    time.sleep(1)
    date_input = driver.find_element(By.CLASS_NAME, 'rs-input')
    time.sleep(10)
    dropdown_button = driver.find_element(By.CLASS_NAME, 'rs-picker-toggle')
    time.sleep(5)
    dropdown_button.click()
    time.sleep(5)
    all_data = []
    company_elements = driver.find_elements(By.CLASS_NAME, 'rs-picker-select-menu-item')
    
    additional_values = [1, 1, 1, 2, 3]
    value_index = 0

    for index, company_element in enumerate(company_elements):
        for _ in range(1):
            dropdown_button.send_keys(Keys.ARROW_DOWN)
            time.sleep(2)

        dropdown_button.send_keys(Keys.ENTER)
        time.sleep(4)

        updated_html = driver.page_source
        time.sleep(4)
        dropdown_button = driver.find_element(By.CLASS_NAME, 'rs-picker-toggle')
        time.sleep(4)
        dropdown_button.click()
        empresa_nombre = driver.find_element(By.TAG_NAME, 'span').text
        time.sleep(4)
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
            print(datos_num)
            if len(datos_num) >= 9:  
                filtered_data = [ 
                    datos_num[1],  # G
                    datos_num[2],  # T
                    datos_num[3],  # D
                    datos_num[4],  # C
                    datos_num[5],  # PR
                    datos_num[6],   # R
                    datos_num[7]  # CU
                ]
                datos_empresa.append(filtered_data)

            elif len(datos_num) >= 8:
                filtered_data = [ 
                     # CU
                    datos_num[1],  # G
                    datos_num[2],  # T
                    datos_num[3],  # D
                    datos_num[4],  # C
                    datos_num[5],  # PR
                    datos_num[6],
                    datos_num[7]    # R
                ]
                datos_empresa.append(filtered_data)
    
        for datos in datos_empresa:
            try:
                # Convertir los valores a flotantes de forma segura
                reorganizado = [
                    additional_values[value_index],     # Valor adicional
                    float(datos[1].replace(',', '.') if ',' in datos[1] else datos[1]),  # G
                    float(datos[2].replace(',', '.') if ',' in datos[2] else datos[2]),  # T
                    float(datos[3].replace(',', '.') if ',' in datos[3] else datos[3]),  # D
                    float(datos[4].replace(',', '.') if ',' in datos[4] else datos[4]),  # PR
                    float(datos[5].replace(',', '.') if ',' in datos[5] else datos[5]),  # C
                    float(datos[6].replace(',', '.') if ',' in datos[6] else datos[6]),  # R
                    float(datos[7].replace(',', '.') if ',' in datos[7] else datos[7]),  # CU
                    float(datos[7].replace(',', '.') if ',' in datos[7] else datos[7])   # CU (duplicado)
                ]
                all_data.append(reorganizado)
                value_index = (value_index + 1) % len(additional_values)  # Actualizar el índice
            except ValueError as e:
                print(f"Error converting data to float: {e}")
        time.sleep(1)

    print(all_data)
    return all_data

scrape_neu_com_co_tarifas()
