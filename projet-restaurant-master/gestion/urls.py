from django.urls import path
from . import views

urlpatterns = [
    path('commander/', views.commander, name='commander'),
    path('passer-commande/', views.passer_commande, name='passer_commande'),
    path('historique/', views.historique_commandes, name='historique_commandes'),
    path('commande/<int:commande_id>/', views.detail_commande, name='detail_commande'),
    path('modifier-statut/<int:commande_id>/', views.modifier_statut_commande, name='modifier_statut_commande'),
]