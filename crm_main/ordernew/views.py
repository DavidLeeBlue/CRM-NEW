from django.shortcuts import render, get_object_or_404, redirect
from .models import OrderNew, OrderProductNew
from .forms import OrderForm, OrderProductFormSet

def order_list(request):
    orders = OrderNew.objects.all()
    return render(request, 'ordernew/order_list.html', {'orders': orders})

def order_detailnew(request, pk):
    order = get_object_or_404(OrderNew, id=pk)
    order_products = OrderProductNew.objects.filter(order=order)
    return render(request, 'ordernew/order_detail.html', {'order': order, 'order_products': order_products})

def order_create(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        order_product_formset = OrderProductFormSet(request.POST)

        if order_form.is_valid() and order_product_formset.is_valid():
            order = order_form.save()
            for form in order_product_formset:
                order_product = form.save(commit=False)
                order_product.order = order
                order_product.save()
            return redirect('orders_detailnew', pk=order.id)
            # return redirect('order_detail', order_id=order.id)
    else:
        order_form = OrderForm()
        order_product_formset = OrderProductFormSet()
    
    return render(request, 'ordernew/order_form.html', {'order_form': order_form, 'order_product_formset': order_product_formset})

def order_update(request, pk):
    print('pk:', pk)
    order = get_object_or_404(OrderNew, id=pk)
    print('order:', order)

    if request.method == 'POST':
        order_form = OrderForm(request.POST, instance=order)
        order_product_formset = OrderProductFormSet(request.POST, instance=order)

        if order_form.is_valid() and order_product_formset.is_valid():
            order_form.save()
            order_product_formset.save()
            return redirect('orders_detailnew', pk=order.id)
    else:
        order_form = OrderForm(instance=order)
        order_product_formset = OrderProductFormSet(instance=order)
    
    return render(request, 'ordernew/order_form.html', {'order_form': order_form, 'order_product_formset': order_product_formset})

# def order_update(request,PK):
#     # orders = OrderNew.objects.all()
#     return render(request, 'ordernew/order_list.html')