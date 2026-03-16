from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Produit
from .forms import ProduitForm
from commandes.models import Commande


def catalogue(request):
    produits = Produit.objects.filter(disponible=True)
    return render(request, 'produits/catalogue.html', {'produits': produits})


def detail_produit(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    return render(request, 'produits/detail_produit.html', {'produit': produit})


@login_required
def dashboard_agriculteur(request):
    # Vérifier que l'utilisateur est bien agriculteur
    if not request.user.est_agriculteur():
        messages.error(request, "Accès refusé. Cette page est réservée aux agriculteurs.")
        return redirect('accueil')

    # Produits de l'agriculteur connecté
    produits = Produit.objects.filter(agriculteur=request.user)

    # Commandes reçues sur ses produits
    commandes_recues = Commande.objects.filter(
        items__produit__agriculteur=request.user
    ).distinct().order_by('-date_commande')

    context = {
        'produits': produits,
        'total_produits': produits.count(),
        'produits_disponibles': produits.filter(disponible=True).count(),
        'produits_indisponibles': produits.filter(disponible=False).count(),
        'commandes_recues': commandes_recues,
        'total_commandes': commandes_recues.count(),
    }

    return render(request, 'produits/dashboard_agriculteur.html', context)


@login_required
def tableau_bord(request):
    # Redirection propre vers le seul dashboard qu’on garde
    return redirect('dashboard_agriculteur')


@login_required
def ajouter_produit(request):
    if not request.user.est_agriculteur():
        messages.error(request, "Seuls les agriculteurs peuvent ajouter des produits.")
        return redirect('accueil')

    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            produit = form.save(commit=False)
            produit.agriculteur = request.user
            produit.save()
            messages.success(request, "Produit ajouté avec succès !")
            return redirect('dashboard_agriculteur')
    else:
        form = ProduitForm()

    return render(request, 'produits/form_produit.html', {
        'form': form,
        'titre': 'Ajouter un produit'
    })


@login_required
def modifier_produit(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id, agriculteur=request.user)

    if not request.user.est_agriculteur():
        messages.error(request, "Accès refusé.")
        return redirect('accueil')

    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES, instance=produit)
        if form.is_valid():
            form.save()
            messages.success(request, "Produit modifié avec succès !")
            return redirect('dashboard_agriculteur')
    else:
        form = ProduitForm(instance=produit)

    return render(request, 'produits/form_produit.html', {
        'form': form,
        'titre': 'Modifier le produit'
    })


@login_required
def supprimer_produit(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id, agriculteur=request.user)

    if not request.user.est_agriculteur():
        messages.error(request, "Accès refusé.")
        return redirect('accueil')

    if request.method == 'POST':
        produit.delete()
        messages.success(request, "Produit supprimé avec succès !")
        return redirect('dashboard_agriculteur')

    return render(request, 'produits/confirmer_suppression.html', {'produit': produit})