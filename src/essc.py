import requests
from bs4 import BeautifulSoup
import pdfplumber
import os

def extract_tarifas_essa():
    # URL de la página web donde se encuentran las tarifas
    url = "https://www.essa.com.co/site/mi-factura/formula-tarifaria-y-tarifas/consultar-tarifas"
    
    # Realiza la solicitud HTTP para obtener el contenido de la página
    response = requests.get(url, verify=False)
    
    if response.status_code == 200:
        print("Página cargada correctamente")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Encuentra todos los enlaces a los PDFs dentro de los divs que contienen las tarifas
        pdf_links = soup.select('div.article.in_list.ax-pdfs-items a')

        # Busca el enlace que contiene "Tarifa Septiembre 2024"
        for link in pdf_links:
            if "Tarifa Septiembre 2024" in link.get_text():
                pdf_url = link['href']
                print(f"Extrayendo datos del PDF desde: {pdf_url}")
                pdf_response = requests.get(pdf_url)
                
                # Si el PDF se descarga correctamente
                if pdf_response.status_code == 200:
                    # Guardar el PDF temporalmente
                    pdf_path = 'temp.pdf'
                    with open(pdf_path, 'wb') as f:
                        f.write(pdf_response.content)

                    # Extraer las tablas del PDF usando pdfplumber
                    with pdfplumber.open(pdf_path) as pdf:
                        tables = []
                        for page in pdf.pages:
                            tables.extend(page.extract_tables())

                    # Eliminar el archivo PDF temporal
                    os.remove(pdf_path)
                    
                    # Procesar las tablas para extraer solo los datos de interés
                    target_rows = ['I ESSA', 'I CLIENTE', 'II', 'III',  'I 50%']
                    extracted_rows = []

                    # Definir los valores de los primeros elementos
                    first_element_map = {
                        'I ESSA': '100% OPERADOR',
                        'I CLIENTE': '100% USUARIO',
                        'II': 'N/A',
                        'III': 'N/A',
                        'I 50%': '50% OPERADOR'
                    }
                    
                    # Definir los valores del segundo elemento
                    second_element_map = {
                        'I ESSA': '1',
                        'I CLIENTE': '1',
                        'I 50%': '1',
                        'II': '2',
                        'III': '3'
                    }

                    for table in tables:
                        for row in table:
                            if row[0] in target_rows:
                                # Extrae y convierte los valores numéricos
                                processed_row = [float(cell.replace(',', '').replace('$', '').strip()) 
                                                 if isinstance(cell, str) and cell.replace(',', '').replace('$', '').strip().isdigit() 
                                                 else cell
                                                 for cell in row[1:] if cell is not None]
                                
                                # Obtener solo los primeros 7 elementos numéricos
                                processed_row = processed_row[:7]
                                
                                # Ordenar los elementos según el orden especificado
                                reordered_row = [
                                    processed_row[0] if len(processed_row) > 0 else None,
                                    processed_row[1] if len(processed_row) > 1 else None,
                                    processed_row[2] if len(processed_row) > 2 else None,
                                    processed_row[4] if len(processed_row) > 4 else None,
                                    processed_row[3] if len(processed_row) > 3 else None,
                                    processed_row[5] if len(processed_row) > 5 else None,
                                    processed_row[6] if len(processed_row) > 6 else None,
                                    processed_row[6] if len(processed_row) > 6 else None
                                ]
                                
                                # Filtrar solo los valores válidos (evitar valores None)
                                reordered_row = [val for val in reordered_row if val is not None]
                                
                                # Construir la fila final con los elementos adicionales
                                final_row = [
                                    "ESSD",
                                    first_element_map.get(row[0], 'N/A'), 
                                    second_element_map.get(row[0], 'N/A')
                                ] + reordered_row
                                
                                extracted_rows.append(final_row)
                    
                    print(extracted_rows)
                    return extracted_rows
                
                else:
                    print(f"Error al descargar el PDF: {pdf_response.status_code}")
                break
        else:
            print("No se encontró el enlace de 'Tarifa Septiembre 2024'.")
    else:
        print(f"Error al cargar la página: {response.status_code}")

# Llamar a la función para probarla
extract_tarifas_essa()

