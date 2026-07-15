from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db import transaction

from comptes.models import Dresseur, Pokemone
from social.models import Post, Commentaire, Abonnement
from groupes.models import Groupe, Adhesion


DRESSEURS_DEMO = [
    ("Gilo", "eau", "Nymbulle", "Attrapé un jour de pluie, jamais reparti."),
    ("Aika", "plante", "Feuillenn", "Toujours un pas d'avance grâce à Vive-Attaque."),
    ("Ryu", "electrik", "Voltz", "Se recharge au moindre orage."),
    ("Meji", "tenebres", "Umbrescor", "N'a peur de rien, même pas du noir."),
    ("Loran", "dragon", "Dracolim", "Collectionne les défaites... des autres."),
    ("MysteLia", "psy", "Mysté", "Devine toujours ce que tu vas publier."),
    ("Braisor_exe", "feu", "Braisor", "Chauffe l'ambiance à chaque combat."),
]

# Quelques dresseurs de démo utilisent un modèle 3D plutôt qu'une image plate,
# pour montrer immédiatement le rendu model-viewer sur leur profil.
MODELES_3D_DEMO = {
    "Ryu": "rouage",
    "MysteLia": "planetin",
    "Loran": "astrelin",
}

GROUPES_DEMO = [
    ("Brasier Nation", "feu", "Pour tous les dresseurs de pokémones type Feu — combats, élevage, cosmétiques.", False),
    ("Team Aqua Fans", "eau", "Discussions et tournois pour les types Eau. Ambiance détendue.", False),
    ("Jardin Secret", "plante", "Élevage et évolutions des pokémones Plante.", True),
    ("Dresseurs de Dragons", "dragon", "Le repaire des types Dragon. Combats de haut niveau uniquement.", False),
    ("Électrik Squad", "electrik", "Tournois amicaux et bons plans pour dresseurs Électrik.", False),
]


class Command(BaseCommand):
    help = "Crée des données de démonstration (dresseurs, pokémones, posts, groupes, abonnements) et le groupe Modérateurs."

    @transaction.atomic
    def handle(self, *args, **options):
        # --- Groupe d'administration "Modérateurs" ---------------------
        # Droits explicites de l'administrateur sur les abonnements :
        # un membre de ce groupe peut consulter, ajouter, modifier et
        # supprimer n'importe quel abonnement depuis /admin/.
        moderateurs, _ = Group.objects.get_or_create(name='Modérateurs')
        content_type = ContentType.objects.get_for_model(Abonnement)
        permissions = Permission.objects.filter(content_type=content_type)
        moderateurs.permissions.set(permissions)
        self.stdout.write(self.style.SUCCESS(
            f"Groupe 'Modérateurs' prêt avec {permissions.count()} permission(s) sur les abonnements."
        ))

        # --- Compte administrateur de démonstration ---------------------
        if not Dresseur.objects.filter(username='admin').exists():
            admin = Dresseur.objects.create_superuser('admin', 'admin@catchclub.local', 'admin1234')
            admin.groups.add(moderateurs)
            self.stdout.write(self.style.SUCCESS("Superutilisateur 'admin' créé (mot de passe : admin1234)."))

        # --- Compte modérateur (staff, PAS superuser) --------------------
        # Démontre que les droits sur les abonnements viennent bien du
        # groupe "Modérateurs" et pas seulement du statut superutilisateur :
        # ce compte peut se connecter à /admin/ et gérer les abonnements,
        # sans avoir accès aux autres réglages sensibles du site.
        if not Dresseur.objects.filter(username='modo').exists():
            modo = Dresseur.objects.create_user('modo', 'modo@catchclub.local', 'moderateur123')
            modo.is_staff = True
            modo.save()
            modo.groups.add(moderateurs)
            self.stdout.write(self.style.SUCCESS("Compte modérateur 'modo' créé (mot de passe : moderateur123)."))

        # --- Dresseurs + pokémones ---------------------------------------
        dresseurs = {}
        for username, type_, nom_pkm, presentation in DRESSEURS_DEMO:
            dresseur, cree = Dresseur.objects.get_or_create(
                username=username, defaults={'email': f'{username.lower()}@catchclub.local'}
            )
            if cree:
                dresseur.set_password('motdepasse123')
                dresseur.save()
            Pokemone.objects.get_or_create(
                dresseur=dresseur,
                defaults={
                    'nom': nom_pkm, 'type': type_, 'presentation': presentation,
                    'points_de_vie': 50, 'modele_3d': MODELES_3D_DEMO.get(username, ''),
                }
            )
            dresseurs[username] = dresseur
        self.stdout.write(self.style.SUCCESS(f"{len(dresseurs)} dresseurs prêts (mot de passe : motdepasse123)."))

        # --- Groupes -------------------------------------------------------
        groupes = {}
        for nom, type_, description, prive in GROUPES_DEMO:
            groupe, _ = Groupe.objects.get_or_create(
                nom=nom, defaults={'type': type_, 'description': description, 'prive': prive}
            )
            groupes[nom] = groupe
        for username, dresseur in dresseurs.items():
            for nom_groupe in list(groupes.keys())[:2]:
                Adhesion.objects.get_or_create(dresseur=dresseur, groupe=groupes[nom_groupe])
        self.stdout.write(self.style.SUCCESS(f"{len(groupes)} groupes prêts."))

        # --- Abonnements (débloquent aussi les cartes via signal) ---------
        noms = list(dresseurs.keys())
        for i, username in enumerate(noms):
            for j in range(1, 3):
                cible = dresseurs[noms[(i + j) % len(noms)]]
                Abonnement.objects.get_or_create(suiveur=dresseurs[username], suivi=cible)
        self.stdout.write(self.style.SUCCESS("Abonnements créés (cartes débloquées automatiquement)."))

        # --- Posts + commentaires ------------------------------------------
        exemples_posts = [
            "vient de gagner son 10e combat de rang. On monte tranquillement !",
            "a enfin appris une nouvelle capacité cette nuit. Le grind valait le coup.",
            "cherche un partenaire pour un tournoi ce week-end, qui est chaud ?",
            "a changé d'apparence après son évolution, personne ne m'avait prévenu !",
        ]
        for i, (username, dresseur) in enumerate(dresseurs.items()):
            post, _ = Post.objects.get_or_create(
                auteur=dresseur,
                contenu=f"{dresseur.pokemone.nom} {exemples_posts[i % len(exemples_posts)]}",
            )
            autres = [d for u, d in dresseurs.items() if u != username]
            post.aimes_par.add(*autres[:3])
            Commentaire.objects.get_or_create(
                post=post, auteur=autres[0],
                contenu="Trop bien, bravo !"
            )

        self.stdout.write(self.style.SUCCESS("Publications de démonstration créées."))
        self.stdout.write(self.style.SUCCESS("Terminé. Connecte-toi avec 'admin' / 'admin1234' ou tout autre dresseur / 'motdepasse123'."))
