from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Client
from .forms import AddClientForm
from django.contrib import messages

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


@login_required
def client_add(request):
    if request.method == 'POST':
        form = AddClientForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False) # don't save the form yet, need to add created_by
            lead.created_by = request.user
            lead.save()
            messages.success(request, 'The lead has been added successfully!')
            return redirect('clients_list')
    else:
        form = AddClientForm()
    return render(request, 'client/clients_add.html',{
        'form': form
    }) # one slash here.