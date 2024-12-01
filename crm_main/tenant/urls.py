from django.urls import path
from . import views

app_name = 'tenant'

urlpatterns = [
    path('', views.TenantListView.as_view(), name='list'),
    path('<int:pk>/', views.TenantDetailView.as_view(), name='detail'),
    path('create/', views.TenantCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.TenantUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.TenantDeleteView.as_view(), name='delete'),
]