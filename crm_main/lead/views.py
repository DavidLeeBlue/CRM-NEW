from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.decorators import login_required
from .forms import AddLeadForm
from .models import Lead


@login_required
def leads_list(request):
    leads_list = Lead.objects.filter(created_by=request.user)
    return render(request, 'lead/leads_list.html')


@login_required
def add_lead(request):
    if request.method == 'POST':
        form = AddLeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False) # don't save the form yet, we need to add created_by
            lead.created_by = request.user
            lead.save()
            return redirect('/dashboard')
    else:
        form = AddLeadForm()
    return render(request, 'lead/add_lead.html',{
        'form': form
    }) # one slash here.