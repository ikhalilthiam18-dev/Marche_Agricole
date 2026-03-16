from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import InscriptionForm, ConnexionForm


def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            utilisateur = form.save()
            login(request, utilisateur)
            messages.success(request, "Inscription réussie ! Bienvenue sur Marché Agricole.")
            return redirect('catalogue')
    else:
        form = InscriptionForm()

    return render(request, 'utilisateurs/inscription.html', {'form': form})


def connexion(request):
    if request.method == 'POST':
        next_url = request.POST.get('next', 'catalogue')
        form = ConnexionForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            utilisateur = authenticate(request, username=username, password=password)

            if utilisateur is not None:
                login(request, utilisateur)
                messages.success(request, f"Bienvenue {utilisateur.username} !")
                return redirect(next_url)
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        next_url = request.GET.get('next', 'catalogue')
        form = ConnexionForm()

    return render(request, 'utilisateurs/connexion.html', {
        'form': form,
        'next': next_url
    })


def deconnexion(request):
    logout(request)
    messages.info(request, "Vous êtes déconnecté.")
    return redirect('catalogue')