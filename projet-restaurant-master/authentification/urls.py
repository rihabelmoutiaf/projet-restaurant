from django.contrib import admin
from django.urls import path,include
from authentification import views 

urlpatterns = [
  path('login', views.auth, name='auth'),
  
  
]