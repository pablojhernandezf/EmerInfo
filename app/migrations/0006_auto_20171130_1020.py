# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-30 13:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_administrador_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='establecimiento',
            name='region',
            field=models.IntegerField(max_length=2),
        ),
    ]