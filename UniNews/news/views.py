# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.http import HttpResponse

from .models import Universidad, Noticias
from django.db.models import Max,Sum
from datetime import datetime


def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
    ultimas_noticias = Noticias.objects.order_by('-fecha')
    noticias_mas_vistas = Noticias.objects.order_by('-contador_visitas')[:3]

    context = {'ultimas_noticias': ultimas_noticias,'noticias_mas_vistas' :noticias_mas_vistas}
    return render(request, 'news/index.html', context)

def detalle(request, id_noticia):

    noticia = get_object_or_404(Noticias, pk=id_noticia)

    contador_antes = noticia.contador_visitas
    noticia.contador_visitas += 1
    noticia.save()
    contador_despues = noticia.contador_visitas
    #return render(request, 'news/detalle.html', {'noticia': noticia, 'contador_antes':contador_antes, 'contador_despues':contador_despues})

    return redirect(noticia.link_noticia)

def estadisticas(request):

    # Crea objeto con la tabla de noticias
    noticias = Noticias.objects.order_by('-contador_visitas')

    #mejores_noticia_pucv = noticias.filter(id_universidad=5).aggregate(Max('contador_visitas'))


    # Suma de todas las visitas por universidad
    contador_pucv = noticias.filter(id_universidad__nombre__contains="Pontificia Universidad Catolica de Valparaiso").aggregate(Sum('contador_visitas'))
    mejores_noticia_pucv = noticias.filter(id_universidad__nombre__contains="Pontificia Universidad Catolica de Valparaiso").aggregate(Max('contador_visitas'))
    #SELECT SUM(contador_visitas) in contador_visitas__max FROM noticias INNER JOIN universidad ON noticias.id_universidad = universidad.id_universidad WHERE
    contador_upla = noticias.filter(id_universidad__nombre__contains="Universidad de Playa Ancha").aggregate(Sum('contador_visitas'))
    contador_ufsm = noticias.filter(id_universidad__nombre__contains="Universidad Federico Santa Maria").aggregate(Sum('contador_visitas'))
    contador_ucn = noticias.filter(id_universidad__nombre__contains="Universidad Catolica del Norte").aggregate(Sum('contador_visitas'))
    contador_uv = noticias.filter(id_universidad__nombre__contains="Universidad de Valparaiso").aggregate(Sum('contador_visitas'))

    # Asigna los contadores al diccionario contador
    contador = {'upla':contador_upla, 'pucv':contador_pucv, 'ucn':contador_ucn, 'ufsm':contador_ufsm, 'uv':contador_uv, 'mejores_noticia_pucv':mejores_noticia_pucv}

    # Variables que se envían a la vista
    context = {'noticias':noticias , 'contador':contador}
    return render(request, 'news/estadisticas.html', context)

def region(request, region):
    noticias = Noticias.objects.order_by('-fecha').filter(id_universidad__region__contains=region)
    context = {'noticias':noticias, 'region':region}
    return render(request, 'news/region.html', context)

def categoria(request, categoria):
    noticias = Noticias.objects.order_by('-fecha').filter(categoria=categoria)
    context = {'noticias':noticias, 'categoria':categoria}
    return render(request, 'news/categoria.html', context)

def universidad(request, universidad):
    noticias = Noticias.objects.order_by('-fecha').filter(id_universidad__nombre__contains=universidad)
    context = {'noticias':noticias, 'universidad':universidad}
    return render(request, 'news/universidad.html', context)

