# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-01 18:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20171130_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudenfermedad',
            name='estado',
            field=models.CharField(max_length=30),
        ),
    ]
