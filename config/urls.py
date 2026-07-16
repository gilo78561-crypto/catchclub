from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from django.views.static import serve


def service_worker(request):
    """
    Sert sw.js depuis la racine du site (et non /static/sw.js) : c'est
    nécessaire pour que le service worker puisse contrôler l'ensemble du
    site (sa "portée" par défaut se limite au dossier où il est servi).
    """
    with open(settings.BASE_DIR / 'static' / 'sw.js', 'rb') as f:
        return HttpResponse(f.read(), content_type='application/javascript')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('sw.js', service_worker, name='service_worker'),
    path('comptes/', include('comptes.urls')),
    path('', include('social.urls')),
    path('groupes/', include('groupes.urls')),
    path('collection/', include('collection.urls')),
    path('messages/', include('messagerie.urls')),
    path('notifications/', include('notifications.urls')),
]

# NB : servir les médias depuis Django (plutôt qu'un stockage externe type S3)
# n'est pas recommandé pour un vrai site en production, mais convient pour
# ce déploiement de test entre amis. Sur le tarif gratuit de Render, le
# disque est éphémère : les images envoyées par les utilisateurs sont
# perdues à chaque redéploiement/redémarrage du service.
urlpatterns += [
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
]
