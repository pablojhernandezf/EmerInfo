"""
Definition of views.
"""

from django.shortcuts import render,get_object_or_404,render_to_response

from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from app.models import *
from app.forms import *
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import Group
import csv
def home(request):
    
        if request.method == 'POST':
            form = SearchForm(request.POST)
            if form.is_valid():
                try:
                    rut=form.cleaned_data['rut_paciente']
                    rut_limpio= rut.replace('.','')
                    atencion = AtencionPacienteAmbulatorio.objects.filter(rut_paciente__exact=rut_limpio).latest()
                    paciente = Paciente.objects.get(rut_paciente__exact=rut_limpio)
                except:
                    return render(request, '../templates/app/no_info.html')
                
                return render(request, '../templates/app/info_paciente.html', {'atencion': atencion,'paciente':paciente})
        else:
            form = SearchForm()
        return render(request, '../templates/app/index.html', {'form': form,'title':'Home Page',
            'year':datetime.now().year,})


    

def infoPaciente(request,rut):
    if request.user.is_authenticated:
            
        try:
            rut_limpio=rut.replace('.','')
            atencion = AtencionPacienteAmbulatorio.objects.filter(rut_paciente__exact=rut_limpio).latest()
            paciente = Paciente.objects.get(rut_paciente__exact=rut_limpio)
        except:
            return render(request, '../templates/app/no_info.html')
        return render(request, '../templates/app/info_clinica.html', {'atencion': atencion,'paciente':paciente})
    else:
        rut_limpio=rut.replace('.','')
        try:
            atencion = AtencionPacienteAmbulatorio.objects.filter(rut_paciente__exact=rut_limpio).latest()
            paciente = Paciente.objects.get(rut_paciente__exact=rut_limpio)
        except:
            return render(request, '../templates/app/no_info.html')
        return render(request, '../templates/app/info_publica.html', {'atencion': atencion,'paciente':paciente})
   
################################################################MEDICO####################################################
def registrarMedico(request):

    if request.method == 'POST':
        form = RegistrationFormMedico(request.POST)
        if form.is_valid():
            userm = form.cleaned_data['user']
            passw1m = form.cleaned_data['password1']
            passw2m = form.cleaned_data['password2']
            emailm = form.cleaned_data['email']
            
            
            new_user = User.objects.create_user(username=userm,
                                 email=emailm,
                                 password=passw1m)
                
            
            new_user.save()

            rutm = form.cleaned_data['rut_medico']
            nombresm = form.cleaned_data['nombres']
            apellidopm = form.cleaned_data['apellido_paterno']
            apellidomm = form.cleaned_data['apellido_materno']
            fonom= form.cleaned_data['fono']
            direccionm = form.cleaned_data['direccion']
                
            especialidadm = form.cleaned_data['especialidad']
                
            new_medico = Medico(rut_medico=rutm,nombres=nombresm,apellido_paterno=apellidopm,
                                    apellido_materno=apellidomm,fono=fonom,direccion=direccionm,
                                    email=emailm,especialidad=especialidadm )
            user_tran = User.objects.get(username=userm)
            new_medico.user = user_tran
            g = Group.objects.get(name='Medico') 
            g.user_set.add(user_tran)
            new_medico.save()
            
            
            
            username = userm
            raw_password = passw1m
            user = authenticate(username=userm, password=passw1m)
            login(request, user)
                
            return redirect('home')
     
    else:
        form = RegistrationFormMedico()
    return render(request, '../templates/app/registrar_medico.html', {'form': form})



def actualizarMedico(request):
    try:
        current_user = request.user
        current_username = str(current_user.username)
        medico = Medico.objects.get(user__username__exact=current_username)
        
    except:
        messages.warning(request, 'No puedes realizar esta acción sin estar autenticado', extra_tags='alert')
        return redirect('home')

    data = {'nombres': medico.nombres,
            'apellido_paterno': medico.apellido_paterno,
            'apellido_materno': medico.apellido_materno,
            'email': medico.email,
            'fono': medico.fono,
            'direccion': medico.direccion,
            'especialidad': medico.especialidad,
            }
    form = UpdateFormMedico(data,username = current_username)
    
    if request.method == 'POST':    #terminar la actualizacion con el commit
        form = UpdateFormMedico(request.POST,username =current_username)
        if form.is_valid():
            nombresm = form.cleaned_data['nombres']
            apellido_paternom = form.cleaned_data['apellido_paterno']
            apellido_maternom = form.cleaned_data['apellido_materno']
            emailm = form.cleaned_data['email']
            fonom = form.cleaned_data['fono']
            direccionm = form.cleaned_data['direccion']
            especialidadm = form.cleaned_data['especialidad']
            Medico.objects.filter(user__username__exact=current_username).update(nombres=nombresm)
            Medico.objects.filter(user__username__exact=current_username).update(apellido_paterno=apellido_paternom)
            Medico.objects.filter(user__username__exact=current_username).update(apellido_materno=apellido_maternom)
            Medico.objects.filter(user__username__exact=current_username).update(email=emailm)
            Medico.objects.filter(user__username__exact=current_username).update(fono=fonom)
            Medico.objects.filter(user__username__exact=current_username).update(direccion=direccionm)
            Medico.objects.filter(user__username__exact=current_username).update(especialidad=especialidadm)
            User.objects.filter(username = current_username).update(email=emailm)
            return redirect('home')
            
    return render(request,'../templates/app/actualizar_medico.html', {'form':form})


def eliminarMedico(request):
    try:
        current_user = request.user
        current_username = str(current_user.username)
        medico = Medico.objects.get(user__username__exact=current_username)
    except:
        messages.info(request, 'No puedes realizar esta acción sin estar autenticado')
        return redirect('home')
    if request.method == 'POST':
        logout(request)
        current_user.is_active = False
        current_user.save()
        return redirect('home')

    return render(request,'../templates/app/eliminar_cuenta.html') 

def listarMedico(request):
    
    if request.method == 'POST':
        form = ListFormMedico(request.POST)
        if form.is_valid():
            filtro=int(form.cleaned_data['filtro'])
            busqueda=form.cleaned_data['busqueda']
            
            #return render(request, '../templates/app/listar_medico.html', {'prueba':prueba,'filtro':filtro,'busqueda':busqueda})
            if filtro==1:
                medico= Medico.objects.filter(rut_medico__exact=busqueda)
                return render(request, '../templates/app/listar_medico.html', {'form': form,'medico':medico}) 
            elif filtro==2:
                medico= Medico.objects.filter(nombres__contains=busqueda)
                return render(request, '../templates/app/listar_medico.html', {'form': form,'medico':medico,}) 
            elif filtro==3:
                medico= Medico.objects.filter(apellido_paterno__contains=busqueda)
                return render(request, '../templates/app/listar_medico.html', {'form': form,'medico':medico,}) 
            elif filtro==4:
                medico= Medico.objects.filter(especialidad__contains=busqueda)
                return render(request, '../templates/app/listar_medico.html', {'form': form,'medico':medico,}) 
                
    else:
        medico = Medico.objects.all()
        form= ListFormMedico()

    return render(request, '../templates/app/listar_medico.html', {'form': form,'medico':medico})

def misTickets(request):
    try:
        current_user = request.user
        current_username = str(current_user.username)
        medico = Medico.objects.get(user__username__exact=current_username)
    except:
        messages.info(request, 'No puedes realizar esta acción sin estar autenticado')
        return redirect('home')
    tickets = Ticket.objects.filter(rut_medico=medico.rut_medico)

    return render(request, '../templates/app/listar_tickets.html', {'tickets' : tickets})
    
def Solicitudes(request):
    try:
        current_user = request.user
        current_username = str(current_user.username)
        medico = Medico.objects.get(user__username__exact=current_username)
        solicitudes = SolicitudEnfermedad.objects.filter(rut_medico=medico.rut_medico)
    except:
        messages.info(request, 'No puedes realizar esta acción sin estar autenticado')
        return redirect('home')
    

    return render(request, '../templates/app/listar_solicitudes.html', {'solicitudes': solicitudes})







######################################################################ESTABLECIMIENTO##############################################
def registrarEstablecimiento(request):
     if request.method == 'POST':
        form = RegistrationFormEstablecimiento(request.POST)
        if form.is_valid():

            user = form.cleaned_data['user']
            passw1 = form.cleaned_data['password1']
            passw2 = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            codigo_establecimiento=form.cleaned_data['codigo_establecimiento']
            
            #crear usuario con contrasenha 
           
            new_user = User.objects.create_user(username=user,
                                 email=email,
                                 password=passw1)
            
            new_user.save()


            ubicacion_directorio=os.path.dirname(__file__)
            ubicacion_archivo='Establecimientos.csv'
            ubicacion_completa = os.path.join(ubicacion_directorio, ubicacion_archivo)
            
            with open(ubicacion_completa, 'rt') as csvfile:
                my_content = csv.reader(csvfile, delimiter=',')
                for row in my_content:
                    if codigo_establecimiento in row:
                       nombre=row[10]
                       direccion=row[11]
                       nombre_comuna=row[4]
                       region=row[0]
                
            new_establecimiento = Establecimiento(codigo_establecimiento=codigo_establecimiento,nombre=nombre,
                                                  direccion=direccion,nombre_comuna=nombre_comuna,region=region )
            user_tran = User.objects.get(username=user)
            new_establecimiento.user = user_tran
            g = Group.objects.get(name='Establecimiento') 
            g.user_set.add(user_tran)
            new_establecimiento.save()
            
            username = user
            raw_password = passw1
            user = authenticate(username=user, password=passw1)
            login(request, user)
                
            return redirect('home')
     
     else:
        form = RegistrationFormEstablecimiento()
     return render(request, '../templates/app/registrar_establecimiento.html', {'form': form})
   

def actualizarEstablecimiento(request):
    try:
        current_user = request.user
        current_username = str(current_user.username)
        establecimiento = Establecimiento.objects.get(user__username__exact=current_username)
        
    except:
        messages.warning(request, 'No puedes realizar esta acción sin estar autenticado', extra_tags='alert')
        return redirect('home')
    
    data = {'email': current_user.email,}
    form = UpdateFormEstablecimiento(data,username=current_username)
    
    if request.method == 'POST':    #terminar la actualizacion con el commit
        form = UpdateFormEstablecimiento(request.POST,username =current_username)
        if form.is_valid():
            
            email = form.cleaned_data['email']
            User.objects.filter(username__exact=current_username).update(email=email)
            return redirect('home')
            
    return render(request,'../templates/app/actualizar_establecimiento.html', {'form':form})

def listarEstablecimiento(request):
    if request.method == 'POST':
        form = ListFormEstablecimiento(request.POST)
        if form.is_valid():
            filtro=int(form.cleaned_data['filtro'])
            busqueda=form.cleaned_data['busqueda']

            if filtro==1:
                establecimientos= Establecimiento.objects.filter(codigo_establecimiento__exact=busqueda).exclude(codigo_establecimiento='00-000')
                return render(request, '../templates/app/listar_establecimiento.html', {'form': form,'establecimientos': establecimientos,}) 
            elif filtro==2:
                establecimientos= Establecimiento.objects.filter(nombre__iexact=busqueda).exclude(codigo_establecimiento='00-000')
                return render(request, '../templates/app/listar_establecimiento.html', {'form': form,'establecimientos': establecimientos,})  
            elif filtro==3:
                try:
                    busqueda=int(busqueda)
                except:
                    busqueda=98
                establecimientos= Establecimiento.objects.filter(region__exact=busqueda).exclude(codigo_establecimiento='00-000')
                return render(request, '../templates/app/listar_establecimiento.html', {'form': form,'establecimientos': establecimientos,})
            elif filtro==4:
                establecimientos= Establecimiento.objects.filter(nombre_comuna__iexact=busqueda).exclude(codigo_establecimiento='00-000')
                return render(request, '../templates/app/listar_establecimiento.html', {'form': form,'establecimientos': establecimientos,})
                
    else:
        establecimientos=Establecimiento.objects.all().exclude(codigo_establecimiento='00-000')
        form= ListFormEstablecimiento()

    return render(request, '../templates/app/listar_establecimiento.html', {'form': form,'establecimientos': establecimientos})

def eliminarEstablecimiento(request):
    try:
        current_user = request.user
        current_username = str(current_user.username)
    except:
        messages.info(request, 'No puedes realizar esta acción sin estar autenticado')
        return redirect('home')
    if request.method == 'POST':
        logout(request)
        current_user.is_active = False
        current_user.save()
        return redirect('home')

    return render(request,'../templates/app/eliminar_cuenta.html')
    


##########################PACIENTE######################################################
def registrarPaciente(request):
    if request.method == 'POST':
        form = RegistrationFormPaciente(request.POST)
        if form.is_valid():
            
            rutp = form.cleaned_data['rut_paciente']
            nombresp = form.cleaned_data['nombres']
            apellidopp = form.cleaned_data['apellido_paterno']
            apellidomp = form.cleaned_data['apellido_materno']
            sexop = form.cleaned_data['sexo']
            emailp = form.cleaned_data['email']
            fecha_nacimientop=form.cleaned_data['fecha_nacimiento']
            fonop= form.cleaned_data['fono']
            fono_emergenciap= form.cleaned_data['fono_emergencia']
            direccionp = form.cleaned_data['direccion']
            pesop = form.cleaned_data['peso']
            estaturap = form.cleaned_data['estatura']
   
            new_paciente = Paciente(rut_paciente=rutp,nombres=nombresp,apellido_paterno=apellidopp,
                                    apellido_materno=apellidomp,sexo=sexop,fecha_nacimiento=fecha_nacimientop,email=emailp,fono=fonop,fono_emergencia=fono_emergenciap,
                                    direccion=direccionp, peso=pesop,estatura=estaturap)
            new_paciente.save()
            
            
                
            return redirect('home')
     
    else:
        form = RegistrationFormPaciente()
    
    return render(request, '../templates/app/registrar_paciente.html', {'form': form})

def consultarPaciente(request):
    try:
        current_user = request.user
        current_username = str(current_user.username)
    except:
        messages.info(request, 'No puedes realizar esta acción sin estar autenticado')
        return redirect('home')

    if request.method == 'POST':
         form = ListFormPaciente(request.POST)
         if form.is_valid():
             rut_form=form.cleaned_data['rut_paciente']
             rut_limpio=rut_form.replace('.','')
             request.session['rut_paciente'] = rut_limpio
             paciente = Paciente.objects.get(rut_paciente=rut_limpio)
             return render(request, '../templates/app/pagina_paciente.html', {'paciente': paciente})
    else:
        form = ListFormPaciente()
    return render(request, '../templates/app/consultar_paciente.html', {'form': form})



def modificarPaciente(request):

    try:
        rut_paciente_session= request.session['rut_paciente']
        rut_limpio=rut_paciente_session.replace('.','')
        paciente = Paciente.objects.get(rut_paciente=rut_limpio)
    except:
        return redirect('consultar paciente')

    data = {'nombres': paciente.nombres,
            'apellido_paterno': paciente.apellido_paterno,
            'apellido_materno': paciente.apellido_materno,
            'sexo': paciente.sexo,
            'fecha_nacimiento': paciente.fecha_nacimiento.strftime('%d/%m/%Y'),
            'email': paciente.email,
            'fono': paciente.fono,
            'fono_emergencia': paciente.fono_emergencia,
            'direccion': paciente.direccion,
            'peso': paciente.peso,
            'estatura': paciente.estatura,
            }
    form = UpdateFormPaciente(data,rut_paciente=rut_paciente_session)
    
    if request.method == 'POST':    #terminar la actualizacion con el commit
        form = UpdateFormPaciente(request.POST,rut_paciente=rut_paciente_session)
        if form.is_valid():
            nombresp = form.cleaned_data['nombres']
            apellido_paternop = form.cleaned_data['apellido_paterno']
            apellido_maternop = form.cleaned_data['apellido_materno']
            sexop = form.cleaned_data['sexo']
            fecha_nacimientop = form.cleaned_data['fecha_nacimiento']
            fonop = form.cleaned_data['fono']
            fono_emergenciap = form.cleaned_data['fono_emergencia']
            emailp = form.cleaned_data['email']
            direccionp = form.cleaned_data['direccion']
            pesop = form.cleaned_data['peso']
            estaturap = form.cleaned_data['estatura']

            Paciente.objects.filter(rut_paciente__exact=rut_limpio).update(nombres=nombresp)
            Paciente.objects.filter(rut_paciente__exact=rut_limpio).update(apellido_paterno=apellido_paternop)
            Paciente.objects.filter(rut_paciente__exact=rut_limpio).update(apellido_materno=apellido_maternop)
            Paciente.objects.filter(rut_paciente__exact=rut_limpio).update(sexo=sexop)
            Paciente.objects.filter(rut_paciente__exact=rut_limpio).update(fecha_nacimiento=fecha_nacimientop)
            Paciente.objects.filter(rut_paciente__exact=rut_limpio).update(fono=fonop)
            Paciente.objects.filter(rut_paciente__exact=rut_limpio).update(fono_emergencia=fono_emergenciap)
            Paciente.objects.filter(rut_paciente__exact=rut_limpio).update(email=emailp)
            Paciente.objects.filter(rut_paciente__exact=rut_limpio).update(direccion=direccionp)
            Paciente.objects.filter(rut_paciente__exact=rut_limpio).update(peso=pesop)
            Paciente.objects.filter(rut_paciente__exact=rut_limpio).update(estatura=estaturap)


            
            return redirect('home')
            
    return render(request, '../templates/app/modificar_paciente.html', {'form': form})




################################ATENCIONES########################################################
def ingresarAtencionAmbulatoria(request):
    
    try:
        current_user = request.user
        current_username = str(current_user.username)
        medico = Medico.objects.get(user__username__exact=current_username)

        rut_paciente_session= request.session['rut_paciente']
        rut_limpio=rut_paciente_session.replace('.','')
        paciente = Paciente.objects.get(rut_paciente=rut_limpio)
        
    except:
        messages.info(request, 'No puedes realizar esta acción sin estar autenticado')
        return redirect('home')
    if request.method == 'POST':
        form = RegistrationFormAtencionAmbulatoria(request.POST)
        if form.is_valid():
            
            rut_paciente = rut_limpio
            fecha_atencion_hora = form.cleaned_data['fecha_atencion_hora']
            tratamiento = form.cleaned_data['tratamiento']
            observacion_medica = form.cleaned_data['observacion_medica']
            observacion_publica = form.cleaned_data['observacion_publica']
            codigo_establecimiento = form.cleaned_data['codigo_establecimiento']
            id_who= form.cleaned_data['id_who']
            
            paciente = Paciente.objects.get(rut_paciente=rut_paciente)
            establecimiento= Establecimiento.objects.get(codigo_establecimiento=codigo_establecimiento)
            enfermedad = Enfermedad.objects.get(id_who=str(id_who))
            
          
            new_atencion = AtencionPacienteAmbulatorio(fecha_atencion_hora=fecha_atencion_hora,rut_paciente=paciente,tratamiento=tratamiento,
                                                       observacion_medica=observacion_medica,observacion_publica=observacion_publica,codigo_establecimiento=establecimiento,
                                                       rut_medico=medico,id_who=enfermedad)
            new_atencion.save()
            
            
                
            return redirect('home')
     
    else:
        try:
            atencion = AtencionPacienteAmbulatorio.objects.filter(rut_paciente=rut_limpio).latest()
            data = {'observacion_publica': atencion.observacion_publica,
                   
                'observacion_medica': atencion.observacion_medica,}
            form =RegistrationFormAtencionAmbulatoria(initial=data)
        except:
            form =RegistrationFormAtencionAmbulatoria()
    return render(request, '../templates/app/ingresar_atencion_ambulatoria.html', {'form': form})



def ingresarAtencionUrgencia(request):
    try:
        current_user = request.user
        current_username = str(current_user.username)
        establecimiento = Establecimiento.objects.get(user__username__exact=current_username)
    except:
        return redirect('home')
    
    if request.method == 'POST':
        form = RegistrationFormAtencionUrgencia(request.POST)
        if form.is_valid():
            
            rut_paciente = form.cleaned_data['rut_paciente']
            fecha_atencion_hora = form.cleaned_data['fecha_atencion_hora']
            tratamiento = form.cleaned_data['tratamiento']
            observacion_urgencia = form.cleaned_data['observacion_urgencia']
            rut_encargado_urgencia = form.cleaned_data['rut_encargado_urgencia']
            nombre_encargado_urgencia = form.cleaned_data['nombre_encargado_urgencia']
            cargo_encargado_urgencia = form.cleaned_data['cargo_encargado_urgencia']
            codigo_establecimiento = establecimiento.codigo_establecimiento
            id_who= form.cleaned_data['id_who']
            
            paciente = Paciente.objects.get(rut_paciente=rut_paciente)
            enfermedad= Enfermedad.objects.get(id_who__exact=id_who)
            establecimiento= Establecimiento.objects.get(codigo_establecimiento=codigo_establecimiento)
            try:
                atenciones = AtencionPacienteAmbulatorio.objects.filter(rut_paciente= rut_paciente).values('rut_medico').distinct()
                mails=[]
            
                for atencion in atenciones:
                    rut_medico=atencion['rut_medico']
                    medico = Medico.objects.get(rut_medico=rut_medico)
                    mails.append(medico.email)

           
            

                send_mail('Ingreso de paciente a Sala de Urgencias de paciente '+str(paciente.rut_paciente)+' '+str(paciente.nombres)+' '+str(paciente.apellido_paterno)+' '+str(paciente.apellido_materno) , 
                          'El paciente ha sido atendido en '+str(establecimiento.nombre)+' a causa de : '+str(enfermedad.nombre)+' ', 'noreply@sistema.cl', mails)
            except:
                render(request, '../templates/app/problema_mail.html')
            
            new_atencion = AtencionPacienteUrgencia(fecha_atencion_hora=fecha_atencion_hora,rut_paciente=paciente,tratamiento=tratamiento,
                                                       observacion_urgencia=observacion_urgencia, cargo_encargado=cargo_encargado_urgencia,
                                                       rut_encargado=rut_encargado_urgencia,
                                                       codigo_establecimiento=establecimiento,id_who=enfermedad)
            new_atencion.save()
            
            
            
                
            return redirect('home')
     
    else:
        form =RegistrationFormAtencionUrgencia()
    return render(request, '../templates/app/ingresar_atencion_urgencia.html', {'form': form})

def consultarAtencionAmbulatoria(request):
    try:
        rut_paciente_session= request.session['rut_paciente']
        rut_limpio=rut_paciente_session.replace('.','')
        paciente = Paciente.objects.get(rut_paciente=rut_limpio)
    except:
        return redirect('consultar paciente')
    
    atenciones = AtencionPacienteAmbulatorio.objects.filter(rut_paciente__exact=rut_limpio)

    enfermedades =[]
    for atencion in atenciones:
        enfermedad = Enfermedad.objects.get(id_who=atencion.id_who)
        enfermedades.append(enfermedad)
    lista = zip(atenciones,enfermedades)
    
    return render(request, '../templates/app/listado_atencion_ambulatoria.html', {'lista': lista})
        

def consultarAtencionUrgencia(request):
    try:
        rut_paciente_session= request.session['rut_paciente']
        rut_limpio=rut_paciente_session.replace('.','')
        paciente = Paciente.objects.get(rut_paciente=rut_limpio)
    except:
        return redirect('consultar paciente')

    atenciones = AtencionPacienteUrgencia.objects.filter(rut_paciente__exact=rut_limpio)
    enfermedades =[]
    for atencion in atenciones:
        enfermedad = Enfermedad.objects.get(id_who=atencion.id_who)
        enfermedades.append(enfermedad)
    lista = zip(atenciones,enfermedades)
    return render(request, '../templates/app/listado_atencion_urgencia.html', {'lista': lista})
    
    #return render(, '../templates/app/consultar_atencion_urgencia.html', {'form': form})  

#################################SOLICITUD ENFERMEDAD###################################
def ingresarSolicitudEnfermedad(request):
    try:
            current_user = request.user
            current_username = str(current_user.username)
            medico = Medico.objects.get(user__username__exact=current_username)
    except:
            messages.info(request, 'No puedes realizar esta acción sin estar autenticado')
            return redirect('home')

    if request.method == 'POST':
        form = RegistratioFormSolicitudEnfermedad(request.POST)
        if form.is_valid():
            
            id_who=form.cleaned_data['id_who']
            observacion=form.cleaned_data['observacion']
            

            new_solicitud = SolicitudEnfermedad(rut_medico=medico,id_who=id_who,observacion=observacion,estado='Pendiente')
            new_solicitud.save()
            return redirect('home')
    else:
        form = RegistratioFormSolicitudEnfermedad()
    return render(request, '../templates/app/ingresar_solicitud_enfermedad.html', {'form': form}) 


####################################TICKETS#############################################

def ingresarTicketAsistencia(request):
   
    try:
            current_user = request.user
            current_username = str(current_user.username)
            medico = Medico.objects.get(user__username__exact=current_username)
    except:
            mensaje= 'No puedes realizar esta accion sin estar autenticado'
            return redirect('home')
     
    if request.method == 'POST':
        
        form = form =RegistrationFormTicket(request.POST)
        if form.is_valid():
            descripcion=form.cleaned_data['descripcion']
            fecha_hoy=datetime.today()
         
            new_ticket = Ticket(rut_medico=medico,descripcion=descripcion,fecha_emitido=fecha_hoy)
            new_ticket.save()
            return redirect('home')
    else:
        form =RegistrationFormTicket()
    
    return render(request, '../templates/app/ingresar_ticket_asistencia.html', {'form': form})

def responderTicket(request,numero_ticket):
    pass



############################ADMNISTRADOR##########################################

def registrarAdministrador(request):
    if request.method == 'POST':
        form =RegistrationFormAdministrador(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            passw1 = form.cleaned_data['password1']
            passw2 = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            
            #crear usuario con contrasenha 
            new_user = User.objects.create_user(username=user,
                                 email=email,
                                 password=passw1)
            new_user.save()
            rut_admin = form.cleaned_data['rut_admin']
            nombres = form.cleaned_data['nombres']
            apellido_paterno = form.cleaned_data['apellido_paterno']
            apellido_materno = form.cleaned_data['apellido_materno']
            email = form.cleaned_data['email']
           
                
            new_admin = Administrador(rut_admin=rut_admin,nombres=nombres,apellido_paterno=apellido_paterno,
                                    apellido_materno=apellido_materno,email=email)
            user_tran = User.objects.get(username=user)
            new_admin.user = user_tran
            g = Group.objects.get(name='Administrador') 
            g.user_set.add(user_tran)
            new_admin.save()
            
            username = user
            raw_password = passw1
            user = authenticate(username=user, password=passw1)
            login(request, user)
                
            return redirect('home')
     
    else:
        form =RegistrationFormAdministrador()
    
    
    return render(request, '../templates/app/registrar_administrador.html', {'form': form})

def modificarAdministrador(request):
    try:
        current_user = request.user
        current_username = str(current_user.username)
        admin = Administrador.objects.get(user__username__exact=current_username)
    except:
        messages.warning(request, 'No puedes realizar esta acción sin estar autenticado', extra_tags='alert')
        return redirect('home')

    data = {'nombres': admin.nombres,
            'apellido_paterno': admin.apellido_paterno,
            'apellido_materno': admin.apellido_materno,
            'email' : admin.email
            }
    form = UpdateFormAdministrador(data,username =current_username)
    
    if request.method == 'POST':    #terminar la actualizacion con el commit
        form = UpdateFormAdministrador(request.POST,username =current_username)
        if form.is_valid():
            nombres = form.cleaned_data['nombres']
            apellido_paterno = form.cleaned_data['apellido_paterno']
            apellido_materno = form.cleaned_data['apellido_materno']
            email=form.cleaned_data['email']

            
            Administrador.objects.filter(user__username__exact=current_username).update(nombres=nombres)
            Administrador.objects.filter(user__username__exact=current_username).update(apellido_paterno=apellido_paterno)
            Administrador.objects.filter(user__username__exact=current_username).update(apellido_materno=apellido_materno)
            Administrador.objects.filter(user__username__exact=current_username).update(email=email)
            User.objects.filter(username = current_username).update(email=email)
            return redirect('home')
            
    return render(request,'../templates/app/actualizar_administrador.html', {'form':form})   

def eliminarAdministrador(request):
    try:
        current_user = request.user
        current_username = str(current_user.username)
  
    except:
        messages.info(request, 'No puedes realizar esta acción sin estar autenticado')
        return redirect('home')
    if request.method == 'POST':
        logout(request)
        current_user.is_active = False
        current_user.save()
        return redirect('home')

    return render(request,'../templates/app/eliminar_cuenta.html') 

def revisarSolicitud(request):
    try:
            current_user = request.user
            current_username = str(current_user.username)
            admin = Administrador.objects.get(user__username__exact=current_username)
    except:
            return redirect('home')
    solicitudes =SolicitudEnfermedad.objects.filter(estado = 'Pendiente')
    return render(request, '../templates/app/revisar_solicitud.html', {'solicitudes': solicitudes})

def revisarTicket(request):
    try:
            current_user = request.user
            current_username = str(current_user.username)
            admin = Administrador.objects.get(user__username__exact=current_username)
    except:
            messages.info(request, 'No puedes realizar esta acción sin estar autenticado')
            return redirect('home')
    tickets = Ticket.objects.filter(rut_admin='')
    
    return render(request, '../templates/app/revisar_ticket.html', {'tickets': tickets})


def paginaTicket(request,numero_ticket):

    
    if request.user.groups.filter(name='Administrador').exists():
        ticket = Ticket.objects.get(id=numero_ticket)
        try:
            current_user = request.user
            current_username = str(current_user.username)
            admin = Administrador.objects.get(user__username__exact=current_username)
        except:
            return redirect('home')
        if request.method == 'POST':
            form = ResponderTicket(request.POST)
            if form.is_valid():
                respuesta = form.cleaned_data['respuesta']
                     #update con la respuesta
                Ticket.objects.filter(id=numero_ticket).update(respuesta=respuesta)
                Ticket.objects.filter(id=numero_ticket).update(rut_admin=admin.rut_admin)
                return redirect('home')               

        else:
            form= ResponderTicket()
            return render(request, '../templates/app/pagina_ticket.html', {'ticket':ticket,'form':form})
    elif request.user.groups.filter(name='Medico').exists():
            ticket = Ticket.objects.get(id=numero_ticket)
            return render(request, '../templates/app/pagina_ticket.html', {'ticket':ticket,})
    else:
        return redirect('home')
    
    
    
    

def paginaSolicitud(request,numero_solicitud):
    if request.user.groups.filter(name='Administrador').exists():
        solicitud = SolicitudEnfermedad.objects.get(id=numero_solicitud)
        try:
            current_user = request.user
            current_username = str(current_user.username)
            admin = Administrador.objects.get(user__username__exact=current_username)
        except:
            return redirect('home')
        if request.method == 'POST':

            form = ResponderSolicitud(request.POST)
            if form.is_valid():
                estado = form.cleaned_data['estado']
                
                if int(estado)==1:
                    
                    ubicacion_directorio=os.path.dirname(__file__)
                    ubicacion_archivo='enfermedadesWHO.csv'
                    ubicacion_completa = os.path.join(ubicacion_directorio, ubicacion_archivo)
                    
                    with open(ubicacion_completa, 'rt') as csvfile:
                        my_content = csv.reader(csvfile, delimiter=',')
                        for row in my_content:
                            if row[0]==solicitud.id_who:
                                new_enfermedad = Enfermedad(id_who=row[0],nombre=row[1],clasificacion=row[2],riesgo=row[3])
                                new_enfermedad.save()
                                break
                    SolicitudEnfermedad.objects.filter(id=numero_solicitud).update(estado='Aprobado')
                    SolicitudEnfermedad.objects.filter(id=numero_solicitud).update(rut_admin=admin.rut_admin)
                elif int(estado)==2:
                    SolicitudEnfermedad.objects.filter(id=numero_solicitud).update(estado='Rechazado')
                    
                return redirect('home')               

        else:
            form= ResponderSolicitud()
            return render(request, '../templates/app/pagina_solicitud.html', {'solicitud':solicitud,'form':form})
    elif request.user.groups.filter(name='Medico').exists():
            solicitud = SolicitudEnfermedad.objects.get(id=numero_solicitud)
            return render(request, '../templates/app/pagina_solicitud.html', {'solicitud':solicitud,})
    else:
        return redirect('home')
    
    
    
    
    

def generarEstadisticas(request):
    regiones = {1: 'I',2: 'II',3: 'III',4: 'IV',5: 'V',6: 'VI',7: 'VII',8: 'VIII',9: 'IX',10: 'X',11: 'XI',12: 'XII',13: 'RM',14: 'XIV',15: 'XV'}
    if request.method == 'POST':
            form = GenerateStatisticsForm(request.POST)
            if form.is_valid():
                region=form.cleaned_data['region']
                id_who=form.cleaned_data['enfermedad']
                
                enfermedad = Enfermedad.objects.get(id_who=id_who)

                regionr=regiones[int(region)]
                
                cantidad_atenciones_ambulatorias= AtencionPacienteAmbulatorio.objects.filter(id_who=id_who).filter(codigo_establecimiento__region=99).count()
                cantidad_atenciones_urgencias = AtencionPacienteUrgencia.objects.filter(id_who=id_who).filter(codigo_establecimiento__region=int(region)).count()
                
                promedio = (cantidad_atenciones_urgencias)/15

                promedio=round(promedio, 2)

                
            return render(request, '../templates/app/resultado_estadistica.html', 
                          {'cantidad_atenciones_ambulatorias': cantidad_atenciones_ambulatorias ,
                           'cantidad_atenciones_urgencias': cantidad_atenciones_urgencias,
                           'promedio': promedio,
                           'enfermedad':enfermedad,
                           'regionr':regionr})
    else:
        form = GenerateStatisticsForm()
        return render(request, '../templates/app/generar_estadisticas.html', {'form': form})


def recuperarCuenta(request):
    if request.method == 'POST':
        form=RecuperarCuentaForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            user.is_active = True
            user.save()
            return render(request, '../templates/app/recuperar_cuenta_listo.html', {})
    form=RecuperarCuentaForm()
    return render(request, '../templates/app/recuperar_cuenta.html', {'form': form})