from django.db import models
from django.conf import settings
from django.utils import timezone
from produits.models import Produit


class Panier(models.Model):
    utilisateur = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='panier'
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Panier"
        verbose_name_plural = "Paniers"

    def __str__(self):
        return f"Panier de {self.utilisateur.username}"

    def total_panier(self):
        return sum(item.sous_total() for item in self.items.all())


class PanierItem(models.Model):
    panier = models.ForeignKey(
        Panier,
        on_delete=models.CASCADE,
        related_name='items'
    )
    produit = models.ForeignKey(
        Produit,
        on_delete=models.CASCADE,
        related_name='panier_items'
    )
    quantite = models.PositiveIntegerField(default=1)
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Article du panier"
        verbose_name_plural = "Articles du panier"
        unique_together = ('panier', 'produit')

    def __str__(self):
        return f"{self.produit.nom} x {self.quantite}"

    def sous_total(self):
        return self.produit.prix * self.quantite


class Commande(models.Model):
    STATUT_CHOICES = (
        ('en_attente', 'En attente'),
        ('confirmee', 'Confirmée'),
        ('expediee', 'Expédiée'),
        ('livree', 'Livrée'),
        ('annulee', 'Annulée'),
    )

    MODE_PAIEMENT_CHOICES = (
        ('wave', 'Wave'),
        ('orange_money', 'Orange Money'),
        ('cash_on_delivery', 'Paiement à la livraison'),
    )

    STATUT_PAIEMENT_CHOICES = (
        ('en_attente', 'En attente'),
        ('paye', 'Payé'),
        ('echoue', 'Échoué'),
    )

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='commandes'
    )

    date_commande = models.DateTimeField(default=timezone.now)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    mode_paiement = models.CharField(
        max_length=30,
        choices=MODE_PAIEMENT_CHOICES,
        default='cash_on_delivery'
    )

    statut_paiement = models.CharField(
        max_length=20,
        choices=STATUT_PAIEMENT_CHOICES,
        default='en_attente'
    )

    reference_paiement = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['-date_commande']
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"

    def __str__(self):
        return f"Commande #{self.id} - {self.client.username}"

    def calculer_total(self):
        total = sum(item.sous_total() for item in self.items.all())
        self.total = total
        self.save()
        return total


class CommandeItem(models.Model):
    commande = models.ForeignKey(
        Commande,
        on_delete=models.CASCADE,
        related_name='items'
    )
    produit = models.ForeignKey(
        Produit,
        on_delete=models.CASCADE,
        related_name='commande_items'
    )
    quantite = models.PositiveIntegerField(default=1)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Ligne de commande"
        verbose_name_plural = "Lignes de commande"

    def __str__(self):
        return f"{self.produit.nom} x {self.quantite}"

    def sous_total(self):
        return self.prix_unitaire * self.quantite