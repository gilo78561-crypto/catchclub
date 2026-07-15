from django.contrib import admin
from .models import Groupe, Adhesion


class AdhesionInline(admin.TabularInline):
    model = Adhesion
    extra = 0


@admin.register(Groupe)
class GroupeAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type', 'prive', 'nb_membres', 'date_creation')
    list_filter = ('type', 'prive')
    search_fields = ('nom',)
    inlines = [AdhesionInline]


@admin.register(Adhesion)
class AdhesionAdmin(admin.ModelAdmin):
    list_display = ('dresseur', 'groupe', 'date_adhesion')
    search_fields = ('dresseur__username', 'groupe__nom')
