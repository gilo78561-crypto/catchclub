from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def liste(request):
    notifications = list(request.user.notifications.all()[:50])
    # On marque tout comme lu une fois que le dresseur a ouvert la page.
    request.user.notifications.filter(lu=False).update(lu=True)
    return render(request, 'notifications/liste.html', {'notifications': notifications})
