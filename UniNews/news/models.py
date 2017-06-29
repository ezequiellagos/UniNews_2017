# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Noticias(models.Model):
    id_noticia = models.IntegerField()
    titulo = models.CharField(max_length=200)
    bajada = models.TextField()
    fecha = models.DateField()
    link_noticia = models.CharField(max_length=200)
    link_recurso = models.CharField(max_length=200)
    id_universidad = models.ForeignKey('Universidad', models.DO_NOTHING, db_column='id_universidad')

    categoria = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'noticias'


class Universidad(models.Model):
    id_universidad = models.IntegerField()
    nombre = models.CharField(max_length=100)
    region = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'universidad'