from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, OrderProduct
# from .forms import AddOrderForm, OrderForm, OrderProductFormSet
from .forms import AddOrderForm, OrderForm, OrderProductForm
from django.contrib import messages
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views import View

# Create your views here.
class OrderListView(ListView):
    model = Order
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(OrderListView, self).dispatch(*args, **kwargs)


    def get_queryset(self): # this is the method that is called when the view is loaded, it returns the queryset that is used to populate the list of leads.
        queryset = super(OrderListView,self).get_queryset()
        return queryset.filter(created_by=self.request.user)
    

class OrderDetailView(DetailView):
    model = Order
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):#*args is used to pass any number of arguments to the method, **kwargs is used to pass any additional arguments to the method.
        return super().dispatch(*args, **kwargs) # this method is used to check if the user is logged in before they can access the view. **kwargs is used to pass any additional arguments to the method.
    
    def get_context_data(self, **kwargs): # this method is used to pass additional context to the template, in this case, the AddProductForm form.
        context = super().get_context_data(**kwargs)
        context['form'] = OrderProductForm()
        # context['fileform'] = AddFileForm()

        return context

    def get_queryset(self):
        queryset = super(OrderDetailView, self).get_queryset()
        # team = self.request.user.userprofile.active_team

        # return queryset.filter(team=team, pk=self.kwargs.get('pk'))
        return queryset.filter(pk=self.kwargs.get('pk')).prefetch_related('order_products')

class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('orders:list')
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
        
    def get_queryset(self):
        queryset = super(OrderDeleteView, self).get_queryset()
        # team = self.request.user.userprofile.active_team
        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))
    
    # skip the get_queryset method and use the get method instead.
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)



class OrderCreateView(CreateView):
    model = Order
    # fields = ('name', 'email', 'description', 'priority', 'status',)
    fields = ('order_number', 'client', 'status','total','status',)
    success_url = reverse_lazy('orders:list')

    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs): # this method is used to pass additional context to the template
        context = super().get_context_data(**kwargs)
        # team = self.request.user.userprofile.get_active_team()
        # context['team'] = team
        context['title'] = 'Add order'

        return context

    def form_valid(self, form): # this method is called when the form is valid, it saves the form and adds the created_by field
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        # self.object.team = self.request.user.userprofile.get_active_team()
        self.object.save()
        messages.success(self.request, 'Order "{}" has been added successfully!'.format(self.object.order_number))
        return redirect(self.get_success_url())


class OrderUpdateView(UpdateView):
    model = Order
    # fields = ('name', 'email', 'description', 'priority', 'status',)
    fields = ('order_number', 'client', 'status','total','status',)
    success_url = reverse_lazy('orders:list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit order'

        return context

    def get_queryset(self):
        queryset = super(OrderUpdateView, self).get_queryset()
        # team = self.request.user.userprofile.active_team
        return queryset.filter(pk=self.kwargs.get('pk'))
    
        # add the form_valid method to add a success message
    def form_valid(self, form):
        # messages.success(self.request, "Lead updated successfully.")  # Add success message here
        messages.success(self.request, 'Order "{}" has been updated successfully!'.format(self.object.order_number))
        return super().form_valid(form)

# class AddProductView(LoginRequiredMixin, View):
class AddProductView(View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        form = OrderProductForm(request.POST)

        if form.is_valid():
            product = form.save(commit=False)
            # comment.team = self.request.user.userprofile.get_active_team()
            # product.created_by = request.user
            product.order_id = pk
            product.save()

        return redirect('orders:detail', pk=pk)