from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Groupe, Adhesion


@login_required
def liste(request):
    type_filtre = request.GET.get('type')
    groupes = Groupe.objects.all()
    if type_filtre:
        groupes = groupes.filter(type=type_filtre)

    mes_groupes = request.user.groupes.all()
    return render(request, 'groupes/liste.html', {
        'groupes': groupes,
        'mes_groupes': mes_groupes,
        'type_filtre': type_filtre,
        'types': Groupe._meta.get_field('type').choices,
    })


@login_required
def detail(request, pk):
    groupe = get_object_or_404(Groupe, pk=pk)
    est_membre = groupe.membres.filter(id=request.user.id).exists()
    return render(request, 'groupes/detail.html', {'groupe': groupe, 'est_membre': est_membre})


@login_required
@require_POST
def rejoindre(request, pk):
    groupe = get_object_or_404(Groupe, pk=pk)
    Adhesion.objects.get_or_create(dresseur=request.user, groupe=groupe)
    return redirect('groupes:detail', pk=pk)


@login_required
@require_POST
def quitter(request, pk):
    groupe = get_object_or_404(Groupe, pk=pk)
    Adhesion.objects.filter(dresseur=request.user, groupe=groupe).delete()
    return redirect('groupes:detail', pk=pk)
