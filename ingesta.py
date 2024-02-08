import os
import pyodbc
import re


# Establecer conexión a la base de datos SQL Server
conexion = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-6QD6LBH;DATABASE=giros_minsalud;Trusted_Connection=yes')

def setFecha(mes, anio):
    cursor = conexion.cursor()
    sql = '''UPDATE dbo.captacion 
    SET MES = ? WHERE MES IS NULL
    
    UPDATE dbo.captacion
    SET ANIO = ? WHERE ANIO IS NULL
    '''
    cursor.execute(sql, mes, anio)
    conexion.commit()

# Función para insertar datos en la tabla captacion
def insertar_captacion(datos):
    cursor = conexion.cursor()
    if len(datos) == 9:
        sql = "INSERT INTO dbo.captacion (DANE, DEPARTAMENTO, MUNICIPIO, COD_EPS, NOMBRE_EPS, NIT_IPS, NOMBRE_IPS, TOTAL_GIRO, OBSERVACIÓN) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    elif len(datos) == 10:  # Revisamos la longitud esperada de los datos
        sql = "INSERT INTO dbo.captacion (DANE, DEPARTAMENTO, MUNICIPIO, COD_EPS, NOMBRE_EPS, NIT_IPS, NOMBRE_IPS, COMPLEMENTO_NOMBRE_IPS, TOTAL_GIRO, OBSERVACIÓN) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    elif len(datos) == 11:
        sql = "INSERT INTO dbo.captacion (DANE, DEPARTAMENTO, MUNICIPIO, COD_EPS, NOMBRE_EPS, NIT_IPS, NOMBRE_IPS, COMPLEMENTO_NOMBRE_IPS, FORMA_DE_CONTRATACIÓN, TOTAL_GIRO, OBSERVACIÓN) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    else:
        print("Número de campos incorrecto:", datos)
        return
    
    cursor.execute(sql, datos)
    conexion.commit()


# Función para insertar datos en la tabla evento
def insertar_evento(datos):
    cursor = conexion.cursor()
    if len(datos) == 8:
        sql = "INSERT INTO dbo.evento (MES, ANIO, COD_EPS, NOMBRE_EPS, NIT_IPS, NOMBRE_IPS, TOTAL_GIRO, OBSERVACIÓN) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    elif len(datos) == 9:
        sql = "INSERT INTO dbo.evento (MES, ANIO, COD_EPS, NOMBRE_EPS, NIT_IPS, NOMBRE_IPS, FORMA_DE_CONTRATACIÓN, TOTAL_GIRO, OBSERVACIÓN) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    else:
        return
    cursor.execute(sql, datos)
    conexion.commit()

# Directorio donde se encuentran los archivos a ingestar
directorio = "csv"

# Expresión regular para buscar el mes y el año en el nombre del archivo
patron = r'(\w+)-(\d{4})'

for nombre_archivo in os.listdir(directorio):
    ruta_directorio = os.path.join(directorio, nombre_archivo)
    
    coincidencia = re.search(patron, nombre_archivo)
    if coincidencia:
        mes = coincidencia.group(1)
        anio = coincidencia.group(2)
    else:
        print("No se pudo encontrar mes y año en el nombre del archivo:", nombre_archivo)
        continue  
    
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
        
        with open(ruta_directorio, "r", encoding="utf-8") as archivo:
            # Leer la primera línea del archivo para determinar si tiene el campo "FORMA DE CONTRATACIÓN"
            primera_linea = archivo.readline()
            for linea in archivo:
                    datos = linea.strip().split(',')
                    
                    # Ingestar los datos en la tabla captacion
                    insertar_captacion(datos)
                    setFecha(mes, anio)
                    
        print(f"Datos del archivo {nombre_archivo} ingestado en la tabla captacion.")

    else:
        print("No se encontró un archivo para ingestar")

# Cerrar la conexión a la base de datos
conexion.close()
print("Proceso de ingesta finalizado")