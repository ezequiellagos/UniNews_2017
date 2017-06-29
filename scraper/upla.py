from bs4 import BeautifulSoup
import urllib
import feedparser
import unicodedata

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
        dia = fecha[5]
        mes = fecha[5].lower()
        anno = fecha[5]
    elif universidad == "ucn":
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

def elimina_tildes(s):
   return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

def upla():
    universidad = "Universidad de Playa Ancha"
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


        print categoria_busqueda
        print titulo
        print bajada
        print link
        print imagen
        print fecha
        print "---------------------------------------------------------"

upla()