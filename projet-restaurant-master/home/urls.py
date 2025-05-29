from django.contrib import admin
from django.urls import path, include
from home import views 

urlpatterns = [
    path('page', views.home, name='home'),
    path('commander', views.commander, name='commander'),
    path('submit-order/', views.submit_order, name='submit_order'),  # Add this line
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),  # Add this line
    path('historique/', views.order_history, name='order_history'),  # Add this line
]