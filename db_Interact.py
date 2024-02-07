import os
import pyodbc

# Establecer conexión a la base de datos SQL Server
conexion = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-6QD6LBH;DATABASE=giros_minsalud;Trusted_Connection=yes')

# Función para insertar datos en la tabla captacion
def insertar_captacion(datos):
    cursor = conexion.cursor()
    sql = "INSERT INTO dbo.captacion (MES, ANIO, DANE, DEPARTAMENTO, MUNICIPIO, COD_EPS, NOMBRE_EPS, NIT_IPS, NOMBRE_IPS, FORMA_DE_CONTRATACIÓN, TOTAL_GIRO, OBSERVACIÓN) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(sql, datos)
    conexion.commit()

# Función para insertar datos en la tabla evento
def insertar_evento(datos):
    cursor = conexion.cursor()
    sql = "INSERT INTO dbo.evento (MES, ANIO, COD_EPS, NOMBRE_EPS, NIT_IPS, NOMBRE_IPS, FORMA_DE_CONTRATACIÓN, TOTAL_GIRO, OBSERVACIÓN) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(sql, datos)
    conexion.commit()

# Directorio donde se encuentran los archivos a ingestar
directorio = "csv"

for nombre_archivo in os.listdir(directorio):
    ruta_directorio = os.path.join(directorio, nombre_archivo)
    
    # Verificar si el nombre del archivo contiene "GIRO DIRECTO EVENTO"
    if "GIRO DIRECTO EVENTO" in nombre_archivo:
        # Obtener mes y año del nombre del archivo
        partes_nombre = nombre_archivo.split(' ')[-1].split('-')
        mes = partes_nombre[0]
        anio = partes_nombre[1]

        with open(ruta_directorio, "r", encoding="utf-8") as archivo:
            # Leer cada línea del archivo y separar los campos por coma
            for linea in archivo:
                datos = linea.strip().split(',')
                # Insertar mes y año en los datos
                datos.insert(0, mes)
                datos.insert(1, anio)
                # Ingestar los datos en la tabla evento
                insertar_evento(datos)
        print(f"Datos del archivo {nombre_archivo} ingestado en la tabla evento.")

    # Verificar si el nombre del archivo contiene "giro-directo-discriminado-capita-y-evento"
    elif "giro-directo-discriminado-capita-y-evento" in nombre_archivo:
        # Obtener mes y año del nombre del archivo
        partes_nombre = nombre_archivo.split(' ')[-1].split('-')
        mes = partes_nombre[0]
        anio = partes_nombre[1]

        with open(ruta_directorio, "r", encoding="utf-8") as archivo:
            # Leer la primera línea del archivo para determinar si tiene el campo "FORMA DE CONTRATACIÓN"
            primera_linea = archivo.readline()
            if "FORMA DE CONTRATACIÓN" in primera_linea:
                # El archivo tiene el campo "FORMA DE CONTRATACIÓN"
                # Leer cada línea del archivo y separar los campos por coma
                for linea in archivo:
                    datos = linea.strip().split(',')
                    # Insertar mes y año en los datos
                    datos.insert(0, mes)
                    datos.insert(1, anio)
                    # Ingestar los datos en la tabla captacion
                    insertar_captacion(datos)
            else:
                # El archivo no tiene el campo "FORMA DE CONTRATACIÓN"
                # Regresar al inicio del archivo
                archivo.seek(0)
                # Leer cada línea del archivo y separar los campos por coma
                for linea in archivo:
                    datos = linea.strip().split(',')
                    # Insertar mes y año en los datos
                    datos.insert(0, mes)
                    datos.insert(1, anio)
                    # Ingestar los datos en la tabla captacion
                    insertar_captacion(datos)

        print(f"Datos del archivo {nombre_archivo} ingestado en la tabla captacion.")

    else:
        print("No se encontró un archivo para ingestar")

# Cerrar la conexión a la base de datos
conexion.close()
print("Proceso de ingesta finalizado")







# Importación de librerías necesarias
# import os
# import pyodbc
# import pandas as pd

# def ingesta_datos (archivo,tabla):
#     # Cadena de conexión
#     conexion = pyodbc.connect('Driver = {SQL Server};'
#                             'Server = DESKTOP-6QD6LBH;'
#                             'Database = giros_minsalud;'
#                             'Trusted_Connetion = yes') #Debido a que mi sql server tiene autenticación de windows
    
#     # Lectura del csv
#     datos_csv = pd.read_csv(archivo)
    
#     #Ingesta de datos a la tabla de destino
#     datos_csv.to_sql(tabla, conexion, if_exists='append', index=False)
    
#     #Cierre de la conección 
#     conexion.commit()
#     conexion.close()
#     print(f"Datos de {archivo} ingresados correctamente a la tabla {tabla}")
    