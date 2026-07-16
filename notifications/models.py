from django.conf import settings
from django.db import models

Dresseur = settings.AUTH_USER_MODEL


class Notification(models.Model):
    destinataire = models.ForeignKey(Dresseur, on_delete=models.CASCADE, related_name='notifications')
    texte = models.CharField('texte', max_length=200)
    lien = models.CharField('lien', max_length=200, blank=True)
    lu = models.BooleanField('lue', default=False)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_creation']
        verbose_name = 'notification'
        verbose_name_plural = 'notifications'

    def __str__(self):
        return f"Pour {self.destinataire} : {self.texte}"

    @staticmethod
    def creer(destinataire, texte, lien=''):
        """Petit raccourci utilisé un peu partout dans le site pour créer
        une notification sans avoir à réimporter le modèle à chaque fois."""
        if destinataire is None:
            return
        Notification.objects.create(destinataire=destinataire, texte=texte, lien=lien)
