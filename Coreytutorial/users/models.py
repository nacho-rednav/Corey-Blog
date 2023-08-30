from django.db import models
from django.contrib.auth.models import User
from PIL import Image #libreria pillow

#Creamos un modelo para los perfiles(recuerda hacer migrations)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default = 'default.jpg', upload_to='profile_pics')
    #Default es la foto que usara por defecto si el usuario no sube foto, upload_to es la carpeta donde se guaradaran las profile_imagenes
    #Para usar imagenes he descargado una libreria que se llama Pillow (la descargas y punto no hay que hacer más)

    def __str__(self): #Le decimos que a la hora de hablarnos de los perfiles (en la shell) saque el nombre del usuario y Profile
        return f'{self.user.username} Profile'

    #La funcion save() ya existe en django, la estamos sobreescribiendo
    #Debemos pasar los mismos argumentos que tiene la funcion save de django
    def save(self, *args, **kwargs):  #Esto lo que hace es que cuando se guarda una imagen se asegura
        super().save(*args, **kwargs) #que no es del tamaño maximo
        
        #Esto es de la libreria pillow con la que se manipulan imagenes
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

