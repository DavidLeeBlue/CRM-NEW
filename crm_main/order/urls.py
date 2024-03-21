from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.OrderListView.as_view(), name='list'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='detail'), #optimize the name here.
    path('add-order/', views.OrderCreateView.as_view(), name='add_order'), # changed orders_add to order_add
    path('<int:pk>/delete/', views.OrderDeleteView.as_view(), name='delete'),
    path('<int:pk>/edit/', views.OrderUpdateView.as_view(), name='edit'),
    path('<int:pk>/add-product/', views.AddProductView.as_view(), name='add_product'),
]
