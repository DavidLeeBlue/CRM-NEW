from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.contrib.auth.decorators import login_required
from .forms import AddProductForm
from .models import Product
from django.contrib import messages
# from client.models import Client


@login_required
def products_list(request):
    products = Product.objects.all()
    return render(request, 'product/products_list.html',{
        'products': products
    })

@login_required
def products_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    # Product = get_object_or_404(Product, created_by=request.user,pk=pk)
    # Product = Product.objects.filter(created_by=request.user).get(pk = pk)
    return render(request,'product/products_detail.html',{
        'product':product
    })

@login_required
def products_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, 'The Product has been deleted successfully!')
    # return redirect('/dashboard/products')
    return redirect('products:list')

@login_required
def products_edit(request, pk):
    product = get_object_or_404(Product, created_by=request.user,pk=pk)
    if request.method == 'POST':
        form = AddProductForm(request.POST, instance=product)
        if form.is_valid():
            product.save()
            # messages.success(request, Product.name . ' The Product has been edited successfully!')
            messages.success(request, product.name + ' The Product has been edited successfully!')
            return redirect('products:list')
    else:
        form = AddProductForm(instance=product)
    return render(request, 'product/products_edit.html',{
        'form': form
    }) # one slash here.


@login_required
def products_add(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False) # don't save the form yet, need to add created_by
            product.created_by = request.user
            product.save()
            messages.success(request, 'The Product has been added successfully!')
            return redirect('products:list')
    else:
        form = AddProductForm()
    return render(request, 'product/products_add.html',{
        'form': form
    }) # one slash here.


