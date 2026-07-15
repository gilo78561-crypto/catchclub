from django.conf import settings
from django.db import models

Dresseur = settings.AUTH_USER_MODEL


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


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    auteur = models.ForeignKey(Dresseur, on_delete=models.CASCADE, related_name='messages_envoyes')
    contenu = models.CharField('message', max_length=1000)
    date_envoi = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_envoi']
        verbose_name = 'message'
        verbose_name_plural = 'messages'

    def __str__(self):
        return f"{self.auteur}: {self.contenu[:30]}"
