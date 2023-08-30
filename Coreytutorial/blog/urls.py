from django.urls import path
from . import views
from .views import (PostListView, 
                    PosteDetailView,
                    PostCreateView,
                    PostUpdateView,
                    PosteDeleteView,
                    UserPostListView,
                    CommentaryCreateView,
                    LikeView
                    )

urlpatterns = [
    path('', PostListView.as_view(), name = 'blog-home'),
    #El urls principal te trae aquí y como es '' pues ese es el url por defecto
    path('user/<str:username>/', UserPostListView.as_view(), name = 'user-posts'),
    path('about/', views.about, name = 'blog-about'),
    #Esto hace que cargue el views de about cuando alguien se mete al about
    path('post/<int:pk>/', PosteDetailView.as_view(), name = 'post-detail'),
    #El <int:pk> (int: no es esencial) le dice que cargue el view de ese post especifico, el pk es como su numero de id
    path('post/<int:pk>/comment/', CommentaryCreateView.as_view(), name = 'commentary-create'),
    path('post/new/', PostCreateView.as_view(), name = 'post-create'),
    path('post/<int:pk>/delete/', PosteDeleteView.as_view(), name = 'post-delete'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name = 'post-update'),
    #Al pasar ClassViews tienes que meterle el as_view() porque si no nocarga
    path('like/<int:pk>/', LikeView, name="post-like")
]