# views.py
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import Ticket, Comment, TicketImage
from .forms import TicketForm, CommentForm, TicketImageForm
from django.forms import modelformset_factory

# views.py
# from django.shortcuts import render
# from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# from django.urls import reverse_lazy
# from django.contrib import messages
# from django.utils.decorators import method_decorator
# from django.contrib.auth.decorators import login_required
# from django.views import View
# from .models import Ticket, TicketImage
# from .forms import TicketForm, TicketImageForm


class TicketListView(ListView):
    model = Ticket
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TicketListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return Ticket.objects.filter(created_by=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Ticket List'
        return context

class TicketDetailView(DetailView):
    model = Ticket
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TicketDetailView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['page_title'] = 'Ticket Detail'
        return context

# views.py



class TicketCreateView(CreateView):
    model = Ticket
    form_class = TicketForm
    success_url = reverse_lazy('tickets:list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TicketCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        files = self.request.FILES.getlist('image')
        for file in files:
            TicketImage.objects.create(ticket=self.object, image=file)
        messages.success(self.request, 'Ticket created successfully!')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = TicketImageForm()
        context['page_title'] = 'Create Ticket'
        return context

class TicketUpdateView(UpdateView):
    model = Ticket
    form_class = TicketForm
    success_url = reverse_lazy('tickets:list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TicketUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        files = self.request.FILES.getlist('image')
        for file in files:
            TicketImage.objects.create(ticket=self.object, image=file)
        messages.success(self.request, 'Ticket updated successfully!')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = TicketImageForm()
        context['page_title'] = 'Update Ticket'
        return context

class TicketDeleteView(DeleteView):
    model = Ticket
    success_url = reverse_lazy('tickets:list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TicketDeleteView, self).dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Ticket deleted successfully!')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Delete Ticket'
        return context

class AddCommentView(View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.created_by = request.user
            comment.ticket_id = pk
            comment.save()

        return redirect('ticket:detail', pk=pk)