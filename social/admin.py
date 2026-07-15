from django.contrib import admin
from .models import Post, Commentaire, Abonnement


class CommentaireInline(admin.TabularInline):
    model = Commentaire
    extra = 0
    readonly_fields = ('auteur', 'contenu', 'date_publication')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('auteur', 'contenu_court', 'nb_likes', 'nb_commentaires', 'date_publication')
    list_filter = ('date_publication',)
    search_fields = ('contenu', 'auteur__username')
    inlines = [CommentaireInline]

    @admin.display(description='Contenu')
    def contenu_court(self, obj):
        return obj.contenu[:60]


@admin.register(Abonnement)
class AbonnementAdmin(admin.ModelAdmin):
    """
    Gestion des abonnés par l'administrateur.

    L'admin (superutilisateur, ou tout membre du groupe "Modérateurs" créé
    par la commande seed_demo) a ici un droit complet sur les relations
    d'abonnement : consultation de qui suit qui, suppression individuelle
    ou en masse (modération d'un abonnement abusif), recherche par dresseur.
    """
    list_display = ('suiveur', 'suivi', 'date_abonnement')
    list_filter = ('date_abonnement',)
    search_fields = ('suiveur__username', 'suivi__username')
    autocomplete_fields = ('suiveur', 'suivi')
    actions = ['forcer_desabonnement']

    @admin.action(description="Forcer la suppression des abonnements sélectionnés (modération)")
    def forcer_desabonnement(self, request, queryset):
        nb = queryset.count()
        queryset.delete()
        self.message_user(request, f"{nb} abonnement(s) supprimé(s).")


@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ('auteur', 'post', 'contenu', 'date_publication')
    search_fields = ('contenu', 'auteur__username')
