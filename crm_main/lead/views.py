from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.contrib.auth.decorators import login_required
from .forms import AddLeadForm
from .models import Lead
from django.contrib import messages


@login_required
def leads_list(request):
    leads = Lead.objects.filter(created_by=request.user)
    return render(request, 'lead/leads_list.html',{
        'leads': leads
    })

@login_required
def leads_detail(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user,pk=pk)
    # lead = Lead.objects.filter(created_by=request.user).get(pk = pk)
    return render(request,'lead/leads_detail.html',{
        'lead':lead
    })

@login_required
def leads_delete(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user,pk=pk)
    lead.delete()
    messages.success(request, 'The lead has been deleted successfully!')
    # return redirect('/dashboard/leads')
    return redirect('leads_list')

@login_required
def leads_edit(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user,pk=pk)
    if request.method == 'POST':
        form = AddLeadForm(request.POST, instance=lead)
        if form.is_valid():
            lead.save()
            # messages.success(request, lead.name . ' The lead has been edited successfully!')
            messages.success(request, lead.name + ' The lead has been edited successfully!')
            return redirect('leads_list')
    else:
        form = AddLeadForm(instance=lead)
    return render(request, 'lead/leads_edit.html',{
        'form': form
    }) # one slash here.


@login_required
def add_lead(request):
    if request.method == 'POST':
        form = AddLeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False) # don't save the form yet, need to add created_by
            lead.created_by = request.user
            lead.save()
            messages.success(request, 'The lead has been added successfully!')
            return redirect('leads_list')
    else:
        form = AddLeadForm()
    return render(request, 'lead/add_lead.html',{
        'form': form
    }) # one slash here.