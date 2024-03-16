from django.urls import path
from . import views

urlpatterns = [
    path('', views.products_list, name='products_list'),
    path('<int:pk>/', views.products_detail, name='products_detail'),
    path('<int:pk>/delete/', views.products_delete, name='products_delete'),
    # path('<int:pk>/edit/', views.products_edit, name='products_edit'),
    # path('<int:pk>/convert/', views.convert_to_client, name='products_convert'),
    # path('add-lead/', views.add_lead, name='add_lead'),
]