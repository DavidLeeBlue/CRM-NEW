from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('', views.clients_list, name='list'),
    path('<int:pk>/', views.client_detail, name='detail'),
    path('<int:pk>/delete/', views.clients_delete, name='delete'),
    path('<int:pk>/edit/', views.clients_edit, name='edit'),
    path('add/', views.client_add, name='add'),
]