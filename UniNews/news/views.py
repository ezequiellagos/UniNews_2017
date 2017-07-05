# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.http import HttpResponse

from .models import Universidad, Noticias


def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
    ultimas_noticias = Noticias.objects.order_by('-fecha')
    #universidad = Universidad.objects.filter(id_universidad=ultimas_noticias['id_universidad'])

    universidades = Universidad.objects.get(id_universidad=1)
    universidad = universidades


    context = {'ultimas_noticias': ultimas_noticias, 'universidade':universidad}
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
    noticias = Noticias.objects.order_by('-contador_visitas')
    context = {'noticias':noticias}
    return render(request, 'news/estadisticas.html', context)

def region(request, region):
    noticias = Noticias.objects.order_by('-fecha')
    context = {'region_noticia':region_noticia}
    return render(request, 'news/region.html', context)

def categoria(request, categoria):
    noticias = Noticias.objects.order_by('-fecha')
    context = {'categoria_noticia':categoria_noticia}
    return render(request, 'news/categoria.html', context)

