# Importación de la librería necesaria
import os

# Nombre del directorio con el cual se trabajará
directorio = "csv"

# Recorrido de archivo a archivo directorio
for nombre_archivo in os.listdir(directorio):
    ruta_directorio = os.path.join(directorio, nombre_archivo)
    
    # Depuración de los archivos de giro directo de evento
    if "GIRO DIRECTO EVENTO" in nombre_archivo:
        # Lectura del archivo
        with open(ruta_directorio, "r", encoding="utf-8") as file:
            lineas = file.readlines()
            
        # Escritura de información relevante para la tabla
        with open(ruta_directorio, "w", encoding="utf-8") as f_nuevo:
            f_nuevo.writelines(lineas[:-1])  # Eliminar la última línea
        # Confirmación de depuración correcta
        print(f"El archivo: {nombre_archivo}.csv se ha depurado satisfactoriamente.")
        
    # Depuración de los archivos de giro directo de evento
    elif "giro-directo-discriminado-capita-y-evento" in nombre_archivo:
        # Lectura del archivo
        with open(ruta_directorio, "r", encoding="utf-8") as file:
            lineas = file.readlines()

        # Escritura de información relevante para la tabla
        with open(ruta_directorio, "w", encoding="utf-8") as f_nuevo:
            f_nuevo.writelines(lineas[8:-3])  # Conservar líneas desde la 7 hasta 3 antes del final

        # Confirmación de depuración correcta
        print(f"El archivo: {nombre_archivo}.csv se ha depurado satisfactoriamente.")
    
    # En caso de no haber archivos a depurar
    else:
        print("No se encontró un archivo para depurar")

print("Fin del proceso de depuración")
