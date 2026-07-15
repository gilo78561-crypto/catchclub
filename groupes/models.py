from django.conf import settings
from django.db import models
from django.urls import reverse

from comptes.models import TYPES_POKEMON

Dresseur = settings.AUTH_USER_MODEL


class Groupe(models.Model):
    nom = models.CharField('nom', max_length=80)
    type = models.CharField('type associé', max_length=20, choices=TYPES_POKEMON)
    description = models.TextField('description', max_length=400, blank=True)
    prive = models.BooleanField('groupe privé', default=False)
    membres = models.ManyToManyField(Dresseur, through='Adhesion', related_name='groupes')
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'groupe'
        verbose_name_plural = 'groupes'
        ordering = ['nom']

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return reverse('groupes:detail', kwargs={'pk': self.pk})

    @property
    def nb_membres(self):
        return self.membres.count()


class Adhesion(models.Model):
    dresseur = models.ForeignKey(Dresseur, on_delete=models.CASCADE)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    date_adhesion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('dresseur', 'groupe')
        verbose_name = 'adhésion'
        verbose_name_plural = 'adhésions'

    def __str__(self):
        return f"{self.dresseur} dans {self.groupe}"
