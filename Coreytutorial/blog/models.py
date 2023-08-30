from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

#Aqui creo un modelo de como es un post y asi pueden guardarse en la base de datos
class Post(models.Model):
    title = models.CharField(max_length=25)
    content = models.TextField()
    date_posted = models.DateTimeField(default= timezone.now)
    author = models.ForeignKey(User, on_delete= models.CASCADE) #Le dice que hacer con el post si borra el autor
    image = models.ImageField(upload_to='blog_images', blank=True)
    likes = models.ManyToManyField(User, related_name="blog_post") 
    #Es manytomany porque un post puede tener muchos likes dados y un user puede dar muchos likes
    

    def total_likes(self): #Cuenta todos los likes, realmente no lo uso
        return self.likes.count()
        #Lo dejo para que veas lo que hace luego con esto en las views

    def __str__(self):
        return self.title  #En la shell te devuelve el titulo del post si lo buscas

    def get_absolute_url(self): #Devuelve el url del post que se está mirando, esto lo usa la view de crear posts par mandarnos 
                                #al post despues de crearlo
        return reverse('post-detail', kwargs={'pk': self.pk}) #Devuelve el pk del post (es como su id)

    def save(self, *args, **kwargs):  
        super().save(*args, **kwargs) 
    
        if self.image != "":
            img = Image.open(self.image.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)

class Commentary(models.Model):
    author = models.ForeignKey(User, on_delete= models.CASCADE) 
    post = models.ForeignKey(Post, on_delete= models.CASCADE, related_name="comments") #ForeignKey crea una relacion en la que en el model que has
    date_posted = models.DateTimeField(default= timezone.now)                          #puesto el foreignkey es el many, y al model con el que se relaciona (Post en este caso)
    content = models.TextField()                                                        #es el one (many to one). Es como si post tuviese un field = Commentary, gracias a que
                                                                                        #ahora estan relacionados entre si
    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return 'By {} in {}'.format(self.author, self.post.title)

