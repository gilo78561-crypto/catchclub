from django.urls import path
from . import views

app_name = 'comptes'

urlpatterns = [
    path('inscription/', views.inscription, name='inscription'),
    path('inscription/pokemon/', views.creer_pokemon, name='creer_pokemon'),
    path('connexion/', views.ConnexionView.as_view(), name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('profil/modifier/', views.modifier_profil, name='modifier_profil'),
    path('mon-pokemon/', views.mon_pokemon, name='mon_pokemon'),
    path('mon-pokemon/interagir/<str:action>/', views.interagir, name='interagir'),
    path('profil/<str:username>/', views.profil, name='profil'),
]
