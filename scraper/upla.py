from bs4 import BeautifulSoup
import urllib
import feedparser
import unicodedata

def elimina_tildes(s):
   return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

url_rss = "http://www.upla.cl/noticias/feed/"
feed = feedparser.parse( url_rss )

for item in feed['items']:
    #print item['date']
    titulo =  item['title']
    bajada =  item['summary']
    link = item['link']
    categoria = item['category']
    fecha = item['published']


    print categoria
    print titulo
    print bajada
    print link
    print fecha

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

    print imagen
    print "---------------------------------------------------------"