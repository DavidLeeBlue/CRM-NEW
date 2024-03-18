from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Order
from .forms import AddOrderForm
from django.contrib import messages

# Create your views here.

@login_required
def orders_list(request):
    orders = Order.objects.filter(created_by=request.user)
    # orders = get_object_or_404(Order, created_by=request.user)
    return render(request, 'order/orders_list.html',{ 'orders': orders })

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order,created_by=request.user, pk=pk)
    return render(request, 'order/orders_detail.html', {'order': order})


@login_required
def order_add(request):
    if request.method == 'POST':
        form = AddOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False) # don't save the form yet, need to add created_by
            order.created_by = request.user
            order.save()
            messages.success(request, order.order_number +  'The order has been added successfully!')
            return redirect('orders_list')
    else:
        form = AddOrderForm()
    return render(request, 'order/orders_add.html',{
        'form': form
    }) # one slash here.

@login_required
def orders_delete(request, pk):
    order = get_object_or_404(Order, created_by=request.user,pk=pk)
    order.delete()
    messages.success(request, order.order_number + ' The order has been deleted successfully!')
    # return redirect('/dashboard/orders')
    return redirect('orders_list')

@login_required
def orders_edit(request, pk):
    order = get_object_or_404(Order, created_by=request.user,pk=pk)
    if request.method == 'POST':
        form = AddOrderForm(request.POST, instance=order)
        if form.is_valid():
            order.save()
            # messages.success(request, lead.name . ' The lead has been edited successfully!')
            messages.success(request, order.order_number + ' The order has been edited successfully!')
            return redirect('orders_list')
    else:
        form = AddOrderForm(instance=order)
    return render(request, 'order/orders_edit.html',{
        'form': form
    }) # one slash here.

