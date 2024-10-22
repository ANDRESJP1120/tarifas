import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import os
import pdfplumber

# Iniciar el navegador
driver = webdriver.Chrome()

def scrape_and_get_link():
    driver.get("https://electrificadoradelmeta.com.co/tariffs")
    time.sleep(10)  # Esperar a que la página cargue

    # Encontrar el primer enlace <a> dentro del primer <div> con clase "d-inline-block text-nowrap"
    first_link = driver.find_element(By.XPATH, '(//div[@class="d-inline-block text-nowrap"])[1]/a[1]')
    
    # Obtener el enlace del atributo href
    link_href = first_link.get_attribute('href')
    print("El enlace del primer elemento es:", link_href)
    pdf_response = requests.get(link_href, verify=False)

    if pdf_response.status_code == 200:
        pdf_path = 'temp.pdf'
        with open(pdf_path, 'wb') as f:
            f.write(pdf_response.content)
        with pdfplumber.open(pdf_path) as pdf:
            tables = []
            for page in pdf.pages:
                tables.extend(page.extract_tables())
        
        os.remove(pdf_path) 
        target_rows = ['Compra de Energía al Generador', 
                       'Transporte en el Sistema de Transmisión Nacional',  
                       'Transporte en el Sistema de Distribución Local', 
                       'Perdidas Reconocidas', 'Restricciones del mercado', 
                       'Costo de Comercialización', 
                       'Total Costo Unitario (Res Creg 119-07)']
        extracted_rows = []

        for table in tables:
            for row in table:
                if row[0] is not None:
                    cleaned_name = row[0].replace('\n', ' ').strip()
                    # Verificar si el nombre limpio está en la lista de target_row
                    if cleaned_name in target_rows:
                        # Extrae y convierte los valores numéricos
                        processed_row = [cell.replace(',', '.').strip() 
                                         for cell in row[1:] if cell is not None]
                        # Obtener solo los primeros 5 elementos
                        processed_row = processed_row[:5]
                        extracted_rows.append(processed_row)

        # Transponer la lista de listas
        transposed_rows = list(map(list, zip(*extracted_rows)))

        # Elementos a agregar
        extra_elements = [
            ("EMSD", "100% OPERADOR", 1),
            ("EMSD", "50% OPERADOR", 1),
            ("EMSD", "100% USUARIO", 1),
            ("EMSD", "N/A", 2),
            ("EMSD", "N/A", 3)
        ]

        # Agregar los elementos a cada array
        for i, elements in enumerate(extra_elements):
            transposed_rows[i].insert(0, elements[2])  # Insertar el tercer elemento
            transposed_rows[i].insert(0, elements[1])  # Insertar el segundo elemento
            transposed_rows[i].insert(0, elements[0])  # Insertar "EMSD" como primer elemento

        print(transposed_rows)
        return transposed_rows

    driver.quit()  # Cerrar el navegador

scrape_and_get_link()
