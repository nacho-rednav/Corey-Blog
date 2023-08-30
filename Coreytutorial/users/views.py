from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
#Hay que importar todo esto de forms para usarlo aqui

def register(request):
    if request.method == 'POST': #Si lo que ha hecho es rellenar el form
        form = UserRegisterForm(request.POST)
        if form.is_valid(): #Si lo relleno bien
            form.save() #Guardamos en usuario en la base de datos
            username = form.cleaned_data.get('username') #Accedemos al nombre del usuario para poner el mensajito de abajo
            messages.success(request, f'Account created for {username}, log in!')
            return redirect('login') #Te manda a la pagina del log in
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required  #Solo le muestra la pagina a quien haya hecho log in
def profile(request):
    if request.method == 'POST': #Si le ha dado a cambiar datos del perfil
        u_form = UserUpdateForm(request.POST, instance= request.user)
        #Form para cambiar nombre y email, el instance sirve para que salgan los
        #datos actuales del usuario
        p_form = ProfileUpdateForm(request.POST, request.FILES, 
                                instance = request.user.profile)
        #Form para cambiar la foto de perfil

        #En ambos pasamos el request.POST y request.FILES (para la imagen)
        #porque si no al darle a submit no guardaria nada
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Account updated')
            return redirect('profile')
            #Esto te envia a profile tambien, con esto se evita que salga
            #un mensaje de ¿Seguro que quieres volver a mandar el formulario?
            #Cuando el usuario recraga despues de mandar el form
    
    else:
        u_form = UserUpdateForm(instance= request.user)
        p_form = ProfileUpdateForm(instance = request.user.profile)

    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }
    #Para pasar variables a un render se crea un diccionario llamado context,
    #la primer parte sera el nombre de la variable y la segunda el instance que mandamos 
    #desde aqui al html
    return render(request, 'users/profile.html', context)