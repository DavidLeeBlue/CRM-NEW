from django.urls import path
from . import views

urlpatterns = [
    path('', views.orders_list, name='orders_list'),
    # path('<int:pk>/', views.client_detail, name='clients_detail'),
    # path('<int:pk>/delete/', views.clients_delete, name='clients_delete'),
    # path('<int:pk>/edit/', views.clients_edit, name='clients_edit'),
    # path('add/', views.client_add, name='clients_add'),
]