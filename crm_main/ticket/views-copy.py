from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views import View
from .models import Ticket, Comment
from .forms import TicketForm, CommentForm

class TicketListView(ListView):
    model = Ticket
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TicketListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return Ticket.objects.filter(created_by=self.request.user)

class TicketDetailView(DetailView):
    model = Ticket
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TicketDetailView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

class TicketCreateView(CreateView):
    model = Ticket
    form_class = TicketForm
    success_url = reverse_lazy('tickets:list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TicketCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Ticket created successfully!')
        return super().form_valid(form)

class TicketUpdateView(UpdateView):
    model = Ticket
    form_class = TicketForm
    success_url = reverse_lazy('tickets:list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TicketUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Ticket updated successfully!')
        return super().form_valid(form)

class TicketDeleteView(DeleteView):
    model = Ticket
    success_url = reverse_lazy('tickets:list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TicketDeleteView, self).dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Ticket deleted successfully!')
        return super().delete(request, *args, **kwargs)

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
