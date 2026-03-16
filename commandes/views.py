from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Panier, PanierItem, Commande, CommandeItem
from produits.models import Produit


@login_required
def voir_panier(request):
    panier, created = Panier.objects.get_or_create(utilisateur=request.user)
    items = panier.items.all()

    return render(request, 'commandes/panier.html', {
        'panier': panier,
        'items': items
    })


@login_required
def ajouter_au_panier(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id, disponible=True)
    panier, created = Panier.objects.get_or_create(utilisateur=request.user)

    item, created = PanierItem.objects.get_or_create(
        panier=panier,
        produit=produit,
        defaults={'quantite': 1}
    )

    if not created:
        item.quantite += 1
        item.save()

    messages.success(request, f"{produit.nom} a été ajouté au panier.")
    return redirect('commandes:voir_panier')


@login_required
def augmenter_quantite(request, ligne_id):
    item = get_object_or_404(PanierItem, id=ligne_id, panier__utilisateur=request.user)

    # Vérifier le stock
    if item.quantite < item.produit.quantite_stock:
        item.quantite += 1
        item.save()
        messages.success(request, "Quantité augmentée.")
    else:
        messages.warning(request, "Stock insuffisant.")

    return redirect('commandes:voir_panier')


@login_required
def diminuer_quantite(request, ligne_id):
    item = get_object_or_404(PanierItem, id=ligne_id, panier__utilisateur=request.user)

    if item.quantite > 1:
        item.quantite -= 1
        item.save()
        messages.success(request, "Quantité diminuée.")
    else:
        item.delete()
        messages.info(request, "Produit retiré du panier.")

    return redirect('commandes:voir_panier')


@login_required
def supprimer_du_panier(request, ligne_id):
    item = get_object_or_404(PanierItem, id=ligne_id, panier__utilisateur=request.user)
    item.delete()
    messages.success(request, "Produit supprimé du panier.")
    return redirect('commandes:voir_panier')


@login_required
def vider_panier(request):
    panier, created = Panier.objects.get_or_create(utilisateur=request.user)
    panier.items.all().delete()
    messages.success(request, "Le panier a été vidé.")
    return redirect('commandes:voir_panier')


@login_required
def passer_commande(request):
    panier, created = Panier.objects.get_or_create(utilisateur=request.user)
    items = panier.items.all()

    if not items.exists():
        messages.warning(request, "Votre panier est vide.")
        return redirect('commandes:voir_panier')

    # Vérification du stock avant commande
    for item in items:
        if item.quantite > item.produit.quantite_stock:
            messages.error(
                request,
                f"Stock insuffisant pour {item.produit.nom}. Stock disponible : {item.produit.quantite_stock}"
            )
            return redirect('commandes:voir_panier')

    # Créer la commande
    commande = Commande.objects.create(
        client=request.user,
        statut='en_attente',
        mode_paiement='cash_on_delivery',
        statut_paiement='en_attente',
    )

    total = 0

    # Créer les lignes de commande + diminuer le stock
    for item in items:
        CommandeItem.objects.create(
            commande=commande,
            produit=item.produit,
            quantite=item.quantite,
            prix_unitaire=item.produit.prix
        )

        # Mise à jour stock
        item.produit.quantite_stock -= item.quantite
        if item.produit.quantite_stock <= 0:
            item.produit.quantite_stock = 0
            item.produit.disponible = False
        item.produit.save()

        total += item.produit.prix * item.quantite

    commande.total = total
    commande.save()

    # Vider le panier
    items.delete()

    messages.success(request, "Commande passée avec succès.")
    return redirect('commandes:mes_commandes')


@login_required
def mes_commandes(request):
    commandes = Commande.objects.filter(client=request.user).order_by('-date_commande')
    return render(request, 'commandes/mes_commandes.html', {
        'commandes': commandes
    })


@login_required
def detail_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id, client=request.user)
    return render(request, 'commandes/detail_commande.html', {
        'commande': commande
    })