from bs4 import BeautifulSoup
#import requests
import urllib

#contents = requests.get("http://www.pucv.cl/pucv/site/tax/port/all/taxport_1___1.html")
contents = urllib.urlopen("http://www.pucv.cl/pucv/site/tax/port/all/taxport_1___1.html").read()
data = contents
bs = BeautifulSoup(data, 'lxml')

articulos = bs.findAll("article")
for n in articulos:
    link = n.a['href']
    link = "http://www.pucv.cl" + link.replace("..", "")
    pagina_noticia = urllib.urlopen(link)
    soup = BeautifulSoup(pagina_noticia,"html.parser")

    


