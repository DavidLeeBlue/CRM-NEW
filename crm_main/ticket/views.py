# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import Ticket, Comment, TicketImage, CommentImage
from .forms import TicketForm, CommentForm, TicketImageForm, CommentImageForm
from django.views.generic.edit import FormMixin

class TicketListView(ListView):
    model = Ticket

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TicketListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = Ticket.objects.filter(created_by=self.request.user)
        priority = self.request.GET.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Ticket List'
        context['priorities'] = Ticket.CHOICES_PRIORITY
        context['selected_priority'] = self.request.GET.get('priority', '')
        return context

class TicketDetailView(FormMixin, DetailView):
    model = Ticket
    form_class = CommentForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TicketDetailView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['image_form'] = CommentImageForm()
        context['comments'] = self.object.comments.all()
        context['page_title'] = 'Ticket Detail'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        image_form = CommentImageForm(request.POST, request.FILES)
        if form.is_valid() and image_form.is_valid():
            return self.form_valid(form, image_form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, image_form):
        comment = form.save(commit=False)
        comment.created_by = self.request.user
        comment.ticket = self.get_object()
        comment.save()
        for image in self.request.FILES.getlist('images'):
            CommentImage.objects.create(comment=comment, image=image)
        return redirect('tickets:detail', pk=comment.ticket.pk)

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
        image_form = CommentImageForm(request.POST, request.FILES)

        if form.is_valid() and image_form.is_valid():
            comment = form.save(commit=False)
            comment.created_by = request.user
            comment.ticket_id = pk
            comment.save()
            for image in request.FILES.getlist('images'):
                CommentImage.objects.create(comment=comment, image=image)

        return redirect('tickets:detail', pk=pk)