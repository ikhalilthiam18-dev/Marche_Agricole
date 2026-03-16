from django.shortcuts import render
from produits.models import Produit

def accueil(request):
    produits_recents = Produit.objects.all().order_by('-id')[:6]
    return render(request, 'accueil.html', {
        'produits_recents': produits_recents
    })