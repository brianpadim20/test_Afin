# Documentación de la prueba técnica propuesta por Grupo Afín

---

### Enunciado
En esta prueba debes descargar la información de los últimos 13 meses, la información corresponde a los giros que el ministerio de salud realiza a sus prestadores por los conceptos de cápita y evento desde el siguiente enlace: https://www.adres.gov.co/eps/giro-directo/Paginas/girosDiscriminados/giro-por-tipo-de-contratacion.aspx.

Esta información deberá ser consolidada en una base de datos SQL, en cada archivo que descargue tendrás dos hojas debes revisar como consolidar todo en una base de datos. La información que se tiene esta por prestador y la eps que realiza el giro adicional la información por departamento y municipio. Esta información es la fuente principal de análisis.

Después de construir la información en sql realizaras un reporte con los hallazgo encontrados en la calidad de datos y presentar un informe donde detalles que ha pasado en estos 13 meses como por ejemplo en graficas ver cuál es el prestador mas importante y que eps le han girado recurso al igual que el comportamiento en el tiempo. Eres libre de proponer el análisis de la información, gráficos, tablas o cualquier mecanismo que te permita explicarlo fácilmente.

Estas en la libertad de adicionar tablas que consideres necesarias en el modelo de la información, que te sirvan al momento de analizar.

### solucion:

---
**Revisión de cabeceras**
Lo primero que se hizo fue descargar el reporte de los últimos 13 meses del ministerio de salud; se guardaron en un directorio llamado excel.

Posteriormente se revisa el encabezado de cada uno de los archivos descargados para mirar los campos que tendrán las tablas de la base de datos, quedando de la siguiente manera:

- **Giro de capitación:**

![capitación](imagenes%20a%20usar/cabeceras%20de%20giro%20de%20capitación.png)


- **Giro directo de evento**
![giro-directo-de-evento](imagenes%20a%20usar/Giro%20directo%20de%20evento.png)

---
**Separación de las tablas:**
Como todas las tablas tenían tanto giro directo como discriminado cápita, se separa en dos archivos excel, para que así sea más fácil su cambio de formato

---
**Cambio de formato .xslx a .csv**

Como los archivos vienen en formato excel (.xslx), se procede a crear un código que los cambie de formato de manera automática a coma separeted values (.csv) para facilitar la ingesta a la base de datos.

Para esto, el código se hizo uso de las siguientes librerías:
- **os**: Es un módulo que proporciona una forma de trabajar con el sistema operativo, permitiendo acceder a funciones relacionadas con el sistema de archivos, como la creación de directorios, la enumeración de archivos en un directorio, entre otras.

- **pandas**: Es una biblioteca de análisis de datos que proporciona estructuras de datos flexibles y herramientas para trabajar con ellas. En este caso, se utiliza para leer archivos Excel y luego escribir los datos en archivos CSV.

**Bibliotecas adicionales**
Para que el script funcionara, se tuvieron que instalar dos bibliotecas adicionales:
- **openpyxl**: Es necesario instalar esta biblioteca para que pandas pueda leer archivos Excel en formato .xlsx.
- **pyarrow**: Puede leer y escribir una variedad de formatos de archivos de datos, incluidos Excel y CSV, con un rendimiento muy alto y una eficiencia de almacenamiento.

El código se crea de la siguiente manera:

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

---
**Depuración de los archivos generados**
La finalidad de este código es depurar los archivos CSV generados antes de ser ingresados en la tabla a la cual corresponden de SQL Server. La depuración implica eliminar líneas innecesarias o no deseadas de los archivos CSV para que los datos resultantes sean consistentes y estén formateados correctamente antes de ser cargados en la base de datos.

El código se diseñó para realizar dos tipos de depuración:

Para archivos que contienen "GIRO DIRECTO EVENTO" en su nombre: El código elimina simplemente la última línea del archivo, debido a que esta línea contiene información que no es necesaria o no es relevante para la tabla de la base de datos.

Para archivos que contienen "giro-directo-discriminado-capita-y-evento" en su nombre: El código conserva solo las líneas desde la línea 8 hasta las últimas tres líneas antes del final del archivo. Esto se hizo para eliminar encabezados o líneas de pie de página innecesarias en los archivos CSV.

La finalidad general de este código es preparar los archivos CSV para su carga en una tabla de SQL Server, asegurando que los datos estén limpios y formateados adecuadamente para su uso en la base de datos.

El código quedó de la siguiente manera:

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


---

**Creación de la base de datos**

Para esta prueba se trabajará con MS SQL Server; por este motivo, la sintaxis del script será la siguiente:

    --Creación de la base de datos
    CREATE DATABASE giros_minsalud

    --Uso de la base de datos creada
    USE giros_minsalud

    --Creación de las tablas para la base
    CREATE TABLE captacion(
        MES varchar(15), --Para tener control de a qué mes pertenece cada registro en esta tabla
        ANIO varchar(10), --Para saber si el año es 2023 o 2024, debido a que hay información de enero 2024
        --Campos especificados en la tabla descargada
        DANE varchar(15),
        DEPARTAMENTO varchar(50),
        MUNICIPIO varchar(50),
        COD_EPS varchar(50),
        NOMBRE_EPS varchar(50),
        NIT_IPS varchar(50),
        NOMBRE_IPS varchar(50),
        FORMA_DE_CONTRATACIÓN varchar(50),
        TOTAL_GIRO varchar(50),
        OBSERVACIÓN varchar(50)

    )

    CREAATE TABLE evento(
        MES varchar(15), --Para tener control de a qué mes pertenece cada registro en esta tabla
        ANIO varchar(10), --Para saber si el año es 2023 o 2024, debido a que hay información de enero 2024
        --Campos especificados en la tabla descargada
        COD_EPS varchar(50),
        NOMBRE_EPS varchar(50),
        NIT_IPS varchar(50),
        NOMBRE_IPS varchar(50),
        FORMA_DE_CONTRATACIÓN varchar(50),
        TOTAL_GIRO varchar(50),
        OBSERVACIÓN varchar(50)

    )

De esta manera, se crea exitosamente la base de datos giros_minsalud y las respectivas tablas de captación y evento, como se evidencia en la siguiente captura de pantalla:

![base_creada](imagenes%20a%20usar/Creación%20bd.png)

---
**Ingesta de información a la tabla**
Una vez depurada la información con la cual se va a trabajar, se procede a ingestar la información a la tabla