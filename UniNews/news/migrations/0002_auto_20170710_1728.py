# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-10 21:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='noticias',
            options={'managed': False, 'verbose_name_plural': 'Noticias'},
        ),
        migrations.AlterModelOptions(
            name='universidad',
            options={'managed': False, 'verbose_name_plural': 'Universidades'},
        ),
    ]
