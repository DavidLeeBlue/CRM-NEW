from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.orders_list, name='list'),
    path('<int:pk>/', views.order_detail, name='detail'), #optimize the name here.
    path('add/', views.order_add, name='add'), # changed orders_add to order_add
    path('<int:pk>/delete/', views.orders_delete, name='delete'),
    path('<int:pk>/edit/', views.orders_edit, name='edit'),
]