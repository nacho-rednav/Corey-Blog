from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self): #Se necesita para que funcionen las signals y se cree un 
        import users.signals #perfil para cada usuario
