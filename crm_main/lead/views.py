from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.contrib.auth.decorators import login_required
# from .forms import AddLeadForm
from .models import Lead
from django.contrib import messages
from client.models import Client
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views import View

class LeadListView(ListView):
    model = Lead
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LeadListView, self).dispatch(*args, **kwargs)

    def get_queryset(self): # this is the method that is called when the view is loaded, it returns the queryset that is used to populate the list of leads.
        queryset = super(LeadListView,self).get_queryset()
        return queryset.filter(created_by=self.request.user, converted_to_client=False)


class LeadDetailView(DetailView):
    model = Lead
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = super(LeadDetailView, self).get_queryset()
        # team = self.request.user.userprofile.active_team

        # return queryset.filter(team=team, pk=self.kwargs.get('pk'))
        return queryset.filter(pk=self.kwargs.get('pk'))

# @login_required
# def leads_detail(request, pk):
#     lead = get_object_or_404(Lead, created_by=request.user,pk=pk)
#     # lead = Lead.objects.filter(created_by=request.user).get(pk = pk)
#     return render(request,'lead/leads_detail.html',{
#         'lead':lead
#     })


# class LeadDeleteView(LoginRequiredMixin, DeleteView):
class LeadDeleteView(DeleteView):
    model = Lead
    # success_url = reverse_lazy('leads:list')
    success_url = reverse_lazy('leads_list')
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
        
    def get_queryset(self):
        queryset = super(LeadDeleteView, self).get_queryset()
        # team = self.request.user.userprofile.active_team

        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))
    
    # skip the get_queryset method and use the get method instead.
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

# @login_required
# def leads_delete(request, pk):
#     lead = get_object_or_404(Lead, created_by=request.user,pk=pk)
#     lead.delete()
#     messages.success(request, 'The lead has been deleted successfully!')
#     # return redirect('/dashboard/leads')
#     return redirect('leads_list')


# class LeadUpdateView(LoginRequiredMixin, UpdateView):
class LeadUpdateView(UpdateView):
    model = Lead
    fields = ('name', 'email', 'description', 'priority', 'status',)
    success_url = reverse_lazy('leads_list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit lead'

        return context

    def get_queryset(self):
        queryset = super(LeadUpdateView, self).get_queryset()
        # team = self.request.user.userprofile.active_team
        return queryset.filter(pk=self.kwargs.get('pk'))

# @login_required
# def leads_edit(request, pk):
#     lead = get_object_or_404(Lead, created_by=request.user,pk=pk)
#     if request.method == 'POST':
#         form = AddLeadForm(request.POST, instance=lead)
#         if form.is_valid():
#             lead.save()
#             # messages.success(request, lead.name . ' The lead has been edited successfully!')
#             messages.success(request, lead.name + ' The lead has been edited successfully!')
#             return redirect('leads_list')
#     else:
#         form = AddLeadForm(instance=lead)
#     return render(request, 'lead/leads_edit.html',{
#         'form': form
#     }) # one slash here.

# class LeadCreateView(LoginRequiredMixin, CreateView):

# class LeadCreateView(LoginRequiredMixin, CreateView):
class LeadCreateView(CreateView):
    model = Lead
    fields = ('name', 'email', 'description', 'priority', 'status',)
    success_url = reverse_lazy('leads_list')

    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs): # this method is used to pass additional context to the template
        context = super().get_context_data(**kwargs)
        # team = self.request.user.userprofile.get_active_team()
        # context['team'] = team
        context['title'] = 'Add lead'

        return context

    def form_valid(self, form): # this method is called when the form is valid, it saves the form and adds the created_by field
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        # self.object.team = self.request.user.userprofile.get_active_team()
        self.object.save()
        messages.success(self.request, 'Lead "{}" has been added successfully!'.format(self.object.name))
        return redirect(self.get_success_url())




# @login_required
# def add_lead(request):
#     if request.method == 'POST':
#         form = AddLeadForm(request.POST)
#         if form.is_valid():
#             lead = form.save(commit=False) # don't save the form yet, need to add created_by
#             lead.created_by = request.user
#             lead.save()
#             messages.success(request, 'The lead has been added successfully!')
#             return redirect('leads_list')
#     else:
#         form = AddLeadForm()
#     return render(request, 'lead/add_lead.html',{
#         'form': form
#     }) # one slash here.

class ConvertToClientView(View):
    def get(self,request,*args,**kwargs):
        pk = self.kwargs.get('pk')
        lead = get_object_or_404(Lead, created_by=request.user,pk=pk)
        client = Client.objects.create(
            name=lead.name,
            email=lead.email,
            description=lead.description,
            created_by=request.user,
            # team=team,
        )

        lead.converted_to_client = True
        lead.save()

        # Convert lead comments to client comments

        # comments = lead.comments.all()

        # for comment in comments:
        #     ClientComment.objects.create(
        #         client = client,
        #         content = comment.content,
        #         created_by = comment.created_by,
        #         team = team
        #     )
        
        # Show message and redirect

        messages.success(request, 'The lead was converted to a client.')

        return redirect('leads_list')



# @login_required
# def convert_to_client(request, pk):
#     lead = get_object_or_404(Lead, created_by=request.user,pk=pk)
#     client = Client.objects.create(
#         name = lead.name,
#         email = lead.email,
#         description = lead.description,
#         created_by = request.user
#     )
#     lead.converted_to_client = True
#     lead.save()
#     messages.success(request, 'The lead has been converted to client successfully!')
#     return redirect('leads_list')
