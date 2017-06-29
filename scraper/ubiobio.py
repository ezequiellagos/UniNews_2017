from bs4 import BeautifulSoup
import urllib
import feedparser
import unicodedata

def elimina_tildes(s):
   return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

#def ubiobio():
url_rss = "http://noticias.ubiobio.cl/feed/"
feed = feedparser.parse( url_rss )

for item in feed['items']:
    #print item['date']
    titulo =  item['title']
    bajada =  item['summary']
    link = item['link']
    categoria = item['category']
    fecha = item['published']

    # Parsea la categoria para ser buscada
    categoria_busqueda = categoria.lower()
    categoria_busqueda = elimina_tildes(categoria_busqueda)
    categoria_busqueda = categoria_busqueda.replace(" ", "-")
    """
    # Entra en la pagina de cada categoria y busca todas las noticias
    contents = urllib.urlopen("http://noticias.ubiobio.cl/category/"+categoria_busqueda+"/").read()
    bs = BeautifulSoup(contents, "html.parser")
    divs = bs.find_all("div", ["gdl-blog-mediumt"])

    # Por cada noticia obtiene su titulo
    for div in divs:
        titulo_articulo = div.find("h2",["blog-title"])

        # Si el titulo de la noticia es igual al titulo obtenido del XML, obtiene la imagen de esa noticia y termina el ciclo
        
        if titulo_articulo == titulo:
            imagen = div.find("img", ['blog-media-wrapper gdl-image'])['src']
            break
        """

    print categoria
    #print titulo_articulo
    print titulo
    print bajada
    print link
    print fecha
    #print imagen
    print "---------------------------------------------------------"

