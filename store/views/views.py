# store/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.forms import model_to_dict
from django.http import HttpResponse
from django.views import View
import json
from users.models import CustomerProfile, SellerProfile, CustomUser
from store.models.product import Product, Category
from store.models.order import Order, Cart


class Index(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'base.html')

class HomeView(LoginRequiredMixin, View):
    """
    Home view that is displayed when the user is authenticated.
    """
    def get(self, request):
        categories = Category.objects.exclude(name='Requested')
        categories_json = {}
        products = Product.objects.filter(status='available')
        orders = Order.objects.filter(user=request.user)
        orders_not_in_cart = []
        for order in orders:
            if order.cart:
                continue
            orders_not_in_cart.append(order)
        return render(request, 'store/home.html', {'products': products, 'orders': orders_not_in_cart, 'categories': categories, 'categories_json': json.dumps(categories_json)})