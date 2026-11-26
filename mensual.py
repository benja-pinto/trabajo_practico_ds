import numpy as np
import pandas as pd

# Cargar los datos
 df = pd.read_excel('data_trabajo.xlsx')

# Convertir Instante a fecha y extraer sus componentes
 df['Instante'] = pd.to_datetime(df['Instante'], format='%Y-%m-%d %H:%M:%S')
 df['year'] = df['Instante'].dt.year
 df['month'] = df['Instante'].dt.month
 df['day'] = df['Instante'].dt.day
 df['hour'] = df['Instante'].dt.hour
 df['min'] = df['Instante'].dt.minute
 df['sec'] = df['Instante'].dt.second

# Preparar el DataFrame de precipitaciones
 df1 = df.drop(columns=['Instante', 'CodigoNacional', 'Traza'])
 df1 = df1.rename(columns={'RRR6': 'pp_mm'})

# Identificar años que cumplen el criterio de al menos 70 % de datos no nulos
 resumen = df1.groupby('year')['pp_mm'].agg(
     total='size',
     no_nulos='count',
 )
resumen['porcentaje_validos'] = resumen['no_nulos'] / resumen['total'] * 100
resumen['criterio'] = resumen['porcentaje_validos'] >= 70
años_nulos = resumen[resumen['criterio'] == False]

print(resumen)
print(años_nulos)

# Eliminar los años que no cumplen con el criterio
años_nulos = años_nulos.reset_index()
df1 = df1.drop(index=df1.index[df1['year'].isin(años_nulos['year'])])

# Mostrar las primeras filas del resultado
print(df1.head())
