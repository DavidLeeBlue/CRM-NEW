# from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import AddTicketForm, AddCommentForm
from .models import Ticket, Comment
from django.contrib import messages
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views import View

class TicketListView(ListView):
    model = Ticket

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TicketListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = super(TicketListView, self).get_queryset()
        return queryset.filter(created_by=self.request.user)

class TicketDetailView(DetailView):
    model = Ticket

class TicketCreateView(CreateView):
    model = Ticket
    form_class = AddTicketForm
    success_url = reverse_lazy('ticket-list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TicketCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Ticket created successfully.')
        return super(TicketCreateView, self).form_valid(form)

class TicketUpdateView(UpdateView):
    model = Ticket
    form_class = AddTicketForm
    success_url = reverse_lazy('ticket-list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TicketUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Ticket updated successfully.')
        return super(TicketUpdateView, self).form_valid(form)

class TicketDeleteView(DeleteView):
    model = Ticket
    success_url = reverse_lazy('ticket-list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TicketDeleteView, self).dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Ticket deleted successfully.')
        return super(TicketDeleteView, self).delete(request, *args, **kwargs)

class CommentCreateView(CreateView):
    model = Comment
    form_class = AddCommentForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CommentCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.ticket = get_object_or_404(Ticket, pk=self.kwargs['ticket_id'])
        messages.success(self.request, 'Comment added successfully.')
        return super(CommentCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('ticket-detail', kwargs={'pk': self.kwargs['ticket_id']})