from django.urls import path
from .views import (
    ajouter_au_panier,
    voir_panier,
    augmenter_quantite,
    diminuer_quantite,
    supprimer_du_panier,
    vider_panier,
    passer_commande,
    mes_commandes,
    detail_commande,
)

app_name = 'commandes'

urlpatterns = [
    # Panier
    path('panier/', voir_panier, name='voir_panier'),
    path('panier/ajouter/<int:produit_id>/', ajouter_au_panier, name='ajouter_au_panier'),
    path('panier/augmenter/<int:ligne_id>/', augmenter_quantite, name='augmenter_quantite'),
    path('panier/diminuer/<int:ligne_id>/', diminuer_quantite, name='diminuer_quantite'),
    path('panier/supprimer/<int:ligne_id>/', supprimer_du_panier, name='supprimer_du_panier'),
    path('panier/vider/', vider_panier, name='vider_panier'),

    # Commandes
    path('passer-commande/', passer_commande, name='passer_commande'),
    path('mes-commandes/', mes_commandes, name='mes_commandes'),
    path('mes-commandes/<int:commande_id>/', detail_commande, name='detail_commande'),
]