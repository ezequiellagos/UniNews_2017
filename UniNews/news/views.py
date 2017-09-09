# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
# from django.http import HttpResponse

from .models import Universidad, Noticias
from django.db.models import Max,Sum
from django.conf import settings

from datetime import datetime, date, time, timedelta
import calendar


def paginacion(noticias_object, request, noticias_por_pagina=12):
    paginacion = Paginator(noticias_object, noticias_por_pagina)
    page = request.GET.get('page')
    try:
        noticias = paginacion.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        noticias = paginacion.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        noticias = paginacion.page(paginacion.num_pages)
    return noticias

def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")

    # Formato de Fecha
    hoy = datetime.today()
    semana_atras = date.today() - timedelta(days=14)
    formato = "%Y-%m-%d" # AAAA-MM-DD
    fecha_actual = hoy.strftime(formato)
    fecha_pasada = semana_atras.strftime(formato)
    # Fin Formato Fecha

    ultimas_noticias = Noticias.objects.order_by('-fecha')
    noticias_mas_vistas = Noticias.objects.filter(fecha__range=[fecha_pasada, fecha_actual]).order_by('-contador_visitas')[:3]


    noticias = paginacion(ultimas_noticias, request)

    context = {'noticias_mas_vistas' :noticias_mas_vistas, 'noticias': noticias}
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
    # Formato de Fecha
    hoy = datetime.today()
    semana_atras = date.today() - timedelta(days=14)
    formato = "%Y-%m-%d" # AAAA-MM-DD
    fecha_actual = hoy.strftime(formato)
    fecha_pasada = semana_atras.strftime(formato)
    # Fin Formato Fecha

    noticias = Noticias.objects.order_by('-fecha').filter(id_universidad__region__contains=region)
    noticias_mas_vistas = Noticias.objects.filter(id_universidad__region__contains=region).filter(fecha__range=[fecha_pasada, fecha_actual]).order_by('-contador_visitas')[:3]

    noticias = paginacion(noticias, request)

    context = {'noticias':noticias, 'region':region, 'noticias_mas_vistas':noticias_mas_vistas}
    return render(request, 'news/region.html', context)

def categoria(request, categoria):
    # Formato de Fecha
    hoy = datetime.today()
    semana_atras = date.today() - timedelta(days=14)
    formato = "%Y-%m-%d" # AAAA-MM-DD
    fecha_actual = hoy.strftime(formato)
    fecha_pasada = semana_atras.strftime(formato)
    # Fin Formato Fecha

    noticias = Noticias.objects.order_by('-fecha').filter(categoria=categoria)
    noticias_mas_vistas = Noticias.objects.filter(categoria__contains=categoria).filter(fecha__range=[fecha_pasada, fecha_actual]).order_by('-contador_visitas')[:3]

    noticias = paginacion(noticias, request)

    context = {'noticias':noticias, 'categoria':categoria, 'noticias_mas_vistas':noticias_mas_vistas}
    return render(request, 'news/categoria.html', context)

def universidad(request, universidad):
    # Formato de Fecha
    hoy = datetime.today()
    semana_atras = date.today() - timedelta(days=14)
    formato = "%Y-%m-%d" # AAAA-MM-DD
    fecha_actual = hoy.strftime(formato)
    fecha_pasada = semana_atras.strftime(formato)
    # Fin Formato Fecha

    noticias = Noticias.objects.order_by('-fecha').filter(id_universidad__nombre__contains=universidad)
    noticias_mas_vistas = Noticias.objects.filter(id_universidad__nombre__contains=universidad).filter(fecha__range=[fecha_pasada, fecha_actual]).order_by('-contador_visitas')[:3]

    noticias = paginacion(noticias, request)

    context = {'noticias':noticias, 'universidad':universidad, 'noticias_mas_vistas':noticias_mas_vistas}
    return render(request, 'news/universidad.html', context)

