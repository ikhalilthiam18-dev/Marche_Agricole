from django.contrib import admin
from .models import Panier, PanierItem, Commande, CommandeItem


class PanierItemInline(admin.TabularInline):
    model = PanierItem
    extra = 0


@admin.register(Panier)
class PanierAdmin(admin.ModelAdmin):
    list_display = ('id', 'utilisateur', 'date_creation')
    inlines = [PanierItemInline]


class CommandeItemInline(admin.TabularInline):
    model = CommandeItem
    extra = 0


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'client',
        'date_commande',
        'statut',
        'mode_paiement',
        'statut_paiement',
        'total'
    )
    list_filter = ('statut', 'mode_paiement', 'statut_paiement', 'date_commande')
    search_fields = ('client__username', 'reference_paiement')
    inlines = [CommandeItemInline]


admin.site.register(PanierItem)
admin.site.register(CommandeItem)