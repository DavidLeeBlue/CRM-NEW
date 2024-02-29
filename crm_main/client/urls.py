from django.urls import path
from . import views

urlpatterns = [
    path('', views.clients_list, name='clients_list'),
    path('<int:pk>/', views.client_detail, name='clients_detail'),
    path('<int:pk>/delete/', views.clients_delete, name='clients_delete'),
    path('add/', views.client_add, name='clients_add'),
]