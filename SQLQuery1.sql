--Creación de la base de datos
CREATE DATABASE giros_minsalud

--Uso de la base de datos creada
USE giros_minsalud

--Creación de las tablas para la base
CREATE TABLE captacion(
	MES varchar(15),
	ANIO varchar(10),
	DANE varchar(15),
	DEPARTAMENTO varchar(50),
	MUNICIPIO varchar(50),
	COD_EPS varchar(50),
	NOMBRE_EPS varchar(50),
	NIT_IPS varchar(50),
	NOMBRE_IPS varchar(50),
	COMPLEMENTO_NOMBRE_IPS varchar(50),
	FORMA_DE_CONTRATACIÓN varchar(50),
	TOTAL_GIRO varchar(50),
	OBSERVACIÓN varchar(50)

)

CREATE TABLE evento(
	MES varchar(15),
	ANIO varchar(10),
	COD_EPS varchar(50),
	NOMBRE_EPS varchar(50),
	NIT_IPS varchar(50),
	NOMBRE_IPS varchar(50),
	FORMA_DE_CONTRATACIÓN varchar(250),
	TOTAL_GIRO varchar(50),
	OBSERVACIÓN varchar(50)

)

SELECT count(*) FROM dbo.evento
SELECT count(*) FROM dbo.captacion

SELECT * FROM dbo.evento
SELECT * FROM dbo.captacion


ALTER TABLE dbo.captacion
ALTER COLUMN NOMBRE_IPS varchar(250)

truncate table dbo.evento
truncate table dbo.captacion