# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Noticias(models.Model):
    id_noticia = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=200)
    bajada = models.TextField()
    fecha = models.DateField(blank=True, null=True)
    link_noticia = models.CharField(max_length=200)
    link_recurso = models.CharField(max_length=200)
    id_universidad = models.ForeignKey('Universidad', models.DO_NOTHING, db_column='id_universidad')
    categoria = models.CharField(max_length=100)
    contador_visitas = models.IntegerField(null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'noticias'
        verbose_name_plural = 'Noticias'


class Universidad(models.Model):
    id_universidad = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    region = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'universidad'
        verbose_name_plural = 'Universidades'

    def __str__(self):
        return '{}'.format(self.nombre)
