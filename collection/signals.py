from django.db.models.signals import post_save
from django.dispatch import receiver

from social.models import Abonnement
from .models import PossessionCarte


@receiver(post_save, sender=Abonnement)
def debloquer_carte_a_l_abonnement(sender, instance, created, **kwargs):
    """
    Quand un dresseur s'abonne à un autre, il débloque automatiquement
    la carte du pokémone suivi dans sa collection (si celui-ci a déjà
    créé son pokémone).
    """
    if not created:
        return
    pokemone = getattr(instance.suivi, 'pokemone', None)
    if pokemone is not None:
        PossessionCarte.objects.get_or_create(collectionneur=instance.suiveur, pokemone=pokemone)
