from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, OrderProduct
from .forms import AddOrderForm, OrderForm, OrderProductForm
from django.contrib import messages
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views import View

class OrderListView(ListView):
    model = Order
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(OrderListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(created_by=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Order List'
        return context

class OrderDetailView(DetailView):
    model = Order
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OrderProductForm()
        context['page_title'] = 'Order Detail'
        return context

    def get_queryset(self):
        queryset = super(OrderDetailView, self).get_queryset()
        return queryset.filter(pk=self.kwargs.get('pk'))

class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('orders:list')
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = super(OrderDeleteView, self).get_queryset()
        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Delete Order'
        return context

class OrderCreateView(CreateView):
    model = Order
    fields = ('order_number', 'client', 'status', 'total', 'status',)
    success_url = reverse_lazy('orders:list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add order'
        context['page_title'] = 'Create Order'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        messages.success(self.request, 'Order "{}" has been added successfully!'.format(self.object.order_number))
        return redirect(self.get_success_url())

class OrderUpdateView(UpdateView):
    model = Order
    fields = ('order_number', 'client', 'status', 'total', 'status',)
    success_url = reverse_lazy('orders:list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit order'
        context['page_title'] = 'Update Order'
        return context

    def get_queryset(self):
        queryset = super(OrderUpdateView, self).get_queryset()
        return queryset.filter(pk=self.kwargs.get('pk'))

    def form_valid(self, form):
        messages.success(self.request, 'Order "{}" has been updated successfully!'.format(self.object.order_number))
        return super().form_valid(form)

class AddProductView(CreateView):
    model = OrderProduct
    form_class = OrderProductForm
    template_name = 'order/add_product.html'
    success_url = reverse_lazy('orders:list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.order = get_object_or_404(Order, pk=self.kwargs['pk'])
        messages.success(self.request, 'Product has been added to the order successfully!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Add Product to Order'
        return context