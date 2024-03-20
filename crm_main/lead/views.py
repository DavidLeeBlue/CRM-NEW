from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.contrib.auth.decorators import login_required
# from .forms import AddLeadForm, AddCommentForm
from .forms import AddCommentForm
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
    def dispatch(self, *args, **kwargs):#*args is used to pass any number of arguments to the method, **kwargs is used to pass any additional arguments to the method.
        return super().dispatch(*args, **kwargs) # this method is used to check if the user is logged in before they can access the view. **kwargs is used to pass any additional arguments to the method.
    
    def get_context_data(self, **kwargs): # this method is used to pass additional context to the template, in this case, the AddCommentForm form.
        context = super().get_context_data(**kwargs)
        context['form'] = AddCommentForm()
        # context['fileform'] = AddFileForm()

        return context

    def get_queryset(self):
        queryset = super(LeadDetailView, self).get_queryset()
        # team = self.request.user.userprofile.active_team

        # return queryset.filter(team=team, pk=self.kwargs.get('pk'))
        return queryset.filter(pk=self.kwargs.get('pk'))

class LeadDeleteView(DeleteView):
    model = Lead
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
    
    # add the form_valid method to add a success message
    def form_valid(self, form):
        # messages.success(self.request, "Lead updated successfully.")  # Add success message here
        messages.success(self.request, 'Lead "{}" has been updated successfully!'.format(self.object.name))
        return super().form_valid(form)

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
    
# class AddCommentView(LoginRequiredMixin, View):
class AddCommentView(View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        form = AddCommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            # comment.team = self.request.user.userprofile.get_active_team()
            comment.created_by = request.user
            comment.lead_id = pk
            comment.save()

        return redirect('leads_detail', pk=pk)

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
