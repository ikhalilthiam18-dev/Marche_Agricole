from django.contrib.auth.models import AbstractUser
from django.db import models


class Utilisateur(AbstractUser):
    TYPE_CHOICES = (
        ('agriculteur', 'Agriculteur'),
        ('client', 'Client'),
    )

    type_utilisateur = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='client'
    )

    telephone = models.CharField(max_length=20, blank=True, null=True)

    def est_agriculteur(self):
        return self.type_utilisateur == 'agriculteur'

    def est_client(self):
        return self.type_utilisateur == 'client'

    def __str__(self):
        return self.username