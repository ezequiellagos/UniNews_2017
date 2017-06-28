import sqlite3

conexion = sqlite3.connect("bd_universidades.db")
consulta = conexion.cursor()

sql      = """ 
CREATE TABLE IF NOT EXISTS universidad(
id_universidad INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
nombre VARCHAR(100) NOT NULL,
region VARCHAR(1) NOT NULL
)"""

sql2 = """
CREATE TABLE IF NOT EXISTS noticias(
id_noticia INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
titulo VARCHAR(200) NOT NULL,
bajada TEXT NOT NULL,
fecha DATE NOT NULL,
link_noticia VARCHAR(200) NOT NULL,
link_recurso VARCHAR(200) NOT NULL,
id_universidad INTEGER NOT NULL,
categoria VARCHAR(100) NOT NULL,
FOREIGN KEY (id_universidad) REFERENCES universidad(id_universidad)
)"""

if(consulta.execute(sql)):
	print("TABLA CREADA CON EXITO")
else:
	print("HA OCURRIDO UN ERROR AL CREAR LA TABLA")

if(consulta.execute(sql2)):
	print("TABLA CREADA CON EXITO")
else:
	print("HA OCURRIDO UN ERROR AL CREAR LA TABLA")

consulta.close()
conexion.commit()
conexion.close()