from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Client

# Create your views here.

@login_required
def clients_list(request):
    clients = Client.objects.filter(created_by=request.user)
    return render(request, 'client/clients_list.html',{ 'clients': clients })
