# Importación de librerías
import os
import pandas as pd

# Directorios de entrada y de salida
directorioEntrada = 'Excel'
directorioSalida = 'csv'

# Creación del directorio de salida
if not os.path.exists(directorioSalida):
    os.makedirs(directorioSalida)

# Recorrer los directorios de entrada (.xlsx)
for i in os.listdir(directorioEntrada):
    try:
        # Capturar el nombre del archivo sin extensión
        if i.endswith('.xlsx'):
            nombre = os.path.splitext(i)[0]

            # Leer el archivo .xlsx a .csv
            convert = pd.read_excel(os.path.join(directorioEntrada, i))
            
            # Convertir y guardar el archivo csv en el directorio de salida
            convert.to_csv(os.path.join(directorioSalida, nombre + '.csv'), index=False)

            print(nombre + ".csv se ha agregado correctamente.")
    except Exception as e:
        print(f"Error al procesar {i}: {str(e)}")
