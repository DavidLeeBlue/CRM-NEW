from django.urls import path
from . import views

urlpatterns = [
    # path('', views.leads_list, name='leads_list'),
    path('', views.LeadListView.as_view(), name='leads_list'),
    path('<int:pk>/', views.LeadDetailView.as_view(), name='leads_detail'),
    path('<int:pk>/delete/', views.LeadDeleteView.as_view(), name='leads_delete'),
    path('<int:pk>/edit/', views.LeadUpdateView.as_view(), name='leads_edit'),
    # path('<int:pk>/convert/', views.ConvertToClientView.as_view(), name='leads_convert'),
    path('<int:pk>/convert/', views.ConvertToClientView.as_view(), name='leads_convert'),
    path('add-lead/', views.LeadCreateView.as_view(), name='add_lead'),
]


