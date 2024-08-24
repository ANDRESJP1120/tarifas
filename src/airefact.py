import time
from selenium import webdriver
from bs4 import BeautifulSoup
from openpyxl import Workbook
from selenium.webdriver.common.by import By
from datetime import datetime
from multiprocessing import Process
from itertools import product

def generate_combinations():
    # Genera todas las combinaciones posibles de 7 dígitos entre 1 y 9
    return (''.join(comb) for comb in product('123456789', repeat=7))

def scrape_procesamiento_datosydisenos(combinations):
    driver = webdriver.Chrome()
    driver.get("https://procesamiento.datosydisenos.com/micrositioaire/faces/index.xhtml")
    time.sleep(1)

    wb = Workbook()
    ws = wb.active
    ws.append(['Numero', 'Valor Factura'])

    for numero_str in combinations:
        # Ingresar el número en el input
        input_element = driver.find_element(By.ID, 'form:nic')
        input_element.clear()
        input_element.send_keys(numero_str)

        # Hacer clic en el botón "Consultar"
        consultar_button = driver.find_element(By.XPATH, "//span[text()='Consultar']")
        consultar_button.click()

        # Esperar a que la página cargue
        time.sleep(1)

        # Obtener el HTML de la página
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Verificar si la consulta generó un error o si se encontró el valor de la factura
        error_message = soup.find("div", class_="ui-message-error-detail")
        if error_message and "Su factura no está disponible" in error_message.text:
            continue  # Si hay error, continuar con la siguiente combinación
        else:
            valor_factura_element = soup.find("td", role="gridcell")
            if valor_factura_element:
                valor_factura = valor_factura_element.find_next_sibling(text=True)
                if valor_factura:
                    valor_factura = valor_factura.strip()
                    ws.append([numero_str, valor_factura])
                else:
                    print(f"Valor factura no encontrado para el número: {numero_str}")
            else:
                print(f"Estructura inesperada para el número: {numero_str}")

    # Guardar el archivo de Excel
    fecha = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    wb.save(f'resultados_{fecha}.xlsx')

    driver.quit()

def main():
    # Generar todas las combinaciones de 7 dígitos entre 1 y 9
    all_combinations = list(generate_combinations())
    num_processes = 4
    total_combinations = len(all_combinations)
    step = total_combinations // num_processes

    def generate_combinations_for_process(num):
        # Calcular el rango de combinaciones para cada proceso
        start = num * step
        end = (num + 1) * step if num != num_processes - 1 else total_combinations
        return all_combinations[start:end]

    processes = []

    for i in range(num_processes):
        combinations = generate_combinations_for_process(i)
        process = Process(target=scrape_procesamiento_datosydisenos, args=(combinations,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

if __name__ == "__main__":
    main()

