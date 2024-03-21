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
    

# @login_required
# def orders_list(request):
#     orders = Order.objects.filter(created_by=request.user)
#     # orders = get_object_or_404(Order, created_by=request.user)
#     return render(request, 'order/orders_list.html',{ 'orders': orders })
    

class OrderDetailView(DetailView):
    model = Order
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):#*args is used to pass any number of arguments to the method, **kwargs is used to pass any additional arguments to the method.
        return super().dispatch(*args, **kwargs) # this method is used to check if the user is logged in before they can access the view. **kwargs is used to pass any additional arguments to the method.
    
    def get_context_data(self, **kwargs): # this method is used to pass additional context to the template, in this case, the AddCommentForm form.
        context = super().get_context_data(**kwargs)
        context['form'] = OrderProductForm()
        # context['fileform'] = AddFileForm()

        return context

    def get_queryset(self):
        queryset = super(OrderDetailView, self).get_queryset()
        # team = self.request.user.userprofile.active_team

        # return queryset.filter(team=team, pk=self.kwargs.get('pk'))
        return queryset.filter(pk=self.kwargs.get('pk'))

# @login_required
# def order_detail(request, pk):
#     order = get_object_or_404(Order,created_by=request.user, pk=pk)
#     return render(request, 'order/orders_detail.html', {
#         'order': order,
#         'form': OrderProductForm(),})

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


# @login_required
# def orders_delete(request, pk):
#     order = get_object_or_404(Order, created_by=request.user,pk=pk)
#     order.delete()
#     messages.success(request, order.order_number + ' The order has been deleted successfully!')
#     # return redirect('/dashboard/orders')
#     return redirect('orders:list')



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

# @login_required
# def order_add(request):
#     if request.method == 'POST':
#         form = AddOrderForm(request.POST)
#         if form.is_valid():
#             order = form.save(commit=False) # don't save the form yet, need to add created_by
#             order.created_by = request.user
#             order.save()
#             messages.success(request, order.order_number +  'The order has been added successfully!')
#             return redirect('orders:list')
#     else:
#         form = AddOrderForm()
#     return render(request, 'order/orders_add.html',{
#         'form': form
#     }) # one slash here.

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
    
# @login_required
# def orders_edit(request, pk):
#     order = get_object_or_404(Order, created_by=request.user,pk=pk)
#     if request.method == 'POST':
#         form = AddOrderForm(request.POST, instance=order)
#         if form.is_valid():
#             order.save()
#             # messages.success(request, lead.name . ' The lead has been edited successfully!')
#             messages.success(request, order.order_number + ' The order has been edited successfully!')
#             return redirect('orders:list')
#     else:
#         form = AddOrderForm(instance=order)
#     return render(request, 'order/orders_edit.html',{
#         'form': form
#     }) # one slash here.

