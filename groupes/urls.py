from django.urls import path
from . import views

app_name = 'groupes'

urlpatterns = [
    path('', views.liste, name='liste'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/rejoindre/', views.rejoindre, name='rejoindre'),
    path('<int:pk>/quitter/', views.quitter, name='quitter'),
]
