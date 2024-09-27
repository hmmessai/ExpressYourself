import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from store.models.product import Product, Color, Size
from store.models.order import Order, Cart, Payment

@login_required
def product(request, product_id):
    product = Product.objects.get(id=product_id)

    return render(request, 'store/products/products_admin.html', {'product': product})


@login_required
def add_product(request):
    colors = Color.objects.all()
    sizes = Size.objects.all()
    if request.method == 'POST':
        pass
    return render(request, 'store/products/add_product.html', {'colors': colors, 'sizes': sizes})

@login_required
def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if product:
        product.delete()
    else:
        return redirect.back()
    return redirect('home')

def order_details(request, order_id):
    order = Order.objects.get(id=order_id)
    uorders = Order.objects.filter(user=order.user)
    if order:
        return render(request, 'store/products/order_details.html', {'order': order, 'uorders': uorders})
    else:
        return redirect.back()
