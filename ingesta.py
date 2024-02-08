import os
import pyodbc

# Establecer conexión a la base de datos SQL Server
conexion = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-6QD6LBH;DATABASE=giros_minsalud;Trusted_Connection=yes')

# Función para insertar datos en la tabla captacion
def insertar_captacion(datos):
    cursor = conexion.cursor()
    if len(datos) == 9:
        sql = "INSERT INTO dbo.captacion (MES, ANIO, DANE, DEPARTAMENTO, MUNICIPIO, COD_EPS, NOMBRE_EPS, NIT_IPS, NOMBRE_IPS, TOTAL_GIRO, OBSERVACIÓN) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        
    elif len(datos) == 10:
        sql = "INSERT INTO dbo.captacion (MES, ANIO, DANE, DEPARTAMENTO, MUNICIPIO, COD_EPS, NOMBRE_EPS, NIT_IPS, NOMBRE_IPS, FORMA_DE_CONTRATACIÓN,TOTAL_GIRO, OBSERVACIÓN) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

    else:
        return
    
    cursor.execute(sql, datos)
    conexion.commit()

# Función para insertar datos en la tabla evento
def insertar_evento(datos):
    cursor = conexion.cursor()
    if len(datos)== 8:
        sql = "INSERT INTO dbo.evento (MES, ANIO, COD_EPS, NOMBRE_EPS, NIT_IPS, NOMBRE_IPS, TOTAL_GIRO, OBSERVACIÓN) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    
    elif len(datos) == 9:
        sql = "INSERT INTO dbo.evento (MES, ANIO, COD_EPS, NOMBRE_EPS, NIT_IPS, NOMBRE_IPS, FORMA_DE_CONTRATACIÓN, TOTAL_GIRO, OBSERVACIÓN) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    
    else:
        return
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
            
            print(f"Ingestando la información del archivo {nombre_archivo} en la tabla evento...")
            
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
                
                print(f"Ingestando la información del archivo {datos} en la tabla tabla captación...")
                
                for linea in archivo:
                    datos = linea.strip().split(',')
                    # Insertar mes y año en los datos
                    datos.insert(0, mes)
                    datos.insert(1, anio)
                    # Ingestar los datos en la tabla captacion
                    insertar_captacion(datos)
                    
        print(f"Datos del archivo {datos} ingestado en la tabla captación.")

    else:
        print("No se encontró un archivo para ingestar")

# Cerrar la conexión a la base de datos
conexion.close()
print("Proceso de ingesta finalizado")
