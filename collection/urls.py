from django.urls import path
from . import views

app_name = 'collection'

urlpatterns = [
    path('', views.ma_collection, name='ma_collection'),
    path('echanges/', views.mes_echanges, name='mes_echanges'),
    path('echanges/<int:pk>/<str:decision>/', views.repondre_echange, name='repondre_echange'),
    path('echanger/<str:username>/', views.proposer_echange, name='proposer_echange'),
]
