from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('comptes/', include('comptes.urls')),
    path('', include('social.urls')),
    path('groupes/', include('groupes.urls')),
    path('collection/', include('collection.urls')),
    path('messages/', include('messagerie.urls')),
]

# NB : servir les médias depuis Django (plutôt qu'un stockage externe type S3)
# n'est pas recommandé pour un vrai site en production, mais convient pour
# ce déploiement de test entre amis. Sur le tarif gratuit de Render, le
# disque est éphémère : les images envoyées par les utilisateurs sont
# perdues à chaque redéploiement/redémarrage du service.
urlpatterns += [
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
]
