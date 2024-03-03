from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.contrib.auth.decorators import login_required
# from .forms import AddProductForm
from .models import Product
from django.contrib import messages
# from client.models import Client


@login_required
def products_list(request):
    products = Product.objects.all()
    return render(request, 'product/products_list.html',{
        'products': products
    })

# @login_required
# def products_detail(request, pk):
#     Product = get_object_or_404(Product, created_by=request.user,pk=pk)
#     # Product = Product.objects.filter(created_by=request.user).get(pk = pk)
#     return render(request,'Product/products_detail.html',{
#         'Product':Product
#     })

# @login_required
# def products_delete(request, pk):
#     Product = get_object_or_404(Product, created_by=request.user,pk=pk)
#     Product.delete()
#     messages.success(request, 'The Product has been deleted successfully!')
#     # return redirect('/dashboard/products')
#     return redirect('products_list')

# @login_required
# def products_edit(request, pk):
#     Product = get_object_or_404(Product, created_by=request.user,pk=pk)
#     if request.method == 'POST':
#         form = AddProductForm(request.POST, instance=Product)
#         if form.is_valid():
#             Product.save()
#             # messages.success(request, Product.name . ' The Product has been edited successfully!')
#             messages.success(request, Product.name + ' The Product has been edited successfully!')
#             return redirect('products_list')
#     else:
#         form = AddProductForm(instance=Product)
#     return render(request, 'Product/products_edit.html',{
#         'form': form
#     }) # one slash here.


# @login_required
# def add_Product(request):
#     if request.method == 'POST':
#         form = AddProductForm(request.POST)
#         if form.is_valid():
#             Product = form.save(commit=False) # don't save the form yet, need to add created_by
#             Product.created_by = request.user
#             Product.save()
#             messages.success(request, 'The Product has been added successfully!')
#             return redirect('products_list')
#     else:
#         form = AddProductForm()
#     return render(request, 'Product/add_Product.html',{
#         'form': form
#     }) # one slash here.

# @login_required
# def convert_to_client(request, pk):
#     Product = get_object_or_404(Product, created_by=request.user,pk=pk)
#     client = Client.objects.create(
#         name = Product.name,
#         email = Product.email,
#         description = Product.description,
#         created_by = request.user
#     )
#     Product.converted_to_client = True
#     Product.save()
#     messages.success(request, 'The Product has been converted to client successfully!')
#     return redirect('products_list')
