from django.contrib import admin
from .models import  Client, Table, Serveur, Plat, Commande

admin.site.register(Client)
admin.site.register(Table)
admin.site.register(Serveur)
admin.site.register(Plat)
admin.site.register(Commande)

