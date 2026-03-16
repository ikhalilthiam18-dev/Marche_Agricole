from django.urls import path
from . import views

urlpatterns = [
    # Catalogue client
    path('', views.catalogue, name='catalogue'),
    path('detail/<int:produit_id>/', views.detail_produit, name='detail_produit'),

    # Dashboard agriculteur (CRUD visible ici)
    path('dashboard/', views.dashboard_agriculteur, name='dashboard_agriculteur'),

    # Ancienne route conservée pour compatibilité -> redirige vers dashboard
    path('tableau-bord/', views.tableau_bord, name='tableau_bord'),

    # CRUD produits
    path('ajouter/', views.ajouter_produit, name='ajouter_produit'),
    path('modifier/<int:produit_id>/', views.modifier_produit, name='modifier_produit'),
    path('supprimer/<int:produit_id>/', views.supprimer_produit, name='supprimer_produit'),
]