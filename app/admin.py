from django.contrib import admin

from .models import *
from django.contrib.auth.models import Permission

admin.site.register(Permission)
admin.site.register(Medico)
admin.site.register(Paciente)
admin.site.register(Administrador)
admin.site.register(Establecimiento)
admin.site.register(Enfermedad)
admin.site.register(SolicitudEnfermedad)
admin.site.register(Ticket)
admin.site.register(AtencionPacienteAmbulatorio)
admin.site.register(AtencionPacienteUrgencia)

