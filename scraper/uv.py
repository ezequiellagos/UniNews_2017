from bs4 import BeautifulSoup
import urllib


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


def uv():
    universidad = "Universidad de Valparaíso"
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
        titulo = bs_noticia.find("div", id = "n_titulo").text
        bajada = bs_noticia.find("div", id = "n_bajada").text
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


        print universidad
        print fecha
        print titulo
        print bajada
        print link
        print imagen

        print "--------------------------------------------------------------------------------------------"

uv()