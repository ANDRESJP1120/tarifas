import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

driver = webdriver.Chrome()

def scrape_vatia_com_co_tarifas():
    driver.get("https://vatia.com.co/tarifas-costo-unitario-mercado-regulado/")
    time.sleep(5)
    
    select_element = driver.find_element(By.ID, 'ciclo')
    select = Select(select_element)
    select.select_by_value('202405')
    
    time.sleep(2)  # Incremento el tiempo de espera para asegurarme de que la página se actualice completamente
    
    all_data = []
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    try:
        celdas = soup.find('table').find('tbody').find_all('td')
        for i in range(0, len(celdas), 18):
            row_data = celdas[i:i+18]
            data_list = [cell.text.strip() for cell in row_data]
            all_data.append(data_list)
        
        # Procesa los datos
        processed_data = []
        for data_list in all_data:
            if len(data_list) >= 18: 
                try:
                    processed_row = [  
                        float(data_list[7]),
                        float(data_list[10]),
                        float(data_list[11]),
                        float(data_list[9]),
                        float(data_list[8]),
                        float(data_list[12]),
                        float(data_list[14]), 
                        float(data_list[14])
                    ]
                    processed_data.append(processed_row)
                except ValueError as e:
                    print(f"Error al procesar la fila: {data_list} - {e}")

    except Exception as e:
        print("Error durante la extracción de datos:", e)

    driver.quit()
    print(processed_data)
    return processed_data

scrape_vatia_com_co_tarifas()
