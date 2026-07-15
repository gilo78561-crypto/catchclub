from django.conf import settings
from django.db import models

Dresseur = settings.AUTH_USER_MODEL

EXTENSIONS_VIDEO = ('.mp4', '.webm', '.mov', '.ogg')


class Conversation(models.Model):
    participants = models.ManyToManyField(Dresseur, related_name='conversations')
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'conversation'
        verbose_name_plural = 'conversations'

    def __str__(self):
        noms = ", ".join(p.username for p in self.participants.all())
        return f"Conversation ({noms})"

    @property
    def dernier_message(self):
        return self.messages.order_by('-date_envoi').first()

    def autre_participant(self, utilisateur):
        return self.participants.exclude(id=utilisateur.id).first()


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    auteur = models.ForeignKey(Dresseur, on_delete=models.CASCADE, related_name='messages_envoyes')
    contenu = models.CharField('message', max_length=1000, blank=True)
    fichier = models.FileField('image ou vidéo', upload_to='messages/', blank=True, null=True)
    date_envoi = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_envoi']
        verbose_name = 'message'
        verbose_name_plural = 'messages'

    def __str__(self):
        return f"{self.auteur}: {self.contenu[:30]}"

    @property
    def est_video(self):
        return bool(self.fichier) and self.fichier.name.lower().endswith(EXTENSIONS_VIDEO)

    @property
    def est_image(self):
        return bool(self.fichier) and not self.est_video
