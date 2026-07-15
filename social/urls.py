from django.urls import path
from . import views

app_name = 'social'

urlpatterns = [
    path('', views.fil, name='fil'),
    path('publier/', views.publier, name='publier'),
    path('post/<int:post_id>/aimer/', views.aimer, name='aimer'),
    path('post/<int:post_id>/commenter/', views.commenter, name='commenter'),
    path('suivre/<str:username>/', views.suivre, name='suivre'),
    path('se-desabonner/<str:username>/', views.se_desabonner, name='se_desabonner'),
    path('recherche/', views.rechercher, name='rechercher'),
]
