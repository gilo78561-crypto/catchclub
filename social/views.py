from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Post, Commentaire, Abonnement
from .forms import PostForm, CommentaireForm

Dresseur = get_user_model()


@login_required
def fil(request):
    """Fil d'actualité : posts des dresseurs suivis + les siens."""
    if not request.user.a_un_pokemone():
        return redirect('comptes:creer_pokemon')

    suivis_ids = list(request.user.abonnements.values_list('suivi_id', flat=True))
    suivis_ids.append(request.user.id)
    posts = Post.objects.filter(auteur_id__in=suivis_ids).select_related('auteur', 'auteur__pokemone')

    form = PostForm()
    return render(request, 'social/fil.html', {'posts': posts, 'form': form})


@login_required
@require_POST
def publier(request):
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
        post = form.save(commit=False)
        post.auteur = request.user
        post.save()
        messages.success(request, 'Publié !')
    return redirect('social:fil')


@login_required
@require_POST
def aimer(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.aimes_par.all():
        post.aimes_par.remove(request.user)
    else:
        post.aimes_par.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'social:fil'))


@login_required
@require_POST
def commenter(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentaireForm(request.POST)
    if form.is_valid():
        commentaire = form.save(commit=False)
        commentaire.post = post
        commentaire.auteur = request.user
        parent_id = request.POST.get('parent_id')
        if parent_id:
            commentaire.parent = get_object_or_404(Commentaire, id=parent_id, post=post)
        commentaire.save()
    return redirect(request.META.get('HTTP_REFERER', 'social:fil'))


@login_required
@require_POST
def suivre(request, username):
    """Le dresseur connecté s'abonne à un autre dresseur (débloque sa carte, voir collection.signals)."""
    cible = get_object_or_404(Dresseur, username=username)
    if cible != request.user:
        Abonnement.objects.get_or_create(suiveur=request.user, suivi=cible)
        messages.success(request, f"Tu suis maintenant {cible.username}.")
    return redirect('comptes:profil', username=username)


@login_required
@require_POST
def se_desabonner(request, username):
    cible = get_object_or_404(Dresseur, username=username)
    Abonnement.objects.filter(suiveur=request.user, suivi=cible).delete()
    messages.info(request, f"Tu ne suis plus {cible.username}.")
    return redirect('comptes:profil', username=username)


@login_required
def rechercher(request):
    """Recherche de dresseurs par nom d'utilisateur ou nom de pokémone."""
    from groupes.models import Groupe

    q = request.GET.get('q', '').strip()
    dresseurs = []
    groupes = []
    if q:
        dresseurs = Dresseur.objects.filter(
            models.Q(username__icontains=q) | models.Q(pokemone__nom__icontains=q)
        ).select_related('pokemone').distinct()
        groupes = Groupe.objects.filter(nom__icontains=q)

    return render(request, 'social/recherche.html', {'q': q, 'dresseurs': dresseurs, 'groupes': groupes})
