from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .models import Post, Commentary
from django.http import HttpResponseRedirect, HttpRequest
from django.urls import reverse
from django.views.generic import (
                    ListView, 
                    DetailView, 
                    CreateView,
                    UpdateView,
                    DeleteView
                    )
#Las views pueden ser Class views que aportan mas funcionalidad, busca en la doc de django
#En estas class views tu le dices el model con el que va a interactuar y ella se encarg de casi todo lo demas

def LikeView(request, pk): #Funcion que recoge en qué post le han dado like y le suma el like
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    url = request.POST.get('next')

    #Busca como hacer que al dar like te deje en la misma pagina donde estás
    return HttpResponseRedirect(url)#Nos envia al post en el que estamos

class PostListView(ListView): #Esta es la pagina principal, que es una lista de posts
    model = Post #Le decimos el model con el que interactua
    template_name = 'blog/home.html' #El template que debe cargar
    context_object_name = 'posts' #El nombre de la variable que pasamos a los templates
    ordering = ['-date_posted'] #Le decimos que los muestre del ultimo subido al primero
    paginate_by = 5 #Le decimos que en cada pagona muestre un max de 5 posts
                    #Mostrar demasiados haria a la pagina lenta

class UserPostListView(ListView): #Los posts de un usuario concreto
    model = Post 
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts' 
    paginate_by = 5

    #Esta viene en django pensada para que la sobreescribas para filtrar lo que muestra la ListView
    def get_queryset(self):
        #Cogemos el autor dle post (si no existe da 404), lo saca del url
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author = user).order_by('-date_posted')
        #Solo muestra los posts creados por el autor del post en el que hemos clicado

class PosteDetailView(DetailView): #Esta muestra los detalles de un post especifico cuando te metes en ese post
    model = Post
    context_object_name = 'post'
    #<app>/<model>_<viewtype>.html Por defecto va a cargar un template que tenga ese formato, si nuestro template tiene
    #                              ese formato no hay que poner un template_name

    def get_context_data(self, *args, **kwargs): #Añadimos a lo que pasamos al template los likes
        context = super().get_context_data(**kwargs) #Esto se pone siempre

        #En este caso esto no sirve de nada porque en el template uso post.likes.count y me sirve
        #Pero es interesante ver el funcionamiento de esto
        #Context es lo que pasas al template, en las classviews hay que llamar a esta get_context_data()
        post = get_object_or_404(Post, id=self.kwargs['pk']) #Cogemos el post cuyo id es el que está en el url
        total_likes = post.total_likes() #Llamamos a la funcion que cuenta likes que hemos creado
        context["total_likes"] = total_likes #Lo pasamos al template y alli podemos acceder a estos datos con el nombre que pongamos en los corchetes
        return context

class CommentaryCreateView(LoginRequiredMixin, CreateView):
    model = Commentary	                                 
    fields = ['content'] #Se mete el comentario


    def form_valid(self, form): 
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['pk']#En kwargs creo que se accede a lo que haya en el url. En este caso le estamos diciendo que el id del post
        return super().form_valid(form)         #al que esta comentando es el 'pk' que hay en el url y con eso lo identifica y se asigna
    
    def get_success_url(self):
        url = self.request.POST['next']
        return url



#Los mixins a la izq del class view
class PostCreateView(LoginRequiredMixin, CreateView): #View para crear, es un form. LoginRequiredMixing hace que haya que estar login para acceder
    model = Post	                                  #Por defecto busca el template <app>/<model>_form.html
    fields = ['title', 'content', 'image'] #El form tendra para meter title y content

    def form_valid(self, form): 
        form.instance.author = self.request.user #Si el form esta bien, se asigna al auhtor el usuario que lo ha creado
        return super().form_valid(form) #Se devuelve el form_valid de django despues de hacer ese cambio

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): #View para cambiar un post. Por defecto busca el template <app>/<model>_form.html
                    #UserPassesTest hace que el usuario tenga que cumplir lo que ponemos en test_func para acceder
    model = Post	
    fields = ['title', 'content']

    def form_valid(self, form): #Cuando se modifica se le dice cual es el autor del post (el model lo necesita)
        form.instance.author = self.request.user
        return super().form_valid(form) #Realmente funciona sin esta funcion peor Corey la puso y eso va a misa

    def test_func(self): #UserPassesTest
        post = self.get_object() #Cogemos el post que esta mirando
        if self.request.user == post.author: #Comprueba que el que lo mira es el que lo creo
            return True
        return False #Si no lo es no permite modificarlo

class PosteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):#Por defecto busca el template <app>/<model>_confirm_delete.html
    model = Post
    success_url = '/' #Si lo borras te manda al home

    def test_func(self): #UserPassesTestMixin
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
    #Cuando alguien va a la pagina de about esto hace que cargue el about.html
