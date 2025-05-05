from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)  

    def __str__(self):
        return f"{self.prenom} {self.nom}"

class Table(models.Model):
    numero = models.IntegerField(unique=True)
    capacite = models.IntegerField()

    def __str__(self):
        return f"Table {self.numero} (Capacité: {self.capacite})"

class Serveur(models.Model):
    email = models.CharField(max_length=255, unique=True)
    mot_de_passe = models.CharField(max_length=255)
    tables_assignees = models.CharField(max_length=255, blank=True, null=True)
    administrateur = models.ForeignKey(
        User,  
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        limit_choices_to={'is_superuser': True} 
    )

    def __str__(self):
        return self.email

class Plat(models.Model):
    TYPE_CHOICES = [
        ('entree', 'Entrée'),
        ('plat', 'Plat Principal'),
        ('dessert', 'Dessert'),
        ('boisson', 'Boisson'),
    ]

    nom = models.CharField(max_length=100)  
    description = models.TextField(blank=True, null=True)  
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES,
        blank=True,
        null=True
    )  

    def __str__(self):
        return self.nom

class Commande(models.Model):
    STATUT_CHOICES = [
        ('en_cours', 'En Cours'),
        ('servie', 'Servie'),
        ('payee', 'Payée'),
        ('annulee', 'Annulée'),
    ]
    
    table = models.ForeignKey('Table', on_delete=models.SET_NULL, null=True)
    serveur = models.ForeignKey('Serveur', on_delete=models.SET_NULL, null=True)
    client = models.ForeignKey('Client', on_delete=models.SET_NULL, blank=True, null=True)
    date_commande = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_cours')
    notes = models.TextField(blank=True, null=True)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Commande #{self.id} - Table {self.table.numero if self.table else '?'}"