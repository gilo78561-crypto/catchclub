from django.contrib import admin
from .models import PossessionCarte, Echange


@admin.register(PossessionCarte)
class PossessionCarteAdmin(admin.ModelAdmin):
    list_display = ('collectionneur', 'pokemone', 'date_obtention')
    search_fields = ('collectionneur__username', 'pokemone__nom')
    list_filter = ('date_obtention',)


@admin.register(Echange)
class EchangeAdmin(admin.ModelAdmin):
    list_display = ('proposant', 'receveur', 'carte_proposee', 'carte_demandee', 'statut', 'date_creation')
    list_filter = ('statut',)
    search_fields = ('proposant__username', 'receveur__username')
