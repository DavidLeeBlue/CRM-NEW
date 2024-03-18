from django.urls import path
from . import views

urlpatterns = [
    path('', views.orders_list, name='orders_list'),
    path('<int:pk>/', views.order_detail, name='orders_detail'), #optimize the name here.
    # path('<int:pk>/delete/', views.orders_delete, name='orders_delete'),
    # path('<int:pk>/edit/', views.orders_edit, name='orders_edit'),
    # path('add/', views.order_add, name='orders_add'),
]