from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

#Esto se llaman django signals y en este caso las hemos usado para que cada vez que se creau un usuario
#tambien se cree su perfil. No se muy bien como funcionan, habra que buscar tutoriales
#Ademas para que funcione en apps.py en users hay una def ready(self): Sin esa no funcionaria

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
    