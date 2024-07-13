from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
import json
from ..models.users import CustomerProfile, SellerProfile, CustomUser
from ..models.product import Product, Color, Size
from ..models.order import Order, Cart


def order(request, product_id, user_id):
    product = Product.objects.get(id=product_id)
    user = CustomUser.objects.get(id=user_id)
    if request.method == 'POST':
        color_name = request.POST['color'] 
        size_name = request.POST['size']

        color = Color.objects.get(name=color_name)
        size = Size.objects.get(name=size_name)

        order = Order.objects.create(user=user, product=product, color=color, size=size)
        order.save()
        return redirect('home')
    return render(request, 'store/order.html', {'product': product})


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    user = request.user
    if request.method == 'POST':
        try:
            cart, created = Cart.objects.get_or_create(user=user)
            if cart.orders.filter(product=product).exists():
                raise Exception("Order already added to cart")
            order = Order.objects.create(user=user, product=product)
            cart.orders.add(order)
            messages.success(request, f"Successfully added to cart")
        except Exception as e:
            messages.error(request, f"Error Occured: {e}")
        return redirect('home')
    return redirect('home')

def view_cart(request):
    user = request.user

    cart = get_object_or_404(Cart, user=user)

    return render(request, 'store/cart.html', {'cart': cart})

def checkout(request):
    selected_orders = request.POST.getlist('orders')
    orders = []
    user = request.user

    print(selected_orders)

    orders = Order.objects.filter(id__in=selected_orders)

    print(orders)
    # Ensure all selected orders belong to the user's cart
    user.cart.orders.remove(*orders)
    

    return redirect('view_cart')