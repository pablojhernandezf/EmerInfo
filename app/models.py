"""
Definition of models.
"""

from django.db import models

# Create your models here.
"""
Definition of models.
"""


from django.db import models
from datetime import datetime
from django.contrib.auth.models import User




# Create your models here.

class Medico(models.Model):
    rut_medico = models.CharField(primary_key=True, max_length=10)
    nombres = models.CharField(max_length=30)
    apellido_paterno = models.CharField(max_length=15)
    apellido_materno = models.CharField(max_length=15)
    fono = models.CharField(max_length=12, blank=True, null=True)
    direccion = models.CharField(max_length=30)
    email = models.CharField(max_length=30, blank=True, null=True)
    especialidad = models.CharField(max_length=15, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, max_length =15)

    
    def __str__ (self):
        return (self.rut_medico)

class Administrador(models.Model):
    rut_admin = models.CharField(primary_key=True, max_length=10)
    nombres = models.CharField(max_length=30)
    apellido_paterno = models.CharField(max_length=15)
    apellido_materno = models.CharField(max_length=15)
    email = models.CharField(max_length=30, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return(self.rut_admin)

class Establecimiento (models.Model):
    codigo_establecimiento = models.CharField(primary_key=True, max_length=6)
    nombre = models.CharField(max_length=30)
    direccion = models.CharField(max_length=30)
    nombre_comuna = models.CharField(max_length=15)
    region = models.IntegerField()
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return(self.codigo_establecimiento)

class Paciente (models.Model):
    rut_paciente = models.CharField(primary_key=True, max_length=10)
    nombres = models.CharField(max_length=30)
    apellido_paterno = models.CharField(max_length=15)
    apellido_materno = models.CharField(max_length=15)
    sexo = models.CharField(max_length=1)
    fecha_nacimiento = models.DateField()
    fono = models.CharField(max_length=12, blank=True, null=True)
    fono_emergencia = models.CharField(max_length=12, blank=True, null=True)
    direccion = models.CharField(max_length=30)
    email = models.EmailField(max_length=30, blank=True, null=True)
    peso = models.DecimalField(null=False,max_digits=4,decimal_places=1)
    estatura = models.DecimalField(null=False,max_digits=3,decimal_places=2)
   
    
    
    
    def __str__ (self):
        return (self.rut_paciente)


class AtencionPacienteUrgencia(models.Model):
    rut_paciente = models.ForeignKey('Paciente',on_delete=models.CASCADE)
    codigo_establecimiento = models.ForeignKey('Establecimiento',on_delete=models.CASCADE)
    id_who = models.ForeignKey('Enfermedad',on_delete=models.CASCADE)
    fecha_atencion_hora = models.DateTimeField()
    rut_encargado = models.CharField(max_length=10)
    nombre_encargado = models.CharField(max_length=15)
    cargo_encargado = models.CharField(max_length=20)
    tratamiento =models.TextField()
    observacion_urgencia=models.TextField()
    
    class Meta:
        unique_together = (('rut_paciente', 'fecha_atencion_hora'),)
        get_latest_by = 'fecha_atencion_hora'

    def __str__ (self):
        return (str(self.fecha_atencion_hora))

class AtencionPacienteAmbulatorio (models.Model):
    rut_paciente = models.ForeignKey('Paciente',on_delete=models.CASCADE)
    rut_medico = models.ForeignKey('Medico',on_delete=models.CASCADE)
    id_who = models.ForeignKey('Enfermedad',on_delete=models.CASCADE)
    codigo_establecimiento=models.ForeignKey('Establecimiento', on_delete=models.CASCADE)
    fecha_atencion_hora = models.DateTimeField()
    observacion_publica=models.TextField()
    observacion_medica=models.TextField()
    tratamiento = models.TextField()

    class Meta:
        unique_together = (('rut_paciente', 'fecha_atencion_hora'),)
        get_latest_by = 'fecha_atencion_hora'
    def __str__ (self):
        return (str(self.fecha_atencion_hora))




class Enfermedad (models.Model):
    id_who = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=30)
    clasificacion = models.CharField(max_length=15)
    riesgo = models.CharField(max_length=15)
    
    def __str__ (self):
        return str(self.id_who)

class SolicitudEnfermedad (models.Model):
    
    rut_admin = models.CharField( max_length=10)
    rut_medico=models.ForeignKey('Medico', on_delete=models.CASCADE)   
    id_who = models.CharField(max_length=7)
    observacion = models.TextField()
    estado = models.CharField(max_length=30)
    


class Ticket (models.Model):
    
    rut_medico = models.ForeignKey('Medico',on_delete=models.CASCADE)
    rut_admin  = models.CharField(max_length=10, blank=True )
    fecha_emitido = models.DateField()
    descripcion =models.TextField()
    respuesta =models.TextField( )

