"""
Definition of urls for TrabajoTitulo4.
"""
from app.views import *
from datetime import datetime
from django.conf.urls import url

from django.contrib.auth import views as auth_views

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin


urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^(?P<rut>0*(\d{1,3}(\.?\d{3})*)\-?([\dkK]))$', app.views.infoPaciente, name='info paciente'),
    #Medico
    url(r'^registrar_medico/$', app.views.registrarMedico, name='registrar medico'),
    url(r'^actualizar_medico/$', app.views.actualizarMedico, name='actualizar medico'),
    url(r'^eliminar_medico/$', app.views.eliminarMedico, name='eliminar medico'),
    url(r'^listar_medico/$', app.views.listarMedico, name='listar medico'),
    url(r'^ingresar_atencion/$', app.views.ingresarAtencionAmbulatoria, name='ingresar atencion ambulatoria'),
    url(r'^consultar_atencion/$', app.views.consultarAtencionAmbulatoria, name='consultar atencion ambulatoria'),
    url(r'^ingresar_solicitud_enf/$', app.views.ingresarSolicitudEnfermedad, name='ingresar solicitud enfermedad'),
    url(r'^ingresar_ticket/$', app.views.ingresarTicketAsistencia, name='ingresar ticket asistencia'),
    url(r'^mis_tickets/$', app.views.misTickets, name='mis tickets'),
    url(r'^solicitudes/$', app.views.Solicitudes, name='solicitudes'),
    #paciente
    url(r'^registrar_paciente/$', app.views.registrarPaciente, name='registrar paciente'),
    url(r'^consultar_paciente/$', app.views.consultarPaciente, name='consultar paciente'),
    url(r'^modificar_paciente/$', app.views.modificarPaciente, name='modificar paciente'),
    
    #Establecimiento
    url(r'^registrar_establecimiento/$', app.views.registrarEstablecimiento, name='registrar establecimiento'),
    url(r'^actualizar_establecimiento/$', app.views.actualizarEstablecimiento, name='actualizar establecimiento'),
    url(r'^listar_establecimiento/$', app.views.listarEstablecimiento, name='listar establecimiento'),
    url(r'^ingresar_atencion_urg/$', app.views.ingresarAtencionUrgencia, name='ingresar atencion urgencia'),
    url(r'^consultar_atencion_urg/$', app.views.consultarAtencionUrgencia, name='consultar atencion urgencia'),
    url(r'^eliminar_establecimiento/$', app.views.eliminarEstablecimiento, name='eliminar establecimiento'),
    
    #Administrador
    url(r'^registrar_admin/$', app.views.registrarAdministrador, name='registrar administrador'),
    url(r'^modificar_administrador/$', app.views.modificarAdministrador, name='modificar administrador'),
    url(r'^eliminar_administrador/$', app.views.eliminarAdministrador, name='eliminar administrador'),
    url(r'^revisar_ticket/$', app.views.revisarTicket, name='revisar ticket'),
    url(r'^revisar_solicitud/$', app.views.revisarSolicitud, name='revisar solicitud'),
   
    #Ticket y Solicitud
    url(r'^pagina_ticket/(?P<numero_ticket>[0-9]+)$', app.views.paginaTicket, name='pagina ticket'),
    url(r'^revisar_solicitud/(?P<numero_solicitud>[0-9]+)$', app.views.paginaSolicitud, name='pagina solicitud'),
    #Utilitarios
    url(r'^estadisticas/$', app.views.generarEstadisticas, name='generar estadisticas'),
    url(r'^recuperar_cuenta/$', app.views.recuperarCuenta, name='recuperar cuenta'),
    #password reset con mail
    url(r'^password_reset/$', auth_views.password_reset, name='password reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, {
        
        'post_reset_redirect': '/',
    }, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    
    url(r'^login/$',
        auth_views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        auth_views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
]
