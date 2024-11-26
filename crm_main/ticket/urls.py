from django.urls import path
from . import views
# from django.conf import settings
# from django.conf.urls.static import static

app_name = 'tickets'

urlpatterns = [
    path('', views.TicketListView.as_view(), name='list'),
    path('<int:pk>/', views.TicketDetailView.as_view(), name='detail'),
    path('create/', views.TicketCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.TicketUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.TicketDeleteView.as_view(), name='delete'),
    path('<int:pk>/add-comment/', views.AddCommentView.as_view(), name='add_comment'),
    path('add-ticket/', views.TicketCreateView.as_view(), name='add_ticket'),
]
