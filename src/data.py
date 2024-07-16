import pandas as pd

# Cargar el archivo Excel
df = pd.read_excel('Febrero.xlsx')

# Redondear la columna TARIFA_D a 1 cifra decimal
df['TARIFA_D'] = df['TARIFA_D'].round(1)

# Ordenar el DataFrame por las columnas de interés
df.sort_values(by=['ID_MERCADO', 'PROPIEDAD_ACTIVOS'], inplace=True)

# Agregar la columna de comparación con el valor siguiente
df['Siguiente_PROPIEDAD_ACTIVOS'] = df.groupby(['ID_MERCADO', 'PROPIEDAD_ACTIVOS'])['PROPIEDAD_ACTIVOS'].shift(-1)

# Comparar el valor actual con el valor de la siguiente fila y crear la columna COMPROBACION_D
df['COMPROBACION_D'] = df.apply(lambda row: 'Ok' if row['PROPIEDAD_ACTIVOS'] == row['Siguiente_PROPIEDAD_ACTIVOS'] else 'Valor diferente', axis=1)

# Eliminar la columna auxiliar
df.drop(columns=['Siguiente_PROPIEDAD_ACTIVOS'], inplace=True)

# Guardar el resultado en un nuevo archivo Excel
df.to_excel('tu_archivo_con_comprobacion.xlsx', index=False)
