from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Tenant, TenantImage
from .forms import TenantForm

class TenantListView(ListView):
    model = Tenant

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TenantListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return Tenant.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Tenant List'
        return context

class TenantDetailView(DetailView):
    model = Tenant

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TenantDetailView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Tenant Detail'
        return context

class TenantCreateView(CreateView):
    model = Tenant
    form_class = TenantForm
    success_url = reverse_lazy('tenant:list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TenantCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        files = self.request.FILES.getlist('image')
        for file in files:
            TenantImage.objects.create(tenant=self.object, image=file)
        messages.success(self.request, 'Tenant created successfully!')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Create Tenant'
        return context

class TenantUpdateView(UpdateView):
    model = Tenant
    form_class = TenantForm
    success_url = reverse_lazy('tenant:list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TenantUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        files = self.request.FILES.getlist('image')
        for file in files:
            TenantImage.objects.create(tenant=self.object, image=file)
        messages.success(self.request, 'Tenant updated successfully!')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Update Tenant'
        return context

class TenantDeleteView(DeleteView):
    model = Tenant
    success_url = reverse_lazy('tenant:list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TenantDeleteView, self).dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Tenant deleted successfully!')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Delete Tenant'
        return context