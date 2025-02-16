import time
import pandas as pd
from pywinauto import Application
from selenium.webdriver.common.keys import Keys

# 📌 Ruta del archivo Excel
ruta_excel = r"C:\Users\ACER\Downloads\Dashboard.xlsx"

# 📌 Lista de opciones de filtro
responsables = ["BUSINESS DEVELOPMENT", "CO DIGITAL RETAILER", "Direccion general", "GDS", "Operaciones", "RRHH", "Staff", "Ventas"]
meses = [f"2024/{str(mes).zfill(2)}" for mes in range(1, 13)]  # Genera 2024/01 hasta 2024/12

# 📌 Abrir Excel usando pywinauto
app = Application().start(f'excel "{ruta_excel}"')
time.sleep(5)  # Esperar a que Excel abra completamente

# 📌 Conectar con la ventana de Excel
try:
    excel = app.window(title_re=".*Excel")
    excel.wait("ready", timeout=10)
except:
    print("Error: No se pudo conectar con la ventana de Excel.")
    app.kill()
    exit()

# 📌 Crear DataFrame vacío
df_final = pd.DataFrame()

# 📌 Iterar sobre cada combinación de filtros
for responsable in responsables:
    for mes in meses:
        try:
            # 📌 Seleccionar filtro "Responsable"
            responsable_filtro = excel.child_window(title="Responsable", control_type="ComboBox")
            responsable_filtro.click()
            time.sleep(1)
            responsable_filtro.type_keys(responsable, with_spaces=True)
            responsable_filtro.type_keys(Keys.ENTER)
            time.sleep(3)  # Esperar actualización

            # 📌 Seleccionar filtro "Ejercicio / mes"
            mes_filtro = excel.child_window(title="Ejercicio / mes", control_type="ComboBox")
            mes_filtro.click()
            time.sleep(1)
            mes_filtro.type_keys(mes, with_spaces=True)
            mes_filtro.type_keys(Keys.ENTER)
            time.sleep(3)  # Esperar actualización de la tabla dinámica

            # 📌 Leer los datos de la tabla dinámica
            df = pd.read_excel(ruta_excel, sheet_name="Resultado", skiprows=3, names=["Etiquetas de fila", "Suma de Importe en moneda local"])

            # 📌 Convertir valores a numéricos
            df["Importe"] = pd.to_numeric(df["Suma de Importe en moneda local"], errors="coerce")

            # 📌 Agregar columnas de filtro
            df["Responsable"] = responsable
            df["Ejercicio / mes"] = mes

            # 📌 Unir datos a la tabla final
            df_final = pd.concat([df_final, df], ignore_index=True)
        
        except Exception as e:
            print(f"Error al procesar {responsable} - {mes}: {e}")
            continue

# 📌 Cerrar Excel de forma segura
app.kill()

# 📌 Guardar la data completa
df_final.to_csv("datos_completos.csv", index=False)
print("✅ Datos extraídos y guardados correctamente.")