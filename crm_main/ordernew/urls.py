from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('<int:pk>/', views.order_detailnew, name='orders_detailnew'), #optimize the name here.
    path('create/', views.order_create, name='order_create'), # changed orders_add to order_add
    # path('<int:pk>/delete/', views.orders_delete, name='orders_delete'),
    path('<int:pk>/update/', views.order_update, name='order_update'),
]