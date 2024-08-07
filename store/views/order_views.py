from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
import json
from users.models import CustomerProfile, SellerProfile, CustomUser
from store.models.product import Product, Color, Size
from store.models.order import Order, Cart
from utilities.qr import generate_qr_code, decode_qr_code


def order(request, product_id):
    product = Product.objects.get(id=product_id)
    user = request.user
    products = Product.objects.filter(category=product.category)
    if request.method == 'POST':
        color_name = request.POST['color'] 
        size_name = request.POST['size']

        color = Color.objects.get(name=color_name)
        size = Size.objects.get(name=size_name)

        order = Order.objects.create(user=user, product=product, color=color, size=size)
        return redirect('home')
    return render(request, 'store/order.html', {'product': product, 'products': products})


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

def checkout(request, order_id):
    if request.method == 'POST':
        selected_orders = request.POST.getlist('items')
        orders = []
        user = request.user
        order = Order.objects.get(id=order_id)

        print(order)

        user.cart.orders.remove(order)
        return redirect('view_cart')

def get_product_data(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_data = {
        'name': product.name,
        'available_colors': [{'name': color.name, 'hex_value': color.hex_value} for color in product.available_colors.all()],
        'sizes': [{'name': size.name, 'short_name': size.short_letter} for size in product.size.all()],
    }
    return JsonResponse(product_data)

def my_orders(request):
    if request.user:
        user = request.user
        orders = Order.objects.filter(user=user, cart=None)
    return render(request, 'store/my_orders.html', {'orders': orders})

def order_details(request):
    if request.method == 'POST':
        generate_qr_code(request.order)

        