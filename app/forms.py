"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from app.models import *
from django.core.validators import RegexValidator
import csv
from itertools import cycle
import os
from datetime import datetime,date
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.admin import widgets 
from django.db.models import Q
rutregex = RegexValidator(r'^0*(\d{1,3}(\.?\d{3})*)\-?([\dkK])$', 'Solo rut con o sin puntos y guion ')
celularregex = RegexValidator(r'^\+?56(\s?)(0?9)(\s?)[98765]\d{7}$', 'Solo celulares en chile ')
passwordregex = RegexValidator(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,30}$', 'Minimo ocho caracteres, Maximo 30, debe contener por lo menos una letra mayuscula, una minuscula y un numero')
nombreregex = RegexValidator(r'^(?=.*[a-z])[A-Za-zñÑáéíóúÁÉÍÓÚ\s]{2,30}$','Maximo treinta caracteres, no se admiten numeros')
apellidosregex = RegexValidator(r'^(?=.*[a-z])[A-Za-zñÑáéíóúÁÉÍÓÚ\s]{2,15}$','Maximo quince caracteres, no se admiten numeros')
direccionregex = RegexValidator(r'^[A-Za-zñÑáéíóúÁÉÍÓÚ\s,#0-9]{,30}$','maximo 30 caracteres')
usuarioregex = RegexValidator(r'^[A-Za-z0-9ñ_.-]{5,15}$','Minimo 5 caracteres, maximo 15')
pesoregex = RegexValidator(r'^\d{1,3}(.\d{1,2})?','peso en kilos, max 2 decimales y el separador es un punto ')
estaturaregex = RegexValidator(r'^\d{1,3}(.\d{1,2})?','estatura en centimetros, max 2 decimales y el separador es un punto ')
fechahoraregex = RegexValidator('^\d{1,2}\/\d{1,2}\/\d{4}\ \d{2}\:\d{2}','dd/mm/aaaa HH:MM')
fecharegex = RegexValidator('^\d{1,2}\/\d{1,2}\/\d{4}','dd/mm/aaaa') 





class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=15,label=_("Usuario"),
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Ej: usuario192'}))
    password = forms.CharField(label=_("Contraseña"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Ej: **********'}))

#################################FORMULARIOS MEDICO#################################################
class RegistrationFormMedico(forms.Form):
    rut_medico = forms.CharField(max_length=10, required=True,label="Rut del Médico:",widget=forms.TextInput(attrs={'placeholder': 'Ej: 18658620-4','class': 'form-control'}),validators=[rutregex])
    nombres = forms.CharField(max_length=30, required=True,label="Nombres:",widget=forms.TextInput(attrs={'placeholder': 'Ej: Pablo Javier','class': 'form-control'}),validators=[nombreregex])
    apellido_paterno = forms.CharField(max_length=30, required=True,label="Apellido Paterno:",widget=forms.TextInput(attrs={'placeholder': 'Ej: Hernández','class': 'form-control'}),validators=[apellidosregex])
    apellido_materno =  forms.CharField(max_length=30, required=True,label="Apellido Materno:",widget=forms.TextInput(attrs={'placeholder': 'Ej: Fuentes','class': 'form-control'}),validators=[apellidosregex])
    email = forms.EmailField(max_length=30,label="Email:",widget=forms.TextInput(attrs={'placeholder': 'Ej: pjhfxx@gmail.com','class': 'form-control'}),)
    fono = forms.CharField(max_length=12,label="Celular:", required=True,widget=forms.TextInput(attrs={'placeholder': 'Ej: +56989079205','class': 'form-control'}),validators=[celularregex])
    direccion =forms.CharField(max_length=30,label="Dirección:", required=True,widget=forms.TextInput(attrs={'placeholder': 'Ej: Av. SiempreViva #123, Santiago','class': 'form-control'}),validators=[direccionregex])
    especialidad = forms.CharField(max_length=30,label="Especialidad:", required=True,widget=forms.TextInput(attrs={'placeholder': 'Ej: General','class': 'form-control'}),validators=[nombreregex])
    user = forms.CharField(max_length=15,label="Usuario:", required=True,widget=forms.TextInput(attrs={'placeholder': 'Ej: usuario123','class': 'form-control'}),validators=[usuarioregex])
    password1 =  forms.CharField(label=_("Contraseña"),widget=forms.PasswordInput({'class': 'form-control','placeholder':'','class': 'form-control'}), validators=[passwordregex])
    password2 = forms.CharField(label=_("Confirmar Contraseña"),widget=forms.PasswordInput({'class': 'form-control','placeholder':'','class': 'form-control'}), validators=[passwordregex])

    def clean_rut_medico(self):
        #Verificar que el rut sea valido
        rut_form=str(self.cleaned_data['rut_medico'])
        rut_limpio = rut_form.replace(".","")
        #nuevo
        rut_limpio = rut_form.replace(".","")
        
        digito_verificador = rut_limpio[-1:]

        if digito_verificador=="k" or digito_verificador=="K":
            digito_verificador = 10
        rut_limpio = rut_limpio[:-2]
        reversed_digits = map(int, reversed(rut_limpio))
        factors = cycle(range(2, 8))
        suma = sum(d * f for d, f in zip(reversed_digits, factors))
        digito_resultado= 11 -(suma%11)
        if digito_resultado==11:
            digito_resultado=0
        ###endnuevo
        

        if int(digito_verificador)!=digito_resultado:
            raise  forms.ValidationError(_("El rut no es valido"), code='invalid')
        
        #si existe dentro del Colegio Medico
        ubicacion_directorio=os.path.dirname(__file__)
        ubicacion_archivo='medicos.csv'
        ubicacion_completa = os.path.join(ubicacion_directorio, ubicacion_archivo)
        is_in_file = False
        with open(ubicacion_completa, 'rt') as csvfile:
            my_content = csv.reader(csvfile, delimiter=',')
            for row in my_content:
                if rut_form.replace(".","") in row:
                    is_in_file = True
        if not is_in_file:
            raise forms.ValidationError(_('No existe en Colegio Medico'), code='invalid')
        


        #Validar que el rut no exista previamente en el sistema
        if Medico.objects.filter(rut_medico=rut_form).exists():
            raise forms.ValidationError(_('Ya existe una cuenta asociada con este Rut'), code='invalid')

        return rut_form

    #Verificar si existe el nombre de usuario
    def clean_user(self):
        user_form=self.cleaned_data['user']
        if User.objects.filter(username=user_form).exists():
            raise forms.ValidationError(_('Este nombre de usuario ya existe'), code='invalid')

        return user_form
    def clean_email(self):
        email=self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('Este email ya existe en el sistema'), code='invalid')
        return email
    #verificar que las contrasenhas son identicas
    def clean(self):
        cleaned_data = super(RegistrationFormMedico,self).clean()
        password1= cleaned_data.get("password1")
        password2= cleaned_data.get("password2")
        email=cleaned_data.get("email")
        rut_medico=cleaned_data.get("rut_medico")


        ubicacion_directorio=os.path.dirname(__file__)
        ubicacion_archivo='medicos.csv'
        ubicacion_completa = os.path.join(ubicacion_directorio, ubicacion_archivo)
        is_in_file = False
        with open(ubicacion_completa, 'rt') as csvfile:
            my_content = csv.reader(csvfile, delimiter=',')
            for row in my_content:
                if row[0]==rut_medico and row[1]==email :
                    is_in_file = True
        if not is_in_file:
            msg= "Este rut no esta asociado a esta cuenta de correo en el Colegio Médico"
            self.add_error('email',msg)

        if password1 != password2:
           msg="Sus contraseñas no coinciden"
           self.add_error('password1',msg)
    
    



class UpdateFormMedico(forms.Form):   
    
    nombres=forms.CharField(max_length=30, required=True,label="Nombres:",widget=forms.TextInput(attrs={'placeholder': 'Ej: Carlos Antonio','class': 'form-control'}), validators=[nombreregex])
    apellido_paterno=forms.CharField(max_length=30, required=True,label="Apellido Paterno:",widget=forms.TextInput(attrs={'placeholder': 'Ej: Rojas','class': 'form-control'}), validators=[apellidosregex])
    apellido_materno=forms.CharField(max_length=30, required=True,label="Apellido Materno:", widget=forms.TextInput(attrs={'placeholder': 'Ej: Gonzalez','class': 'form-control'}), validators=[apellidosregex])
    email = forms.EmailField(max_length=30,label="Email:", widget=forms.TextInput(attrs={'placeholder': 'Ej: correo@ejemplo.com','class': 'form-control'}),)
    fono = forms.CharField(max_length=12, required=True,label="Celular:",widget=forms.TextInput(attrs={'placeholder': 'Ej: +56989079205','class': 'form-control'}),validators=[celularregex])
    direccion =forms.CharField(max_length=30, required=True,label="Dirección:",widget=forms.TextInput(attrs={'placeholder': 'Ej: Tomas Moro #213 , Santiago','class': 'form-control'}), validators=[direccionregex])
    especialidad = forms.CharField(max_length=30, required=True,label="Especialidad:",widget=forms.TextInput(attrs={'placeholder': 'Ej: Nefrólogo','class': 'form-control'}), validators=[nombreregex])
    
    def __init__(self,*args,**kwargs):
        self.username = kwargs.pop('username')
        super(UpdateFormMedico,self).__init__(*args,**kwargs)

    def clean_email(self):
        email=self.cleaned_data['email']

        user = User.objects.get(username=self.username)

        if str(user.email) == email:
            pass
        elif str(user.email) != email: 
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError(_('Este email ya esta asociado a una cuenta de usuario'), code='invalid')
        return email
class ListFormMedico(forms.Form):
    filtros = (
            (1, _("Rut")),
            (2, _("Nombre")),
            (3, _("Apellido Paterno")),
            (4, _("Especialidad")),
            
        )
    busqueda=forms.CharField(label='Ingrese lo que quiere buscar:', required=True,help_text='Requerido',widget=forms.TextInput(attrs={'placeholder': '','class': 'form-control'}))
    filtro = forms.ChoiceField(choices = filtros, label="Filtrar por:", initial='1', widget=forms.Select(attrs={'class': 'form-control'}), required=True,help_text='Seleccione uno por favor')

    
        
                
                
#########################################FORMULARIOS PACIENTES########################################################   
class RegistrationFormPaciente(forms.Form):
    sexo_choice = (
            ('M', _("Hombre")),
            ('F', _("Mujer")),
            ('O', _("Otros")),
        )
   
    rut_paciente = forms.CharField(max_length=10, required=True,label='Rut Paciente:',widget=forms.TextInput(attrs={'placeholder': 'Ej:18658620-4','class': 'form-control'}) ,validators=[rutregex])
    nombres = forms.CharField(max_length=30, required=True, label='Nombres:',widget=forms.TextInput(attrs={'placeholder': 'Ej: Juan','class': 'form-control'}),validators=[nombreregex])
    apellido_paterno = forms.CharField(max_length=30, required=True,label='Apellido Paterno:',widget=forms.TextInput(attrs={'placeholder': 'Ej: Pardo','class': 'form-control'}), validators=[apellidosregex] )
    apellido_materno =  forms.CharField(max_length=30, required=True,label='Apellido Materno:',widget=forms.TextInput(attrs={'placeholder': 'Ej: Rodríguez','class': 'form-control'}),validators=[apellidosregex])
    sexo = forms.ChoiceField(choices = sexo_choice, label="Sexo ", initial='1', widget=forms.Select(attrs={'class': 'form-control'}), required=True,help_text='Seleccione uno por favor')
    fecha_nacimiento = forms.DateField(required=True,label='Fecha de Nacimiento:',widget=forms.TextInput(attrs={'placeholder': 'Ej: 20/12/1993','class': 'form-control'}), input_formats=['%d/%m/%Y'])
    email = forms.EmailField(max_length=30,label='Email:', widget=forms.TextInput(attrs={'placeholder': 'Ej: correo@gmail.com','class': 'form-control'}))
    fono = forms.CharField(max_length=12, required=True,label='Celular:', widget=forms.TextInput(attrs={'placeholder': 'Ej:+56989079205','class': 'form-control'}),validators=[celularregex])
    fono_emergencia = forms.CharField(max_length=12,label='Celular de Emergencia:', required=True, widget=forms.TextInput(attrs={'placeholder': 'Ej:18658620-4','class': 'form-control'}),validators=[celularregex])
    direccion =forms.CharField(max_length=30,label='Dirección:', required=True,widget=forms.TextInput(attrs={'placeholder': 'Ej: Dirección #123','class': 'form-control'}),validators=[direccionregex])
    peso =forms.DecimalField( required=True,label='Peso:', help_text='En kilogramos',widget=forms.TextInput(attrs={'placeholder': 'Ej: 90.4','class': 'form-control'}),max_value=300.0, min_value=35.0,max_digits=3,decimal_places=1,validators=[pesoregex] )
    estatura =forms.DecimalField( required=True,label='Estatura:', help_text='En metros',max_value=3.0, min_value=1.0,max_digits=3, decimal_places=2,widget=forms.TextInput(attrs={'placeholder': 'Ej: 1.81','class': 'form-control'}) ,validators=[estaturaregex])

    def clean_rut_paciente(self):
        rut_form=str(self.cleaned_data['rut_paciente'])
        
        
        rut_limpio = rut_form.replace(".","")
        
        digito_verificador = rut_limpio[-1:]

        if digito_verificador=="k" or digito_verificador=="K":
            digito_verificador = 10
        rut_limpio = rut_limpio[:-2]
        reversed_digits = map(int, reversed(rut_limpio))
        factors = cycle(range(2, 8))
        suma = sum(d * f for d, f in zip(reversed_digits, factors))
        digito_resultado= 11 -(suma%11)
        if digito_resultado==11:
            digito_resultado=0
        
        if int(digito_verificador)!=digito_resultado:
            raise  forms.ValidationError(_("El rut no es valido"), code='invalid')

        #Validar que el paciente no exista ya en el sistema
        if Paciente.objects.filter(rut_paciente=rut_form).exists():
            raise  forms.ValidationError(_("El paciente ya existe en el sistema"), code='invalid')
        

        return rut_form

    def clean_fecha_nacimiento(self):
        fecha_nacimiento=self.cleaned_data['fecha_nacimiento']
        fecha_hoy=date.today()

        if fecha_nacimiento > fecha_hoy:
            raise  forms.ValidationError(_("La fecha de nacimiento no puede ser mayor a la fecha actual"), code='invalid')

        return fecha_nacimiento

    

class UpdateFormPaciente(forms.Form):
    sexo_choice = (
            ('M', _("Hombre")),
            ('F', _("Mujer")),
            ('O', _("Otros")),
        )
    
    nombres = forms.CharField(max_length=30, required=True,label='Nombres:',widget=forms.TextInput(attrs={'placeholder': 'Ej: Ninoska Javiera','class': 'form-control'}), validators=[nombreregex])
    apellido_paterno = forms.CharField(max_length=30, required=True,label='Apellido Paterno:',widget=forms.TextInput(attrs={'placeholder': 'Ej: Bardo','class': 'form-control'}),validators=[apellidosregex])
    apellido_materno =  forms.CharField(max_length=30, required=True,label='Apellido Materno:',widget=forms.TextInput(attrs={'placeholder': 'Ej: Millar','class': 'form-control'}),validators=[apellidosregex])
    sexo = forms.ChoiceField(choices = sexo_choice, label="Sexo:", initial='1', widget=forms.Select(attrs={'class': 'form-control'}), required=True,help_text='Seleccione uno por favor')
    fecha_nacimiento = forms.DateField(required=True,label='Fecha de Nacimiento:',widget=forms.TextInput(attrs={'placeholder': 'Ej: 12/04/1997','class': 'form-control'}),input_formats=['%d/%m/%Y'])
    email = forms.EmailField(max_length=30,label='Email:',widget=forms.TextInput(attrs={'placeholder': 'Ej: pjhfxx@gmail.com','class': 'form-control'}))
    fono = forms.CharField(max_length=12,label='Celular:', required=True, widget=forms.TextInput(attrs={'placeholder': 'Ej: +56989079205','class': 'form-control'}),validators=[celularregex])
    fono_emergencia = forms.CharField(max_length=12,label='Celular de Emergencia:', required=True, widget=forms.TextInput(attrs={'placeholder': 'Ej: +56989079205','class': 'form-control'}),validators=[celularregex])
    direccion =forms.CharField(max_length=30, required=True,label='Dirección:', widget=forms.TextInput(attrs={'placeholder': 'Ej: Dirección #231','class': 'form-control'}),validators=[direccionregex])
    peso =forms.DecimalField( required=True, help_text='En kilogramos',widget=forms.TextInput(attrs={'placeholder': 'Ej: 90.3','class': 'form-control'}),max_value=300.0, min_value=35.0,max_digits=3,decimal_places=1)
    estatura =forms.DecimalField( required=True, help_text='En metros',widget=forms.TextInput(attrs={'placeholder': 'Ej: 1.81','class': 'form-control'}),max_value=3.0, min_value=1.0,max_digits=3, decimal_places=2)

    def __init__(self,*args,**kwargs):
        self.rut_paciente = kwargs.pop('rut_paciente')
        super(UpdateFormPaciente,self).__init__(*args,**kwargs)

    def clean_fecha_nacimiento(self):
        #validar que la fecha no sea mayor a la actual
        fecha_nacimiento= self.cleaned_data['fecha_nacimiento']
        fecha_hoy= date.today()

        if fecha_nacimiento > fecha_hoy:
            raise  forms.ValidationError(_("La fecha de nacimiento NO puede ser mayor a la fecha actual"), code='invalid')
        return fecha_nacimiento

    def clean_email(self):
        email=self.cleaned_data['email']
        paciente = Paciente.objects.get(rut_paciente=self.rut_paciente)

        if str(paciente.email) == email:
            pass
        elif str(paciente.email) != email: 
            if Paciente.objects.filter(email=email).exists():
                raise forms.ValidationError(_('Este email ya esta asociado a un paciente'), code='invalid')
        return email

class ListFormPaciente(forms.Form):
    rut_paciente = forms.CharField(max_length=10, required=True,label='Rut del Paciente:',widget=forms.TextInput(attrs={'placeholder': 'Ej: 18658620-4','class': 'form-control'}),validators=[rutregex])

    #Verificar que el rut sea valido

    def clean_rut_paciente(self):
        rut_form=str(self.cleaned_data['rut_paciente'])
        
        rut_limpio = rut_form.replace(".","")
        
        digito_verificador = rut_limpio[-1:]

        if digito_verificador=="k" or digito_verificador=="K":
            digito_verificador = 10
        rut_limpio = rut_limpio[:-2]
        reversed_digits = map(int, reversed(rut_limpio))
        factors = cycle(range(2, 8))
        suma = sum(d * f for d, f in zip(reversed_digits, factors))
        digito_resultado= 11 -(suma%11)
        if digito_resultado==11:
            digito_resultado=0

        if int(digito_verificador)!=digito_resultado:
            raise  forms.ValidationError(_("El rut no es valido"), code='invalid')

        #validar que exista en el sistema
     
        if not Paciente.objects.filter(rut_paciente=rut_form).exists():
            raise  forms.ValidationError(_("El paciente NO existe en el sistema"), code='invalid')
        return rut_form
####################################################FORMULARIOS ESTABLECIMIENTOS####################################################

class RegistrationFormEstablecimiento(forms.Form):
    codigo_establecimiento = forms.CharField(max_length=6, required=True,label=_("Codigo de Establecimiento"),widget=forms.TextInput({'class': 'form-control','placeholder':'Ej: 01-012'}))
    codigo_verificacion = forms.CharField(max_length=6, required=True, label=_("Codigo de Verificacion"),widget=forms.TextInput({'class': 'form-control','placeholder':'Ej: 789546'}))
    email = forms.EmailField(max_length=30,label=_("Email:"),widget=forms.TextInput({'class': 'form-control','placeholder':'Ej: email@example.com'}))
    user = forms.CharField(max_length=15, required=True,label=_("Usuario:"),widget=forms.TextInput({'class': 'form-control','placeholder':'Ej: usuario123'}),validators=[usuarioregex])
    password1 =  forms.CharField(label=_("Contraseña:"),widget=forms.PasswordInput({'class': 'form-control','placeholder':''}), validators=[passwordregex])
    password2 = forms.CharField(label=_("Confirmar Contraseña:"),widget=forms.PasswordInput({'class': 'form-control','placeholder':''}), validators=[passwordregex])
    

    #Verificar si existe el nombre de usuario
    def clean_user(self):
        user_form=self.cleaned_data['user']
        if User.objects.filter(username=user_form).exists():
            raise forms.ValidationError(_('Este nombre de usuario ya existe'), code='invalid')

        return user_form

    def clean_email(self):
        email=self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('Este email ya existe en el sistema'), code='invalid')
        return email
    #verificar que las contrasenhas son identicas
    def clean(self):
        cleaned_data = super(RegistrationFormEstablecimiento,self).clean()
        password1= cleaned_data.get("password1")
        password2= cleaned_data.get("password2")
        
        if password1 != password2:
           msg="Sus contraseñas no coinciden"
           self.add_error('password1',msg)
        #verificar que la combinacion codigo establecimiento y codigo verificacion sea correcta

        codigo_establecimiento= cleaned_data.get("codigo_establecimiento")
        codigo_verificacion = cleaned_data.get("codigo_verificacion")

        ubicacion_directorio=os.path.dirname(__file__)
        ubicacion_archivo='codigo.csv'
        ubicacion_completa = os.path.join(ubicacion_directorio, ubicacion_archivo)
        is_in_file = False
        with open(ubicacion_completa, 'rt') as csvfile:
            my_content = csv.reader(csvfile, delimiter=',')
            for row in my_content:
                if row[0]==codigo_establecimiento and row[1]==codigo_verificacion:
                    is_in_file = True
        if not is_in_file:
            msg="Esta combinacion de codigos es incorrecta"
            self.add_error('codigo_verificacion',msg)

    #verificar que el codigo de establecimiento sea correcto
    def clean_codigo_establecimiento (self):
        codigo_establecimiento=self.cleaned_data['codigo_establecimiento']
        ubicacion_directorio=os.path.dirname(__file__)
        ubicacion_archivo='Establecimientos.csv'
        ubicacion_completa = os.path.join(ubicacion_directorio, ubicacion_archivo)
        is_in_file = False
        with open(ubicacion_completa, 'rt') as csvfile:
            my_content = csv.reader(csvfile, delimiter=',')
            for row in my_content:
                if codigo_establecimiento in row:
                    is_in_file = True
        if not is_in_file:
            raise forms.ValidationError(_('No existe en el registro de Establecimientos'), code='invalid')

        return codigo_establecimiento

    def clean_codigo_verificacion(self):
        codigo_verificacion=self.cleaned_data['codigo_verificacion']

        ubicacion_directorio=os.path.dirname(__file__)
        ubicacion_archivo='codigo.csv'
        ubicacion_completa = os.path.join(ubicacion_directorio, ubicacion_archivo)
        is_in_file = False
        with open(ubicacion_completa, 'rt') as csvfile:
            my_content = csv.reader(csvfile, delimiter=',')
            for row in my_content:
                
                if int(row[1])==int(codigo_verificacion):
                    is_in_file = True
                    break
        
        if not is_in_file:
            raise forms.ValidationError(_('El codigo de verificación es incorrecto'), code='invalid')
        return codigo_verificacion

class UpdateFormEstablecimiento(forms.Form):   
    email = forms.EmailField(max_length=30,label=_("Email:"),widget=forms.TextInput({'class': 'form-control','placeholder':'Ej: mail@example.com'}))
    
    def __init__(self,*args,**kwargs):
        self.username = kwargs.pop('username')
        super(UpdateFormEstablecimiento,self).__init__(*args,**kwargs)

    def clean_email(self):
        email=self.cleaned_data['email']
        user = User.objects.get(username=self.username)

        if str(user.email) == email:
            pass
        elif str(user.email) != email: 
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError(_('Este email ya esta asociado a una cuenta de usuario'), code='invalid')
        return email
    

class ListFormEstablecimiento(forms.Form):
    filtros = (
            (1, _("Código MINSAL")),
            (2, _("Nombre")),
            (3, _("Región")),
            (4, _("Comuna")),
        )
    busqueda=forms.CharField(label='Ingrese lo que quiere buscar', required=True,widget=forms.TextInput(attrs={'placeholder': '','class': 'form-control'}),help_text='Requerido')
    filtro = forms.ChoiceField(choices = filtros, label="Filtrar por:", initial='1',required=True,widget=forms.Select(attrs={'class': 'form-control'}),help_text='Seleccione uno por favor')



####################################################FORMULARIOS ATENCIONES##########################################################
class RegistrationFormAtencionAmbulatoria (forms.Form):
    
    fecha_atencion_hora = forms.DateTimeField(required=True,label='Fecha y Hora de la atención:',widget=forms.TextInput(attrs={'placeholder': 'Ej: 01/09/2017 09:25','class': 'form-control'}),input_formats=['%d/%m/%Y %H:%M'])
    tratamiento = forms.CharField(max_length=800,required=True,label='Tratamiento:',widget=forms.Textarea(attrs={'placeholder': '','class': 'form-control'}))
    observacion_medica= forms.CharField(max_length=800,required=True,label='Observación Médica:',widget=forms.Textarea(attrs={'placeholder': '','class': 'form-control'}))
    observacion_publica= forms.CharField(max_length=800,required=True,label='Observación Pública:',widget=forms.Textarea(attrs={'placeholder': '','class': 'form-control'}))
    id_who = forms.ChoiceField(required=True,label='Enfermedad :',choices=[(enfermedad.id_who, enfermedad.nombre) for enfermedad in Enfermedad.objects.all()],widget=forms.Select(attrs={'class': 'form-control'}))
    codigo_establecimiento=forms.ChoiceField(required=True,label='Establecimiento :', choices=[(establecimiento.codigo_establecimiento, establecimiento.nombre) for establecimiento in Establecimiento.objects.all()],widget=forms.Select(attrs={'class': 'form-control'}))
    
    def clean_fecha_atencion_hora(self):
        fecha_atencion_hora =self.cleaned_data['fecha_atencion_hora']
        fecha_hoy= datetime.today()
        fecha_hoy = fecha_hoy.replace(tzinfo=None)
        fecha_atencion_hora=fecha_atencion_hora.replace(tzinfo=None)
        if fecha_atencion_hora > fecha_hoy:
            raise  forms.ValidationError(_("La fecha/hora de la atención NO puede ser mayor a la fecha actual"), code='invalid')

        return fecha_atencion_hora

    def clean_rut_paciente(self):
        rut_form=self.cleaned_data['rut_paciente']
        rut_limpio = rut_form.replace(".","")
        
        #MODULO 11
        digito_verificador = rut_limpio[-1:]

        if digito_verificador=="k" or digito_verificador=="K":
            digito_verificador = 10

        rut_limpio = rut_limpio[:-2]

        reversed_digits = map(int, reversed(rut_limpio))
        factors = cycle(range(2, 8))
        suma = sum(d * f for d, f in zip(reversed_digits, factors))
        digito_resultado= 11 -(suma%11)
        
        if int(digito_verificador)!=digito_resultado:
            raise  forms.ValidationError(_("El rut no es valido"), code='invalid')

        #Verifica que el paciente EXISTA en el sistema
        if not Paciente.objects.filter(rut_paciente=rut_form).exists():
            raise forms.ValidationError(_('Este rut de paciente no existe en el sistema'), code='invalid')
        
        return rut_form

    def clean (self):
        cleaned_data = super(RegistrationFormAtencionAmbulatoria,self).clean()
        rut_paciente= cleaned_data.get("rut_paciente")
        fecha_atencion_hora= cleaned_data.get("fecha_atencion_hora")

        if AtencionPacienteAmbulatorio.objects.filter(Q(rut_paciente=rut_paciente) | Q(fecha_atencion_hora=fecha_atencion_hora)).exists():
            msg="Ya existe una atencion prestada al paciente en esta fecha/hora"
            self.add_error('fecha_atencion_hora',msg)
        
        
        

       


class RegistrationFormAtencionUrgencia (forms.Form):
    fecha_atencion_hora = forms.DateTimeField( required=True,label='Fecha y Hora de la atención :',widget=forms.TextInput(attrs={'placeholder': 'Ej: 02/05/2016 15:30','class': 'form-control'}) ,input_formats=['%d/%m/%Y %H:%M'], )
    rut_paciente = forms.CharField(max_length=10,label='Rut del Paciente :',widget=forms.TextInput(attrs={'placeholder': 'Ej: 9867014-9','class': 'form-control'}), required=True,validators=[rutregex])
    rut_encargado_urgencia = forms.CharField(max_length=10,label='Rut del encargado de la atención :',widget=forms.TextInput(attrs={'placeholder': 'Ej: 2219376-4','class': 'form-control'}), required=True,validators=[rutregex])
    nombre_encargado_urgencia=forms.CharField(max_length=30,label='Nombre del encargado de la atención :',widget=forms.TextInput(attrs={'placeholder': 'Ej: Yasna Fuentes','class': 'form-control'}), required=True,validators=[nombreregex])
    cargo_encargado_urgencia=forms.CharField(max_length=30,label='Cargo del encargado de la atención :',widget=forms.TextInput(attrs={'placeholder': 'Ej: Jefa de Urgencias','class': 'form-control'}), required=True, validators=[nombreregex])
    tratamiento = forms.CharField(max_length=800,label='Tratamiento :',required=True,widget=forms.Textarea(attrs={'placeholder': '','class': 'form-control'}))
    observacion_urgencia = forms.CharField(max_length=800,label='Observación de la atención de urgencia :',required=True,widget=forms.Textarea(attrs={'placeholder': '','class': 'form-control'}))
    #codigo_establecimiento=forms.ChoiceField(required=True, choices=[(establecimiento.codigo_establecimiento, establecimiento.nombre) for establecimiento in Establecimiento.objects.all()],label='Establecimiento')
    id_who = forms.ChoiceField(required=True,choices=[(enfermedad.id_who, enfermedad.nombre) for enfermedad in Enfermedad.objects.all()],widget=forms.Select(attrs={'class': 'form-control'}), label='Enfermedad')

    def clean_fecha_atencion_hora(self):
        fecha_atencion_hora =self.cleaned_data['fecha_atencion_hora']
        fecha_hoy= datetime.today()
        fecha_hoy = fecha_hoy.replace(tzinfo=None)
        fecha_atencion_hora=fecha_atencion_hora.replace(tzinfo=None)
        if (fecha_atencion_hora) > (fecha_hoy):
            raise  forms.ValidationError(_("La fecha/hora de la atención NO puede ser mayor a la fecha actual"), code='invalid')

        return fecha_atencion_hora

    def clean_rut_encargado_urgencia(self):
        rut_form=str(self.cleaned_data['rut_encargado_urgencia'])
        
        rut_limpio = rut_form.replace(".","")
        
        digito_verificador = rut_limpio[-1:]

        if digito_verificador=="k" or digito_verificador=="K":
            digito_verificador = 10
        rut_limpio = rut_limpio[:-2]
        reversed_digits = map(int, reversed(rut_limpio))
        factors = cycle(range(2, 8))
        suma = sum(d * f for d, f in zip(reversed_digits, factors))
        digito_resultado= 11 -(suma%11)
        if digito_resultado==11:
            digito_resultado=0
        
        if int(digito_verificador)!=digito_resultado:
            raise  forms.ValidationError(_("El rut no es valido"), code='invalid')
        return rut_form
        
    def clean_rut_paciente(self):
        rut_form=str(self.cleaned_data['rut_paciente'])
        
        rut_limpio = rut_form.replace(".","")
        
        digito_verificador = rut_limpio[-1:]

        if digito_verificador=="k" or digito_verificador=="K":
            digito_verificador = 10
        rut_limpio = rut_limpio[:-2]
        reversed_digits = map(int, reversed(rut_limpio))
        factors = cycle(range(2, 8))
        suma = sum(d * f for d, f in zip(reversed_digits, factors))
        digito_resultado= 11 -(suma%11)
        if digito_resultado==11:
            digito_resultado=0
        
        if int(digito_verificador)!=digito_resultado:
            raise  forms.ValidationError(_("El rut no es valido"), code='invalid')

        #Verifica que el paciente EXISTA en el sistema
        if not Paciente.objects.filter(rut_paciente=rut_form).exists():
            raise forms.ValidationError(_('Este rut de paciente no existe en el sistema'), code='invalid')
        
        return rut_form

    def clean (self):
        cleaned_data = super(RegistrationFormAtencionUrgencia,self).clean()
        rut_paciente= cleaned_data.get("rut_paciente")
        fecha_atencion_hora= cleaned_data.get("fecha_atencion_hora")

        if AtencionPacienteUrgencia.objects.filter(Q(rut_paciente=rut_paciente) & Q(fecha_atencion_hora=fecha_atencion_hora)):
            msg="Ya existe una atencion prestada al paciente en esta fecha/hora"
            self.add_error('fecha_atencion_hora',msg)
    

class RegistratioFormSolicitudEnfermedad (forms.Form):
    
    id_who=forms.CharField(max_length=7,required=True,widget=forms.TextInput(attrs={'placeholder': 'Ej: 1124545','class': 'form-control'}))
    observacion = forms.CharField(max_length=800,required=True,widget=forms.Textarea(attrs={'class': 'form-control'}))

    def clean_id_who (self):
        #que no exista previamente
        id_who=str(self.cleaned_data['id_who'])
        if Enfermedad.objects.filter(id_who=id_who).exists():
            raise forms.ValidationError(_('La enfermedad con este identificador WHO ya existe en el sistema'), code='invalid')
        #que si exista en la base de datos de WHO

        ubicacion_directorio=os.path.dirname(__file__)
        ubicacion_archivo='enfermedadesWHO.csv'
        ubicacion_completa = os.path.join(ubicacion_directorio, ubicacion_archivo)
        is_in_file = False
        with open(ubicacion_completa, 'rt') as csvfile:
            my_content = csv.reader(csvfile, delimiter=',')
            for row in my_content:
                
                if id_who in row:
                    is_in_file = True
                    break
        if not is_in_file :
            raise forms.ValidationError(_('La enfermedad con este identificador no está registrada en WHO'), code='invalid')
        return id_who

class RegistrationFormTicket (forms.Form):
    descripcion = forms.CharField(max_length=800,required=True,widget=forms.Textarea(attrs={'class': 'form-control'}))
    
###############################################FORMULARIOS ADMINISTRADOR###########################################
class RegistrationFormAdministrador (forms.Form):
    rut_admin=forms.CharField(max_length=10,label="Rut del Administrador:",widget=forms.TextInput(attrs={'placeholder': 'Ej: 12345678-0','class': 'form-control'}), required=True,validators=[rutregex])
    nombres=forms.CharField(max_length=30,label="Nombres:", required=True,widget=forms.TextInput(attrs={'placeholder': 'Ej: Johannn Alejandro','class': 'form-control'}),validators=[nombreregex])
    apellido_paterno=forms.CharField(max_length=30,label="Apellido Paterno:", required=True,widget=forms.TextInput(attrs={'placeholder': 'Ej: Roman','class': 'form-control'}),validators=[apellidosregex] )
    apellido_materno=forms.CharField(max_length=30,label="Apellido Materno:", required=True,widget=forms.TextInput(attrs={'placeholder': 'Ej: Santis','class': 'form-control'}),validators=[apellidosregex])
    email = forms.EmailField(max_length=30,label="Email:",widget=forms.TextInput(attrs={'placeholder': 'Ej: jroman@gmail.com','class': 'form-control'}))
    user = forms.CharField(max_length=15, required=True,label="Usuario:",widget=forms.TextInput(attrs={'placeholder': 'Ej: usuario123','class': 'form-control'}), validators=[usuarioregex])
    password1 =  forms.CharField(label=_("Contraseña"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':''}), validators=[passwordregex])
    password2 = forms.CharField(label=_("Confirmar Contraseña"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':''}), validators=[passwordregex])
     #email = forms.EmailField(max_length=30,label="Email:",widget=forms.TextInput(attrs={'placeholder': 'Ej: pjhfxx@gmail.com'}),)
    def clean_rut_admin(self):
        rut_form=str(self.cleaned_data['rut_admin'])
        
        rut_limpio = rut_form.replace(".","")
        rut_limpio2 = rut_limpio
        digito_verificador = rut_limpio[-1:]

        if digito_verificador=="k" or digito_verificador=="K":
            digito_verificador = 10
        rut_limpio = rut_limpio[:-2]
        reversed_digits = map(int, reversed(rut_limpio))
        factors = cycle(range(2, 8))
        suma = sum(d * f for d, f in zip(reversed_digits, factors))
        digito_resultado= 11 -(suma%11)
        if digito_resultado==11:
            digito_resultado=0
        
        if int(digito_verificador)!=digito_resultado:
            raise  forms.ValidationError(_("El rut no es valido"), code='invalid')
        if Administrador.objects.filter(rut_admin=rut_form).exists():
            raise forms.ValidationError(_('Ya existe una cuenta asociada con este Rut'), code='invalid')

        #VER QUE EL ADMIN ESTE EN LA NOMINA
        ubicacion_directorio=os.path.dirname(__file__)
        ubicacion_archivo='administradores.csv'
        ubicacion_completa = os.path.join(ubicacion_directorio, ubicacion_archivo)
        is_in_file = False
        with open(ubicacion_completa, 'rt') as csvfile:
            my_content = csv.reader(csvfile, delimiter=',')
            for row in my_content:
                
                if rut_limpio2 in row:
                    is_in_file = True
                    break
        if not is_in_file :
            raise forms.ValidationError(_('Este rut no se encuentra en la nomina de administradores'), code='invalid')

        return rut_form

    def clean_email(self):
        email=self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('Este email ya existe en el sistema'), code='invalid')
        return email

    def clean_user(self):
        user_form=self.cleaned_data['user']
        if User.objects.filter(username=user_form).exists():
            raise forms.ValidationError(_('Este nombre de usuario ya existe'), code='invalid')

        return user_form
    
    def clean(self):
        cleaned_data = super(RegistrationFormAdministrador,self).clean()
        password1= cleaned_data.get("password1")
        password2= cleaned_data.get("password2")
        rut=cleaned_data.get("rut_admin")
        email=cleaned_data.get("email")
        if password1 != password2:
           msg="Sus contraseñas no coinciden"
           self.add_error('password1',msg)
        #verificar que la combinacion rut mail sea correcta en la nomina
        ubicacion_directorio=os.path.dirname(__file__)
        ubicacion_archivo='administradores.csv'
        ubicacion_completa = os.path.join(ubicacion_directorio, ubicacion_archivo)
        is_in_file = False

        with open(ubicacion_completa, 'rt') as csvfile:
            my_content = csv.reader(csvfile, delimiter=',')
            for row in my_content:
                if row[0]==rut and row[1]==email:
                    is_in_file = True
                    break
        if not is_in_file:
            msg="La combinación Rut/Email es incorrecta "
            self.add_error('rut_admin',msg)

class UpdateFormAdministrador(forms.Form):
    nombres=forms.CharField(max_length=30, required=True,label="Nombres:",widget=forms.TextInput(attrs={'placeholder': 'Ej: Pedro Daniel','class': 'form-control'}), validators=[nombreregex])
    apellido_paterno=forms.CharField(max_length=30, required=True,label="Apellido Paterno:", help_text='Requerido.',widget=forms.TextInput(attrs={'placeholder': 'Ej: Astudillo','class': 'form-control'}), validators=[apellidosregex])
    apellido_materno=forms.CharField(max_length=30, required=True,label="Apellido Materno:", help_text='Requerido.',widget=forms.TextInput(attrs={'placeholder': 'Ej: Montenegro','class': 'form-control'}), validators=[apellidosregex])
    email = forms.EmailField(max_length=30,widget=forms.TextInput(attrs={'placeholder': 'Ej: example@gmail.com','class': 'form-control'}),label="Email:", help_text='Informe una dirección de correo válida.')
    
    def __init__(self,*args,**kwargs):
        self.username = kwargs.pop('username')
        super(UpdateFormAdministrador,self).__init__(*args,**kwargs)

    def clean_email(self):
        email=self.cleaned_data['email']
        user = User.objects.get(username=self.username)

        if str(user.email) == email:
            pass
        elif str(user.email) != email: 
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError(_('Este email ya esta asociado a una cuenta de usuario'), code='invalid')
        return email

class GenerateStatisticsForm(forms.Form):
    list_regiones=(
            (1, _("I")),
            (2, _("II")),
            (3, _("III")),
            (4, _("IV")),
            (5, _("V")),
            (6, _("VI")),
            (7, _("VII")),
            (8, _("VIII")),
            (9, _("IX")),
            (10, _("X")),
            (11, _("XI")),
            (12, _("XII")),
            (13, _("RM")),
            (14, _("XIV")),
            (15, _("XV")),
        )
   
    
    region = forms.ChoiceField(required=True,choices = list_regiones, label="Región:", initial='1', widget=forms.Select(attrs={'placeholder': 'Ej: jroman@gmail.com','class': 'form-control'}),help_text='')
    enfermedad = forms.ChoiceField(required=True,choices=[(enfermedad.id_who, enfermedad.nombre) for enfermedad in Enfermedad.objects.all()],widget=forms.Select(attrs={'placeholder': 'Ej: jroman@gmail.com','class': 'form-control'}), label='Enfermedad:')


class SearchForm(forms.Form):
    rut_paciente=forms.CharField(max_length=10,label='', required=True,widget=forms.TextInput(attrs={'placeholder': 'Ej: 123456789-k','class': 'form-control'}),validators=[rutregex])

    def clean_rut_paciente(self):
        #rut valido
        rut_form=str(self.cleaned_data['rut_paciente'])
        
        
        rut_limpio = rut_form.replace(".","")
        
        digito_verificador = rut_limpio[-1:]

        if digito_verificador=="k" or digito_verificador=="K":
            digito_verificador = 10
        rut_limpio = rut_limpio[:-2]
        reversed_digits = map(int, reversed(rut_limpio))
        factors = cycle(range(2, 8))
        suma = sum(d * f for d, f in zip(reversed_digits, factors))
        digito_resultado= 11 -(suma%11)
        if digito_resultado==11:
            digito_resultado=0

        if int(digito_verificador)!=digito_resultado:
            raise  forms.ValidationError(_("El rut no es valido"), code='invalid')

        #que exista en el Sistema
        if not Paciente.objects.filter(rut_paciente=rut_form).exists():
            raise forms.ValidationError(_('El paciente no existe en el sistema'), code='invalid')
        return rut_form

class ResponderTicket(forms.Form):
    respuesta= forms.CharField(max_length=800,required=True,widget=forms.Textarea(attrs={'placeholder': 'Ej: Respuesta Ingeniosa N°1','class': 'form-control'}))

class ResponderSolicitud(forms.Form):
    choices=(
            (1, _("Aprobado")),
            (2, _("Rechazado")),
        )
    estado = forms.ChoiceField(choices=choices,widget=forms.RadioSelect(attrs={}))

class RecuperarCuentaForm (forms.Form):
    email =forms.EmailField(max_length=30,required=True,widget=forms.TextInput(attrs={'placeholder': 'Ej: pjhfxx@gmail.com','class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        if  User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user.is_active == True:
                raise forms.ValidationError(_('Esta cuenta ya está activa'), code='invalid')
        else:
             raise forms.ValidationError(_('No se ha encontrado una cuenta desactivada con este mail'), code='invalid')

        return email