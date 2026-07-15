from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


TYPES_POKEMON = [
    ('feu', 'Feu'),
    ('eau', 'Eau'),
    ('plante', 'Plante'),
    ('electrik', 'Électrik'),
    ('psy', 'Psy'),
    ('tenebres', 'Ténèbres'),
    ('dragon', 'Dragon'),
    ('normal', 'Normal'),
]

# Modèles 3D (.glb) fournis, proposés comme apparence au choix à la création
# du pokémone. Le fichier correspondant vit dans static/models/pokemon/.
MODELES_3D = [
    ('raccoony', 'Raccoony'),
    ('rouage', 'Rouage'),
    ('planetin', 'Planétin'),
    ('astrelin', 'Astrelin'),
    ('ailune', 'Ailune'),
]

MODELES_3D_FICHIERS = {
    'raccoony': 'models/pokemon/pixellabs-cute-raccoon-illustration-2735.glb',
    'rouage': 'models/pokemon/pixellabs-steampunk-robot-dog-3d-model-2474.glb',
    'planetin': 'models/pokemon/tiny_planet_friends_3d-tinyplanet-2829.glb',
    'astrelin': 'models/pokemon/tiny_planet_friends_3d-tinyplanet-2830.glb',
    'ailune': 'models/pokemon/wings_of_freedom-cute-2767.glb',
}


class Dresseur(AbstractUser):
    """
    Utilisateur du site. Hérite du système d'authentification de Django
    (username, password, is_staff, is_superuser, etc.) et y ajoute
    les informations propres à un dresseur CatchClub.
    """
    bio = models.CharField('bio', max_length=200, blank=True)
    date_inscription = models.DateTimeField('inscrit le', auto_now_add=True)

    class Meta:
        verbose_name = 'dresseur'
        verbose_name_plural = 'dresseurs'

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('comptes:profil', kwargs={'username': self.username})

    @property
    def nb_abonnes(self):
        return self.abonnes.count()

    @property
    def nb_abonnements(self):
        return self.abonnements.count()

    def a_un_pokemone(self):
        return hasattr(self, 'pokemone')


class Pokemone(models.Model):
    """
    Le pokémone créé librement par le dresseur à l'inscription :
    nom, type et apparence choisis par l'utilisateur.
    """
    dresseur = models.OneToOneField(
        Dresseur, on_delete=models.CASCADE, related_name='pokemone'
    )
    nom = models.CharField('nom', max_length=40)
    type = models.CharField('type', max_length=20, choices=TYPES_POKEMON, default='normal')
    image = models.ImageField('image', upload_to='pokemones/', blank=True, null=True)
    modele_3d = models.CharField('modèle 3D', max_length=20, choices=MODELES_3D, blank=True)
    presentation = models.CharField('petite phrase', max_length=140, blank=True)
    points_de_vie = models.PositiveIntegerField('points de vie', default=50)
    affection = models.PositiveIntegerField('affection', default=0)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'pokémone'
        verbose_name_plural = 'pokémones'

    def __str__(self):
        return f"{self.nom} ({self.get_type_display()})"

    @property
    def niveau(self):
        return 1 + self.affection // 50

    @property
    def progression_niveau(self):
        """Pourcentage (0-100) vers le prochain niveau."""
        return int((self.affection % 50) / 50 * 100)

    @property
    def fichier_3d(self):
        """Chemin static (relatif) du modèle .glb choisi, ou None."""
        if self.modele_3d:
            return MODELES_3D_FICHIERS.get(self.modele_3d)
        return None
