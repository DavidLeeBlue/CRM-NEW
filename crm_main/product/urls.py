from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.products_list, name='list'),
    path('<int:pk>/', views.products_detail, name='detail'),
    path('<int:pk>/delete/', views.products_delete, name='delete'),
    path('<int:pk>/edit/', views.products_edit, name='edit'),
    path('add/', views.products_add, name='add'),
]
# 