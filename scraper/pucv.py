from bs4 import BeautifulSoup
import urllib,sqlite3,time

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
    nombre_db = "../../BD/bd_universidades.db"
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
            fecha = time.strftime("%d/%m/%Y")
            print fecha

        else:
            fecha = formatear_fecha(fecha.text,nombre_uni)
            print fecha

        region_u = 5

        newpage = urllib.urlopen(link).read()
        bs_cate = BeautifulSoup(newpage, "html.parser")
        categoria = bs_cate.find("div",{ "class" : "breadcrumbs" })
        categorias = categoria.findAll("a")
        try:
            category = categorias[2].text
        except:
            category = "sin-categoria"

        insertar(nombre_u, region_u, titulo, bajada, fecha, link, imagen, category)


pucv()

    


    


