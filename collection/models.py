from django.conf import settings
from django.db import models

Dresseur = settings.AUTH_USER_MODEL


class PossessionCarte(models.Model):
    """
    Une carte obtenue par un dresseur (le collectionneur) et représentant
    le pokémone d'un autre dresseur. Une carte est débloquée automatiquement
    quand on s'abonne à quelqu'un (voir collection/signals.py).
    """
    collectionneur = models.ForeignKey(Dresseur, on_delete=models.CASCADE, related_name='cartes_possedees')
    pokemone = models.ForeignKey('comptes.Pokemone', on_delete=models.CASCADE, related_name='cartes')
    date_obtention = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('collectionneur', 'pokemone')
        verbose_name = 'carte possédée'
        verbose_name_plural = 'cartes possédées'
        ordering = ['-date_obtention']

    def __str__(self):
        return f"Carte {self.pokemone.nom} possédée par {self.collectionneur}"


class Echange(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('acceptee', 'Acceptée'),
        ('refusee', 'Refusée'),
        ('annulee', 'Annulée'),
    ]

    proposant = models.ForeignKey(Dresseur, on_delete=models.CASCADE, related_name='echanges_proposes')
    receveur = models.ForeignKey(Dresseur, on_delete=models.CASCADE, related_name='echanges_recus')
    carte_proposee = models.ForeignKey(PossessionCarte, on_delete=models.CASCADE, related_name='+')
    carte_demandee = models.ForeignKey(PossessionCarte, on_delete=models.CASCADE, related_name='+')
    statut = models.CharField(max_length=15, choices=STATUT_CHOICES, default='en_attente')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_reponse = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'échange'
        verbose_name_plural = 'échanges'
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.proposant} ↔ {self.receveur} ({self.get_statut_display()})"
