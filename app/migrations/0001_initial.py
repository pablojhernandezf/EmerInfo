# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-29 17:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Administrador',
            fields=[
                ('rut_admin', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nombres', models.CharField(max_length=30)),
                ('apellido_paterno', models.CharField(max_length=15)),
                ('apellido_materno', models.CharField(max_length=15)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AtencionPacienteAmbulatorio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_atencion_hora', models.DateTimeField()),
                ('observacion_publica', models.TextField()),
                ('observacion_medica', models.TextField()),
                ('tratamiento', models.TextField()),
            ],
            options={
                'get_latest_by': 'fecha_atencion_hora',
            },
        ),
        migrations.CreateModel(
            name='AtencionPacienteUrgencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_atencion_hora', models.DateTimeField()),
                ('rut_encargado', models.CharField(max_length=10)),
                ('nombre_encargado', models.CharField(max_length=15)),
                ('cargo_encargado', models.CharField(max_length=20)),
                ('tratamiento', models.TextField()),
                ('observacion_urgencia', models.TextField()),
            ],
            options={
                'get_latest_by': 'fecha_atencion_hora',
            },
        ),
        migrations.CreateModel(
            name='Enfermedad',
            fields=[
                ('id_who', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=30)),
                ('clasificacion', models.CharField(max_length=15)),
                ('riesgo', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Establecimiento',
            fields=[
                ('codigo_establecimiento', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=30)),
                ('direccion', models.CharField(max_length=15)),
                ('nombre_comuna', models.CharField(max_length=15)),
                ('region', models.CharField(max_length=2)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Medico',
            fields=[
                ('rut_medico', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nombres', models.CharField(max_length=30)),
                ('apellido_paterno', models.CharField(max_length=15)),
                ('apellido_materno', models.CharField(max_length=15)),
                ('fono', models.CharField(blank=True, max_length=12, null=True)),
                ('direccion', models.CharField(max_length=30)),
                ('email', models.CharField(blank=True, max_length=30, null=True)),
                ('especialidad', models.CharField(blank=True, max_length=15, null=True)),
                ('user', models.OneToOneField(max_length=15, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('rut_paciente', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nombres', models.CharField(max_length=30)),
                ('apellido_paterno', models.CharField(max_length=15)),
                ('apellido_materno', models.CharField(max_length=15)),
                ('sexo', models.CharField(max_length=1)),
                ('fecha_nacimiento', models.DateField()),
                ('fono', models.CharField(blank=True, max_length=12, null=True)),
                ('fono_emergencia', models.CharField(blank=True, max_length=12, null=True)),
                ('direccion', models.CharField(max_length=30)),
                ('email', models.EmailField(blank=True, max_length=30, null=True)),
                ('peso', models.DecimalField(decimal_places=1, max_digits=4)),
                ('estatura', models.DecimalField(decimal_places=1, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='SolicitudEnfermedad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut_admin', models.CharField(max_length=10)),
                ('id_who', models.CharField(max_length=7)),
                ('observacion', models.TextField()),
                ('estado', models.CharField(max_length=1)),
                ('rut_medico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Medico')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut_admin', models.CharField(blank=True, max_length=10)),
                ('fecha_emitido', models.DateField()),
                ('descripcion', models.TextField()),
                ('respuesta', models.TextField()),
                ('rut_medico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Medico')),
            ],
        ),
        migrations.AddField(
            model_name='atencionpacienteurgencia',
            name='codigo_establecimiento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Establecimiento'),
        ),
        migrations.AddField(
            model_name='atencionpacienteurgencia',
            name='id_who',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Enfermedad'),
        ),
        migrations.AddField(
            model_name='atencionpacienteurgencia',
            name='rut_paciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Paciente'),
        ),
        migrations.AddField(
            model_name='atencionpacienteambulatorio',
            name='codigo_establecimiento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Establecimiento'),
        ),
        migrations.AddField(
            model_name='atencionpacienteambulatorio',
            name='id_who',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Enfermedad'),
        ),
        migrations.AddField(
            model_name='atencionpacienteambulatorio',
            name='rut_medico',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Medico'),
        ),
        migrations.AddField(
            model_name='atencionpacienteambulatorio',
            name='rut_paciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Paciente'),
        ),
        migrations.AlterUniqueTogether(
            name='atencionpacienteurgencia',
            unique_together=set([('rut_paciente', 'fecha_atencion_hora')]),
        ),
        migrations.AlterUniqueTogether(
            name='atencionpacienteambulatorio',
            unique_together=set([('rut_paciente', 'fecha_atencion_hora')]),
        ),
    ]
