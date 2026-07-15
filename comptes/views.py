from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import InscriptionForm, PokemoneForm, ProfilForm
from .models import Dresseur


ACTIONS_INTERACTION = {
    'nourrir': {'gain': 8, 'animation': 'anim-pulse', 'message': "{nom} a bien mangé !"},
    'jouer': {'gain': 5, 'animation': 'anim-jump', 'message': "{nom} adore jouer avec toi !"},
    'caliner': {'gain': 5, 'animation': 'anim-wiggle', 'message': "{nom} ronronne de bonheur."},
}


def inscription(request):
    """Étape 1/2 : création du compte (username, email, mot de passe)."""
    if request.user.is_authenticated:
        return redirect('social:fil')

    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            dresseur = form.save()
            login(request, dresseur)
            messages.success(request, "Compte créé ! Il ne reste plus qu'à créer ton pokémone.")
            return redirect('comptes:creer_pokemon')
    else:
        form = InscriptionForm()

    return render(request, 'comptes/inscription.html', {'form': form, 'etape': 1})


@login_required
def creer_pokemon(request):
    """Étape 2/2 : création libre du pokémone lié au dresseur connecté."""
    if request.user.a_un_pokemone():
        return redirect('social:fil')

    if request.method == 'POST':
        form = PokemoneForm(request.POST, request.FILES)
        if form.is_valid():
            pokemone = form.save(commit=False)
            pokemone.dresseur = request.user
            pokemone.save()
            messages.success(request, f"Bienvenue sur CatchClub avec {pokemone.nom} !")
            return redirect('social:fil')
    else:
        form = PokemoneForm()

    return render(request, 'comptes/creer_pokemon.html', {'form': form, 'etape': 2})


class ConnexionView(LoginView):
    template_name = 'comptes/connexion.html'


@login_required
def deconnexion(request):
    logout(request)
    return redirect('comptes:connexion')


@login_required
def profil(request, username):
    dresseur = get_object_or_404(Dresseur, username=username)
    posts = dresseur.posts.all().order_by('-date_publication')
    est_soi_meme = dresseur == request.user
    suit_deja = False
    if not est_soi_meme:
        suit_deja = request.user.abonnements.filter(suivi=dresseur).exists()

    return render(request, 'comptes/profil.html', {
        'dresseur': dresseur,
        'posts': posts,
        'est_soi_meme': est_soi_meme,
        'suit_deja': suit_deja,
    })


@login_required
def modifier_profil(request):
    if request.method == 'POST':
        form = ProfilForm(request.POST, instance=request.user)
        pokemon_form = PokemoneForm(request.POST, request.FILES, instance=request.user.pokemone)
        if form.is_valid() and pokemon_form.is_valid():
            form.save()
            pokemon_form.save()
            messages.success(request, 'Profil mis à jour.')
            return redirect('comptes:profil', username=request.user.username)
    else:
        form = ProfilForm(instance=request.user)
        pokemon_form = PokemoneForm(instance=request.user.pokemone)

    return render(request, 'comptes/modifier_profil.html', {
        'form': form,
        'pokemon_form': pokemon_form,
    })


@login_required
def mon_pokemon(request):
    """Page interactive : grand modèle 3D + actions (nourrir, jouer, câliner)."""
    if not request.user.a_un_pokemone():
        return redirect('comptes:creer_pokemon')

    return render(request, 'comptes/mon_pokemon.html', {
        'pokemone': request.user.pokemone,
        'actions': ACTIONS_INTERACTION,
    })


@login_required
@require_POST
def interagir(request, action):
    """Action AJAX : augmente l'affection du pokémone et renvoie le nouvel état en JSON."""
    if not request.user.a_un_pokemone():
        return JsonResponse({'erreur': "Tu n'as pas encore de pokémone."}, status=400)

    config = ACTIONS_INTERACTION.get(action)
    if not config:
        return JsonResponse({'erreur': 'Action inconnue.'}, status=400)

    pokemone = request.user.pokemone
    niveau_avant = pokemone.niveau
    pokemone.affection += config['gain']
    pokemone.save(update_fields=['affection'])

    return JsonResponse({
        'affection': pokemone.affection,
        'niveau': pokemone.niveau,
        'progression': pokemone.progression_niveau,
        'gain': config['gain'],
        'animation': config['animation'],
        'message': config['message'].format(nom=pokemone.nom),
        'niveau_augmente': pokemone.niveau > niveau_avant,
    })
