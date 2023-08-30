"""Coreytutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views as user_views                
from django.contrib.auth import views as auth_views  #Funciones ya hechas de django que
                                                      #no se muy bien que hacen
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls), #Aqui se va a la pagina del admin que viene por defcto
    path('', include('blog.urls')),
    #El '' hace que la pagina que se muestra por defecto sea la que luego en blog.urls tiene ''
    #El include('blog.urls') hace que ese path vaya a ese documento y sigue los urls que pone allí
    path('register/', user_views.register, name='register'),
    #Camino que se sigue cuando alguien quiere ir a registrarse
    path('login/', auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),    #Con esto se aprovechan lo que ya hay hecho en
    path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html"), name="logout"),#django para login y logout
    path('profile/', user_views.profile, name='profile'),
    #Estos son todos los paths para realizar el reset de la contraseña si te olvidas, las views viene hechas ya en django
    path('password-reset/', 
        auth_views.PasswordResetView.as_view( #La incial, te pide un email. Si metes uno que no es de ningun usuario no hace nada
            template_name="users/password_reset.html"), 
        name="password_reset"),
    path('password-reset/done', #Tras hacer eso debemos crear un template con este nombre, dice basicamente
        auth_views.PasswordResetDoneView.as_view( #que se le ha enviado un email para cambiar contraseña
            template_name="users/password_reset_done.html"), 
        name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>', 
        auth_views.PasswordResetConfirmView.as_view( #Aqui es donde cambias tu contraseña
            template_name="users/password_reset_confirm.html"), 
        name="password_reset_confirm"),
    path('password-reset-complete/', #Tras eso debemos cear un template con el mismo nombre que este
        auth_views.PasswordResetCompleteView.as_view(#Basicamente dirá, contraseña cambiada
            template_name="users/password_reset_complete.html"),
        name="password_reset_complete"),
]

if settings.DEBUG: #Esto no se que hace pero hace falta para las imagenes creo
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
