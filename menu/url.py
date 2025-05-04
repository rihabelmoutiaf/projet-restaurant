from django.contrib import admin
from django.urls import path, include
from menu import views 


urlpatterns = [
  path('page', views.menu, name='menu'),
  path('about', views.about, name='about'),
]
