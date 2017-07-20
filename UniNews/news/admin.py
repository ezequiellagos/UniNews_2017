# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Universidad, Noticias

# Register your models here.

class UniversidadAdmin(admin.ModelAdmin):
	# Campos a editar
	fields = ['id_universidad', 'nombre','region']
	# Campos para mostrar
	list_display = ('id_universidad', 'nombre','region')

class NoticiasAdmin(admin.ModelAdmin):
	fields = ['id_noticia', 'titulo','bajada', 'link_noticia', 'link_recurso', 'categoria', 'contador_visitas', 'id_universidad']
	list_display = ('titulo','categoria','id_universidad')
	list_filter = ('categoria','id_universidad')

admin.site.register(Universidad, UniversidadAdmin)
admin.site.register(Noticias, NoticiasAdmin)