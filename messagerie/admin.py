from django.contrib import admin
from .models import Conversation, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('auteur', 'contenu', 'date_envoi')


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'date_creation')
    inlines = [MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('auteur', 'conversation', 'contenu', 'date_envoi')
    search_fields = ('contenu', 'auteur__username')
