import feedparser
import re,sqlite3

def formatear_fecha(fecha, universidad):
    fecha = fecha.split()
    if universidad == "uv":
        dia = fecha[0]
        mes = fecha[2].lower()
        anno = fecha[4]
    elif universidad == "upla":
        dia = fecha[1]
        mes = fecha[2].lower()
        anno = fecha[3]
    elif universidad == "ufsm":
        dia = fecha[1]
        mes = fecha[2].lower()
        anno = fecha[3]
    elif universidad == "ucn":
        dia = fecha[1]
        mes = fecha[2].lower()
        anno = fecha[3]
    elif universidad == "pucv":
        dia = fecha[1]
        mes = fecha[3].lower()
        anno = fecha[5]

    if mes == "enero" or mes == "jan":
        mes = '01'
    elif mes == "febrero" or mes == "feb":
        mes = '02'
    elif mes == "marzo" or mes == "mar":
        mes = '03'
    elif mes == "abril" or mes == "apr":
        mes ='04'
    elif mes == "mayo" or mes == "may":
        mes = '05'
    elif mes == "junio" or mes == "jun":
        mes = '06'
    elif mes == "julio" or mes == "jul":
        mes = '07'
    elif mes == "agosto" or mes == "aug":
        mes ='08'
    elif mes == "septiembre" or mes == "sep":
        mes = '09'
    elif mes == "octubre" or mes == "oct":
        mes = '10'
    elif mes == "noviembre" or mes == "nov":
        mes = '11'
    elif mes == "diciembre" or mes == "dec":
        mes ='12'
    fecha = dia + "/" + mes + "/" + anno
    return fecha

def insertar(nombre_u,region_u,titulo_n,bajada,fecha,link_noticia,link_recurso,categoria):
    nombre_db = "../UniNews/bd_universidades.db"
    conexion = sqlite3.connect(nombre_db)
    conexion.text_factory = str
    cursor = conexion.cursor()
    p = cursor.execute("SELECT COUNT(1) FROM noticias WHERE titulo = '%s'" % titulo_n)
    if p.fetchone()[0]:
        print "existe"
    else:
        print "no existo"
        cursor.execute("INSERT INTO universidad(nombre,region) VALUES(?,?)", (nombre_u, region_u))
        id = cursor.lastrowid
        cursor.execute(
        "INSERT INTO noticias(titulo,bajada,fecha,link_noticia,link_recurso,categoria,id_universidad) VALUES (?,?,?,?,?,?,?)",(titulo_n, bajada, fecha, link_noticia, link_recurso, categoria, id))


    conexion.commit()
    conexion.close()

def ucn():
    d = feedparser.parse("http://www.noticias.ucn.cl/feed/")
    for e in d.entries:
        titulo = (e.title)
        nombre_uni = "ucn"
        link_noticia = (e.link)
        categoria = (e.category)
        fecha = e.published
        fecha = formatear_fecha(fecha,nombre_uni)
        description = e.description.split("/>")
        bajada = description[1]
        cuerpo = e['content']
        contenido = cuerpo[0].value
        link_recurso = re.search('(?P<url>http?://[^\s]+(png|jpeg|jpg))', contenido).group("url")
        nombre_u = "Universidad Catolica del Norte"
        region_u = "4"
        insertar(nombre_u, region_u, titulo, bajada, fecha, link_noticia, link_recurso, categoria)


ucn()

