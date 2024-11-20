from django.urls import path
from . import views

app_name = 'tickets'

urlpatterns = [
    path('', views.TicketListView.as_view(), name='list'),
    path('<int:pk>/', views.TicketDetailView.as_view(), name='detail'),
    path('<int:pk>/delete/', views.TicketDeleteView.as_view(), name='delete'),
    path('<int:pk>/edit/', views.TicketUpdateView.as_view(), name='edit'),
    path('<int:pk>/add-comment/', views.CommentCreateView.as_view(), name='add_comment'),
    path('add-ticket/', views.TicketCreateView.as_view(), name='add_ticket'),
]