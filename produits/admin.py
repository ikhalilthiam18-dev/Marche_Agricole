from django.contrib import admin
from .models import Produit

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix', 'quantite_stock', 'agriculteur', 'disponible', 'date_creation')
    list_filter = ('disponible', 'date_creation')
    search_fields = ('nom', 'description')