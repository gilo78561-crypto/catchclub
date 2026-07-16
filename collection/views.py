from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import PossessionCarte, Echange
from notifications.models import Notification

Dresseur = get_user_model()


@login_required
def ma_collection(request):
    cartes = PossessionCarte.objects.filter(collectionneur=request.user).select_related('pokemone', 'pokemone__dresseur')
    return render(request, 'collection/collection.html', {
        'cartes': cartes,
        'total_dresseurs': Dresseur.objects.filter(pokemone__isnull=False).count(),
    })


@login_required
def proposer_echange(request, username):
    """Écran d'échange avec un dresseur donné."""
    autre = get_object_or_404(Dresseur, username=username)
    mes_cartes = PossessionCarte.objects.filter(collectionneur=request.user)
    ses_cartes = PossessionCarte.objects.filter(collectionneur=autre)

    if request.method == 'POST':
        carte_proposee_id = request.POST.get('carte_proposee')
        carte_demandee_id = request.POST.get('carte_demandee')
        carte_proposee = get_object_or_404(PossessionCarte, id=carte_proposee_id, collectionneur=request.user)
        carte_demandee = get_object_or_404(PossessionCarte, id=carte_demandee_id, collectionneur=autre)
        Echange.objects.create(
            proposant=request.user, receveur=autre,
            carte_proposee=carte_proposee, carte_demandee=carte_demandee,
        )
        Notification.creer(autre, f"{request.user.username} te propose un échange de cartes.", '/collection/echanges/')
        messages.success(request, f"Proposition d'échange envoyée à {autre.username}.")
        return redirect('collection:mes_echanges')

    return render(request, 'collection/echange.html', {
        'autre': autre, 'mes_cartes': mes_cartes, 'ses_cartes': ses_cartes,
    })


@login_required
def mes_echanges(request):
    envoyes = Echange.objects.filter(proposant=request.user)
    recus = Echange.objects.filter(receveur=request.user)
    return render(request, 'collection/mes_echanges.html', {'envoyes': envoyes, 'recus': recus})


@login_required
@require_POST
def repondre_echange(request, pk, decision):
    echange = get_object_or_404(Echange, pk=pk, receveur=request.user, statut='en_attente')
    if decision == 'accepter':
        # On échange les propriétaires des deux cartes.
        c1, c2 = echange.carte_proposee, echange.carte_demandee
        c1.collectionneur, c2.collectionneur = c2.collectionneur, c1.collectionneur
        c1.save()
        c2.save()
        echange.statut = 'acceptee'
        Notification.creer(echange.proposant, f"{request.user.username} a accepté ton échange !", '/collection/echanges/')
        messages.success(request, 'Échange conclu !')
    else:
        echange.statut = 'refusee'
        Notification.creer(echange.proposant, f"{request.user.username} a refusé ton échange.", '/collection/echanges/')
        messages.info(request, 'Échange refusé.')
    echange.date_reponse = timezone.now()
    echange.save()
    return redirect('collection:mes_echanges')
