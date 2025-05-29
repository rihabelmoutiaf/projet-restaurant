from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from gestion.models import Commande, Client, Table, Serveur, Plat
from django.utils import timezone

def home(request):   
    return render(request, 'home.html')

def commander(request):   
    return render(request, 'commander.html')

def submit_order(request):
    """Handle order submission from the commander form"""
    if request.method == 'POST':
        try:
            # Get form data
            entrees = request.POST.get('entrées')
            entrees_quantity = int(request.POST.get('entrées-quantity', 0))
            
            plats = request.POST.get('plats')
            plats_quantity = int(request.POST.get('plats-quantity', 0))
            
            desserts = request.POST.get('desserts')
            desserts_quantity = int(request.POST.get('desserts-quantity', 0))
            
            boissons = request.POST.get('boissons')
            boissons_quantity = int(request.POST.get('boissons-quantity', 0))
            
            # Customer information
            name = request.POST.get('name', '').strip()
            phone = request.POST.get('phone', '').strip()
            reservation_datetime = request.POST.get('reservation-datetime')
            
            # Split name into first and last name
            name_parts = name.split(' ', 1)
            prenom = name_parts[0] if name_parts else ''
            nom = name_parts[1] if len(name_parts) > 1 else ''
            
            # Create or get client
            client = None
            if prenom and nom:
                client, created = Client.objects.get_or_create(
                    nom=nom,
                    prenom=prenom,
                    defaults={'telephone': phone}
                )
                if not created and phone:
                    client.telephone = phone
                    client.save()
            
            # Calculate total amount and build order details
            total_amount = 0
            order_details = []
            
            # Define prices (matching your menu)
            prices = {
                'Foie Gras Maison': 264,
                'Tartare de Saumon': 198,
                'Soupe à l\'Oignon Gratinée': 132,
                'Filet de Boeuf Rossini': 418,
                'Risotto aux Champignons Sauvages': 286,
                'Dos de Bar en Croûte de Sel': 352,
                'Soufflé Grand Marnier': 154,
                'Chocolat Fondant': 132,
                'Assiette de Fromages Affinés': 176,
                'Vin Rouge Château Bordeaux': 120,
                'Vin Blanc Chardonnay': 110,
                'Eau Minérale': 25,
                'Café Espresso': 35
            }
            
            # Add items to order
            if entrees_quantity > 0:
                price = prices.get(entrees, 0)
                subtotal = price * entrees_quantity
                total_amount += subtotal
                order_details.append(f"Entrée: {entrees} x{entrees_quantity} = {subtotal} MAD")
            
            if plats_quantity > 0:
                price = prices.get(plats, 0)
                subtotal = price * plats_quantity
                total_amount += subtotal
                order_details.append(f"Plat: {plats} x{plats_quantity} = {subtotal} MAD")
            
            if desserts_quantity > 0:
                price = prices.get(desserts, 0)
                subtotal = price * desserts_quantity
                total_amount += subtotal
                order_details.append(f"Dessert: {desserts} x{desserts_quantity} = {subtotal} MAD")
            
            if boissons_quantity > 0:
                price = prices.get(boissons, 0)
                subtotal = price * boissons_quantity
                total_amount += subtotal
                order_details.append(f"Boisson: {boissons} x{boissons_quantity} = {subtotal} MAD")
            
            # Get a default table and server (you can modify this logic)
            table = Table.objects.first()  # Gets the first available table
            serveur = Serveur.objects.first()  # Gets the first available server
            
            # Create the order
            commande = Commande.objects.create(
                table=table,
                serveur=serveur,
                client=client,
                montant_total=total_amount,
                statut='en_cours'
            )
            
            # Add order details to notes
            notes_content = "Détails de la commande:\n" + "\n".join(order_details)
            if reservation_datetime:
                notes_content += f"\n\nRéservation: {reservation_datetime}"
            
            commande.notes = notes_content
            commande.save()
            
            # Success message
            messages.success(request, f'Commande #{commande.id} passée avec succès! Montant total: {total_amount} MAD')
            return redirect('order_success', order_id=commande.id)
            
        except Exception as e:
            messages.error(request, f'Erreur lors de la création de la commande: {str(e)}')
            return redirect('commander')
    
    # If not POST, redirect to commander page
    return redirect('commander')

def order_success(request, order_id):
    """Display order confirmation page"""
    try:
        commande = Commande.objects.get(id=order_id)
        context = {
            'commande': commande,
        }
        return render(request, 'order_success.html', context)
    except Commande.DoesNotExist:
        messages.error(request, 'Commande introuvable.')
        return redirect('commander')

def order_history(request):
    """Display order history"""
    commandes = Commande.objects.all().order_by('-date_commande')
    context = {
        'commandes': commandes,
    }
    return render(request, 'order_history.html', context)