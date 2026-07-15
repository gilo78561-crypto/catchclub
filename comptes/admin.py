from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Dresseur, Pokemone


class PokemoneInline(admin.StackedInline):
    model = Pokemone
    extra = 0


@admin.register(Dresseur)
class DresseurAdmin(UserAdmin):
    """
    Administration des dresseurs. Un administrateur peut ici gérer les comptes,
    voir/éditer leur pokémone (inline), et modérer (désactiver un compte via
    is_active retire aussi ses abonnements de la vue publique).
    """
    inlines = [PokemoneInline]
    list_display = ('username', 'email', 'is_staff', 'is_active', 'nb_abonnes_admin', 'nb_abonnements_admin', 'date_inscription')
    list_filter = ('is_staff', 'is_active', 'date_inscription')
    search_fields = ('username', 'email')
    fieldsets = UserAdmin.fieldsets + (
        ('Profil CatchClub', {'fields': ('bio',)}),
    )

    @admin.display(description='Abonnés')
    def nb_abonnes_admin(self, obj):
        return obj.nb_abonnes

    @admin.display(description='Abonnements')
    def nb_abonnements_admin(self, obj):
        return obj.nb_abonnements


@admin.register(Pokemone)
class PokemoneAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type', 'modele_3d', 'dresseur', 'points_de_vie', 'date_creation')
    list_filter = ('type', 'modele_3d')
    search_fields = ('nom', 'dresseur__username')
