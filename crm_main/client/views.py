from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Client

# Create your views here.

@login_required
def clients_list(request):
    clients = Client.objects.filter(created_by=request.user)
    # clients = get_object_or_404(Client, created_by=request.user)
    return render(request, 'client/clients_list.html',{ 'clients': clients })

@login_required
def client_detail(request, pk):
    client = get_object_or_404(Client,created_by=request.user, pk=pk)
    return render(request, 'client/clients_detail.html', {'client': client})
