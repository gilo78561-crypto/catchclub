from django.conf import settings
from django.db import models

Dresseur = settings.AUTH_USER_MODEL


class Post(models.Model):
    auteur = models.ForeignKey(Dresseur, on_delete=models.CASCADE, related_name='posts')
    contenu = models.TextField('contenu', max_length=1000)
    image = models.ImageField('image', upload_to='posts/', blank=True, null=True)
    date_publication = models.DateTimeField(auto_now_add=True)
    aimes_par = models.ManyToManyField(Dresseur, related_name='posts_aimes', blank=True)

    class Meta:
        ordering = ['-date_publication']
        verbose_name = 'publication'
        verbose_name_plural = 'publications'

    def __str__(self):
        return f"{self.auteur} — {self.contenu[:40]}"

    @property
    def nb_likes(self):
        return self.aimes_par.count()

    @property
    def nb_commentaires(self):
        return self.commentaires.count()


class Commentaire(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='commentaires')
    auteur = models.ForeignKey(Dresseur, on_delete=models.CASCADE, related_name='commentaires')
    contenu = models.CharField('contenu', max_length=300)
    date_publication = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_publication']
        verbose_name = 'commentaire'
        verbose_name_plural = 'commentaires'

    def __str__(self):
        return f"{self.auteur} sur #{self.post_id}"


class Abonnement(models.Model):
    """
    Relation de suivi entre deux dresseurs (façon "abonnés").
    suiveur  = celui qui s'abonne
    suivi    = celui qui est suivi (gagne un abonné)

    L'administrateur dispose de droits complets sur ce modèle depuis
    l'admin Django (voir social/admin.py) : consultation, suppression
    et modération des abonnements de n'importe quel dresseur.
    """
    suiveur = models.ForeignKey(Dresseur, on_delete=models.CASCADE, related_name='abonnements')
    suivi = models.ForeignKey(Dresseur, on_delete=models.CASCADE, related_name='abonnes')
    date_abonnement = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('suiveur', 'suivi')
        verbose_name = 'abonnement'
        verbose_name_plural = 'abonnements'
        permissions = [
            ('moderer_abonnement', "Peut modérer (forcer la suppression) un abonnement"),
        ]

    def __str__(self):
        return f"{self.suiveur} suit {self.suivi}"
