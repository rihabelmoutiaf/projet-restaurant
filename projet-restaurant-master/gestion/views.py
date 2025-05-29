from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
from .models import Commande, Plat, Table, Serveur, Client


def commander(request):
    """Page pour passer une commande"""
    plats = Plat.objects.all().order_by('type', 'nom')
    tables = Table.objects.all()
    serveurs = Serveur.objects.all()
    
    # Organiser les plats par type
    plats_par_type = {
        'entree': plats.filter(type='entree'),
        'plat': plats.filter(type='plat'), 
        'dessert': plats.filter(type='dessert'),
        'boisson': plats.filter(type='boisson'),
    }
    
    context = {
        'plats_par_type': plats_par_type,
        'tables': tables,
        'serveurs': serveurs,
    }
    return render(request, 'commander.html', context)


def passer_commande(request):
    """Traiter une nouvelle commande"""
    if request.method == 'POST':
        try:
            # Récupérer les données du formulaire
            table_id = request.POST.get('table')
            serveur_id = request.POST.get('serveur')
            client_nom = request.POST.get('client_nom', '').strip()
            client_prenom = request.POST.get('client_prenom', '').strip()
            client_telephone = request.POST.get('client_telephone', '').strip()
            notes = request.POST.get('notes', '').strip()
            
            # Récupérer les plats commandés (format: plat_id_quantity)
            plats_commandes = []
            montant_total = 0
            
            for key, value in request.POST.items():
                if key.startswith('plat_') and key.endswith('_quantity'):
                    plat_id = key.replace('plat_', '').replace('_quantity', '')
                    quantity = int(value) if value and int(value) > 0 else 0
                    
                    if quantity > 0:
                        plat = get_object_or_404(Plat, id=plat_id)
                        plats_commandes.append({
                            'plat': plat,
                            'quantity': quantity,
                            'sous_total': plat.prix * quantity
                        })
                        montant_total += plat.prix * quantity
            
            if not plats_commandes:
                messages.error(request, 'Veuillez sélectionner au moins un plat.')
                return redirect('commander')
            
            # Créer ou récupérer le client
            client = None
            if client_nom and client_prenom:
                client, created = Client.objects.get_or_create(
                    nom=client_nom,
                    prenom=client_prenom,
                    defaults={'telephone': client_telephone}
                )
                if not created and client_telephone:
                    client.telephone = client_telephone
                    client.save()
            
            # Récupérer la table et le serveur
            table = get_object_or_404(Table, id=table_id) if table_id else None
            serveur = get_object_or_404(Serveur, id=serveur_id) if serveur_id else None
            
            # Créer la commande
            commande = Commande.objects.create(
                table=table,
                serveur=serveur,
                client=client,
                montant_total=montant_total,
                notes=notes,
                statut='en_cours'
            )
            
            # Stocker les détails de la commande dans les notes (solution simple)
            details_commande = []
            for item in plats_commandes:
                details_commande.append(f"{item['plat'].nom} x{item['quantity']} = {item['sous_total']} MAD")
            
            commande.notes = f"Détails:\n" + "\n".join(details_commande)
            if notes:
                commande.notes += f"\n\nNotes additionnelles: {notes}"
            commande.save()
            
            messages.success(request, f'Commande #{commande.id} passée avec succès! Montant total: {montant_total} MAD')
            return redirect('historique_commandes')
            
        except Exception as e:
            messages.error(request, f'Erreur lors de la création de la commande: {str(e)}')
            return redirect('commander')
    
    return redirect('commander')


def historique_commandes(request):
    """Page pour afficher l'historique des commandes"""
    commandes = Commande.objects.all().order_by('-date_commande')
    
    # Filtrage par statut si demandé
    statut_filtre = request.GET.get('statut')
    if statut_filtre and statut_filtre != 'tous':
        commandes = commandes.filter(statut=statut_filtre)
    
    context = {
        'commandes': commandes,
        'statut_filtre': statut_filtre,
        'statuts': Commande.STATUT_CHOICES,
    }
    return render(request, 'historique_commandes.html', context)


def detail_commande(request, commande_id):
    """Afficher les détails d'une commande"""
    commande = get_object_or_404(Commande, id=commande_id)
    context = {
        'commande': commande,
    }
    return render(request, 'detail_commande.html', context)


def modifier_statut_commande(request, commande_id):
    """Modifier le statut d'une commande"""
    if request.method == 'POST':
        commande = get_object_or_404(Commande, id=commande_id)
        nouveau_statut = request.POST.get('statut')
        
        if nouveau_statut in dict(Commande.STATUT_CHOICES):
            commande.statut = nouveau_statut
            commande.save()
            messages.success(request, f'Statut de la commande #{commande.id} mis à jour.')
        else:
            messages.error(request, 'Statut invalide.')
    
    return redirect('historique_commandes')