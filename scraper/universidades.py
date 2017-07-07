from bs4 import BeautifulSoup
import urllib, sqlite3, time, unicodedata, feedparser, re


def insertar(nombre_u,region_u,titulo_n,bajada,fecha,link_noticia,link_recurso,categoria):
    nombre_db = "../UniNews/bd_universidades.db"
    conexion = sqlite3.connect(nombre_db)
    conexion.text_factory = str
    cursor = conexion.cursor()
    p = cursor.execute("SELECT COUNT(1) FROM universidad WHERE nombre = '%s'" % nombre_u)
    if p.fetchone()[0]:
        # Universidad existe
        c = cursor.execute("SELECT id_universidad FROM universidad WHERE nombre = '%s'" % nombre_u)
        id =  c.fetchone()[0]
        k = cursor.execute("SELECT COUNT(1) FROM noticias WHERE titulo = '%s'" % titulo_n)
        if k.fetchone()[0]:
            print "Noticia EXISTE: " + nombre_u
        else:
            cursor.execute(
                "INSERT INTO noticias(titulo,bajada,fecha,link_noticia,link_recurso,categoria,id_universidad) VALUES "
                "(?,?,?,?,?,?,?)", (titulo_n, bajada, fecha, link_noticia, link_recurso, categoria, id))
            print "Noticia INSERTADA: " + nombre_u
    else:
        cursor.execute("INSERT INTO universidad(nombre,region) VALUES(?,?)",(nombre_u, region_u))
        print "Universidad INSERTADA: " + nombre_u
        id = cursor.lastrowid
        k = cursor.execute("SELECT COUNT(1) FROM noticias WHERE titulo = '%s'" % titulo_n)
        if k.fetchone()[0]:
            print "Noticia EXISTE: " + nombre_u
        else:
            cursor.execute("INSERT INTO noticias(titulo,bajada,fecha,link_noticia,link_recurso,categoria,id_universidad) VALUES "
                           "(?,?,?,?,?,?,?)",(titulo_n, bajada, fecha, link_noticia, link_recurso, categoria, id))
            print "Noticia INSERTADA: " + nombre_u
    conexion.commit()
    conexion.close()

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
        mes = '04'
    elif mes == "mayo" or mes == "may":
        mes = '05'
    elif mes == "junio" or mes == "jun":
        mes = '06'
    elif mes == "julio" or mes == "jul":
        mes = '07'
    elif mes == "agosto" or mes == "aug":
        mes = '08'
    elif mes == "septiembre" or mes == "sep":
        mes = '09'
    elif mes == "octubre" or mes == "oct":
        mes = '10'
    elif mes == "noviembre" or mes == "nov":
        mes = '11'
    elif mes == "diciembre" or mes == "dec":
        mes = '12'

    if dia == "1":
        dia = '01'
    elif dia == "2":
        dia = '02'
    elif dia == "3" :
        dia = '03'
    elif dia == "4":
        dia = '04'
    elif dia == "5":
        dia = '05'
    elif dia == "6":
        dia = '06'
    elif dia == "7":
        dia = '07'
    elif dia == "8":
        dia = '08'
    elif dia == "9":
        dia = '09'

    #fecha = dia + "/" + mes + "/" + anno
    fecha = anno + "-" + mes + "-" + dia
    return fecha

def elimina_tildes(s):
   return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

def pucv():
    nombre_u = "Pontificia Universidad Catolica de Valparaiso"
    nombre_uni = "pucv"
    contents = urllib.urlopen("http://www.pucv.cl/pucv/site/tax/port/all/taxport_1___1.html").read()
    bs = BeautifulSoup(contents, "html.parser")
    articulos = bs.find_all("article")
    for articulo in articulos:
        link = articulo.a['href']
        link = "http://www.pucv.cl" + link.replace("..", "")

        imagen = articulo.img['src']
        imagen = "http://pucv.cl" + imagen.replace("..","")

        pagina_noticia = urllib.urlopen(link).read()
        bs_noticia = BeautifulSoup(pagina_noticia, "html.parser")
        titulo = bs_noticia.find("h1", { "class" : "titular" }).text

        bajada = bs_noticia.find("p",{ "class" : "bajada" }).text
        fecha = bs_noticia.find("span",{"class":"fecha aright"})
        if fecha is None:
            #fecha = time.strftime("%d/%m/%Y")
            fecha = time.strftime("%Y-%m-%d")

        else:
            fecha = formatear_fecha(fecha.text,nombre_uni)

        region_u = 5

        newpage = urllib.urlopen(link).read()
        bs_cate = BeautifulSoup(newpage, "html.parser")
        categoria = bs_cate.find("div",{ "class" : "breadcrumbs" })
        categorias = categoria.findAll("a")
        try:
            category = categorias[2].text
            categoria_busqueda = category.lower()
            categoria_busqueda = elimina_tildes(categoria_busqueda)
            categoria_busqueda = categoria_busqueda.replace(" ", "-")
        except:
            category = 'sin-categoria'

        

        insertar(nombre_u, region_u, titulo, bajada, fecha, link, imagen, categoria_busqueda)

def ucn():
    d = feedparser.parse("http://www.noticias.ucn.cl/feed/")
    for e in d.entries:
        titulo = (e.title)
        nombre_uni = "ucn"
        link_noticia = (e.link)
        categoria = (e.category)
        categoria_busqueda = categoria.lower()
        categoria_busqueda = elimina_tildes(categoria_busqueda)
        categoria_busqueda = categoria_busqueda.replace(" ", "-")
        fecha = e.published
        fecha = formatear_fecha(fecha,nombre_uni)
        description = e.description.split("/>")
        bajada = description[1]
        cuerpo = e['content']
        contenido = cuerpo[0].value
        link_recurso = re.search('(?P<url>http?://[^\s]+(png|jpeg|jpg))', contenido).group("url")
        nombre_u = "Universidad Catolica del Norte"
        region_u = "2"
        insertar(nombre_u, region_u, titulo, bajada, fecha, link_noticia, link_recurso, categoria_busqueda)

def usm():
    d = feedparser.parse("http://www.noticias.usm.cl/2017/feed/")
    for e in d.entries:
        titulo = (e.title)
        nombre_u = "Universidad Federico Santa Maria"
        nombre_uni = "ufsm"
        link_noticia = (e.link)
        categoria = (e.category)
        categoria_busqueda = categoria.lower()
        categoria_busqueda = elimina_tildes(categoria_busqueda)
        categoria_busqueda = categoria_busqueda.replace(" ", "-")
        bajada = (e.description)
        fecha = e.published
        fecha = formatear_fecha(fecha,nombre_uni)
        region_u = "5"
        cuerpo = e['content']
        contenido = cuerpo[0].value
        link_recurso = re.search('(?P<url>http?://[^\s]+(png|jpeg|jpg))', contenido).group("url")
        insertar(nombre_u, region_u, titulo, bajada, fecha, link_noticia, link_recurso, categoria_busqueda)

def upla():
    universidad = "Universidad de Playa Ancha"
    region = 5
    url_rss = "http://www.upla.cl/noticias/feed/"
    feed = feedparser.parse( url_rss )

    for item in feed['items']:
        #print item['date']
        titulo =  item['title']
        bajada =  item['summary']
        link = item['link']
        categoria = item['category']
        fecha = item['published']
        fecha = formatear_fecha(fecha, "upla")

        # Parsea la categoria para ser buscada
        categoria_busqueda = categoria.lower()
        categoria_busqueda = elimina_tildes(categoria_busqueda)
        categoria_busqueda = categoria_busqueda.replace(" ", "-")

        # Entra en la pagina de cada categoria y busca todas las noticias
        contents = urllib.urlopen("http://www.upla.cl/noticias/category/"+categoria_busqueda+"/").read()
        bs = BeautifulSoup(contents, "html.parser")
        articles = bs.find_all("article", ["item-list"])

        # Por cada noticia obtiene su titulo
        for article in articles:
            titulo_articulo = article.find("a").text

            # Si el titulo de la noticia es igual al titulo obtenido del XML, obtiene la imagen de esa noticia y termina el ciclo
            if titulo_articulo == titulo:
                imagen = article.find("img")['src']
                break

        insertar(universidad, region, titulo, bajada, fecha, link, imagen, categoria_busqueda)

def uv():
    universidad = "Universidad de Valparaiso"
    region = 5
    contents = urllib.urlopen("http://www.uv.cl/pdn/archivo/").read()
    bs = BeautifulSoup(contents, "html.parser")
    divs = bs.find_all("div", ["item n_caja borde6", "item n_caja borde6 fin"])

    for div in divs:
        fecha = div.find("div", ["fecha"]).text
        fecha = formatear_fecha(fecha, "uv")

        imagen = div.find("img", ["sombra"])['src']
        imagen = "http://www.uv.cl/pdn" + imagen.replace("..", "")
        link = div.a['href']
        link = "http://www.uv.cl/pdn" + link.replace("..", "")

        # Accede a la pagina de la noticia
        pagina_noticia = urllib.urlopen(link).read()
        bs_noticia = BeautifulSoup(pagina_noticia, "html.parser")
        titulo = bs_noticia.find("div", id="n_titulo").text
        bajada = bs_noticia.find("div", id="n_bajada").text
        """
        imagen = bs_noticia.find("div", id = "n_clipex")

        video = imagen.iframe
        imagen = imagen.img
        if video is not None:
            # Se obtiene el video de portada de la noticia
            video = video.get('src')
            #print video
        else:
            # Se obtiene la imagen de portada de la noticia
            imagen = imagen.get('src')
            imagen = "http://www.uv.cl" + imagen
        """

        """
        noticias = bs_noticia.find("div", id="n_cuerpo")
        noticias = noticias.find_all("p")

        for noticia in noticias:
            noticia.find("div").clear()
            print noticia
        """

        insertar(universidad, region, titulo, bajada, fecha, link, imagen, 'sin-categoria')

pucv()
ucn()
usm()
upla()
uv()