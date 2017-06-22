from bs4 import BeautifulSoup
import urllib

contents = urllib.urlopen("http://www.uv.cl/pdn/archivo/").read()
bs = BeautifulSoup(contents, "lxml")
divs = bs.find_all("div", ["item n_caja borde6", "item n_caja borde6 fin"])

for div in divs:
    fecha = div.find("div", ["fecha"]).text
    link = div.a['href']
    link = "http://www.uv.cl/pdn" + link.replace("..", "")

    # Accede a la pagina de la noticia
    pagina_noticia = urllib.urlopen(link).read()
    bs_noticia = BeautifulSoup(pagina_noticia, "html.parser")
    titulo = bs_noticia.find("div", id = "n_titulo").text
    bajada = bs_noticia.find("div", id = "n_bajada").text
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

    noticias = bs_noticia.find("div", id="n_cuerpo")
    noticias = noticias.find_all("p")

    for noticia in noticias:
        noticia.find("div").clear()
        print noticia



    #print titulo, "|" ,titulo2
    print "--------------------------------------------------------------------------------------------"
