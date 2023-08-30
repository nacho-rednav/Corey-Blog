from django import forms
from django.contrib.auth.models import User #Añadimos esto para decirle que crea un User
from django.contrib.auth.forms import UserCreationForm 
from .models import Profile

#Aqui creamos el form que queremos
class UserRegisterForm(UserCreationForm): #Hereda de user creation form donde incluye la comprtobacion del nombre,
    email = forms.EmailField()            #la contraseña... Y casi todo en general
    #Añadimos el email que no vienen en UserCreationForm

    class Meta: #Le decimos al form con quien interactua (User) y los fields que va a tener
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm): #forms.ModelForm dice que es una form que interactua con un model
    email = forms.EmailField() #Se añade el campo email

    class Meta: 
        model = User #Le decimos que interactua con el usuario
        fields = ['username', 'email']
        #Permite cambiar los campos username y email

class ProfileUpdateForm(forms.ModelForm):
    class Meta: #Creamos otro form que interactue con el perfil
        model = Profile #para poder cambiar la imagen de perfil tambien
        fields = ['image']