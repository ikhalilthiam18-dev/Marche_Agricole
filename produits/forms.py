from django import forms
from .models import Produit


class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom', 'description', 'prix', 'quantite_stock', 'disponible', 'image']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Tomates fraîches'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Décrivez votre produit...'}),
            'prix': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 1500'}),
            'quantite_stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 25'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }