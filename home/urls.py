from django.contrib import admin
from django.urls import path,include
from home import views 

urlpatterns = [
  path('page', views.home, name='home'),
  path('commander', views.commander, name='commander'),
  
]
