from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('destinataire', 'texte', 'lu', 'date_creation')
    list_filter = ('lu', 'date_creation')
    search_fields = ('destinataire__username', 'texte')
