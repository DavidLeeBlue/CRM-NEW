from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, OrderProduct
from .forms import AddOrderForm, OrderForm, OrderProductFormSet
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

# =====================================================================================================
# =====================================================================================================
# =====================================================================================================
# def order_list(request):
#     orders = Order.objects.all()
#     return render(request, 'order_list.html', {'orders': orders})

# def order_detail(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     order_products = OrderProduct.objects.filter(order=order)
#     return render(request, 'order_detail.html', {'order': order, 'order_products': order_products})

# def order_create(request):
#     if request.method == 'POST':
#         order_form = OrderForm(request.POST)
#         order_product_formset = OrderProductFormSet(request.POST)

#         if order_form.is_valid() and order_product_formset.is_valid():
#             order = order_form.save()
#             for form in order_product_formset:
#                 order_product = form.save(commit=False)
#                 order_product.order = order
#                 order_product.save()
#             return redirect('order_detail', order_id=order.id)
#     else:
#         order_form = OrderForm()
#         order_product_formset = OrderProductFormSet()
    
#     return render(request, 'order_form.html', {'order_form': order_form, 'order_product_formset': order_product_formset})

# def order_update(request, order_id):
#     order = get_object_or_404(Order, id=order_id)

#     if request.method == 'POST':
#         order_form = OrderForm(request.POST, instance=order)
#         order_product_formset = OrderProductFormSet(request.POST, instance=order)

#         if order_form.is_valid() and order_product_formset.is_valid():
#             order_form.save()
#             order_product_formset.save()
#             return redirect('order_detail', order_id=order.id)
#     else:
#         order_form = OrderForm(instance=order)
#         order_product_formset = OrderProductFormSet(instance=order)
    
#     return render(request, 'order_form.html', {'order_form': order_form, 'order_product_formset': order_product_formset})
