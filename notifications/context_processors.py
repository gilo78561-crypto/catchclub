def notifications_non_lues(request):
    """Rend le nombre de notifications non lues disponible dans tous les
    templates, pour afficher le petit point rouge sur la cloche du header."""
    if request.user.is_authenticated:
        return {'nb_notifications_non_lues': request.user.notifications.filter(lu=False).count()}
    return {}
