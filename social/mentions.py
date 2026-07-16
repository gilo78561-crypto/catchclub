"""
Petite mécanique de mentions "@nom" réutilisée par les posts et les
commentaires : extraction des dresseurs mentionnés (pour notifier), et
transformation du texte en HTML avec liens cliquables (pour l'affichage).
"""

import re

from django.contrib.auth import get_user_model
from django.utils.html import escape
from django.utils.safestring import mark_safe

MENTION_RE = re.compile(r'@([A-Za-z0-9_]+)')


def extraire_mentions(texte, exclure=None):
    """Renvoie le queryset des dresseurs valablement mentionnés dans le texte."""
    Dresseur = get_user_model()
    usernames = set(MENTION_RE.findall(texte or ''))
    if not usernames:
        return Dresseur.objects.none()
    qs = Dresseur.objects.filter(username__in=usernames)
    if exclure is not None:
        qs = qs.exclude(id=exclure.id)
    return qs


def rendre_mentions(texte):
    """Transforme '@pseudo' en lien cliquable vers le profil, pour les
    pseudos qui correspondent à un vrai compte. Le texte est échappé
    avant traitement, donc sûr à marquer 'safe' ensuite."""
    if not texte:
        return ''

    texte_echappe = escape(texte)
    usernames = set(MENTION_RE.findall(texte_echappe))
    if not usernames:
        return mark_safe(texte_echappe)

    Dresseur = get_user_model()
    existants = set(Dresseur.objects.filter(username__in=usernames).values_list('username', flat=True))

    def remplacer(match):
        nom = match.group(1)
        if nom in existants:
            return f'<a href="/comptes/profil/{nom}/" class="mention">@{nom}</a>'
        return match.group(0)

    return mark_safe(MENTION_RE.sub(remplacer, texte_echappe))
