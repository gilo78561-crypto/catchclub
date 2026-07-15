from django.urls import path
from . import views

app_name = 'messagerie'

urlpatterns = [
    path('', views.liste_conversations, name='liste'),
    path('<int:pk>/', views.conversation_detail, name='detail'),
    path('<int:pk>/envoyer/', views.envoyer_message, name='envoyer'),
    path('nouvelle/<str:username>/', views.demarrer_conversation, name='demarrer'),
]
