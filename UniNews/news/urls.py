from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<id_noticia>[0-9]+)/$', views.detalle, name='detalle'),
    url(r'^estadisticas/$' , views.estadisticas, name='estadisticas'),
    url(r'^region/(?P<region>[0-9]+)$' , views.region, name='region'),
    url(r'^categoria/(?P<categoria>[0-9A-Za-z]+)$' , views.categoria, name='categoria'),
]