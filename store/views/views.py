# store/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from ..models.users import CustomerProfile, SellerProfile, CustomUser
from ..models.product import Product
from ..models.order import Order
from store.forms import SignUpForm


def index(request):
    return render(request, 'base.html')


@login_required
def view_profile(request):
    user = request.user
    if hasattr(user, 'customer_profile'):
        profile = user.customer_profile
    elif hasattr(user, 'seller_profile'):
        profile = user.seller_profile
    else:
        profile = None
    return render(request, 'store/view_profile.html', {'profile': profile})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'store/login.html', {'error': "Invalid email or password"})
    return render(request, 'store/login.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        role = request.POST['role']

        if password1 == password2:
            if CustomUser.objects.filter(username=username).exists():
                return render(request, 'store/signup.html', {'error': 'Username already exists'})
            if CustomUser.objects.filter(email=email).exists():
                return render(request, 'store/signup.html', {'error': 'Email already exists'})

            try:
                user = CustomUser.objects.create_user(username=username, email=email, password=password1)
                
                if role == 'Buyer':
                    user_profile = CustomerProfile.objects.create(user=user)
                elif role == 'Seller':
                    user_profile = SellerProfile.objects.create(user=user)
                else:
                    user.delete()
                    return render(request, 'store/signup.html', {'error': 'Invalid role selected'})
                
                user.save()
                user_profile.save()

                # authenticate and login user
                user = authenticate(username=username, password=password1)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    return render(request, 'store/signup.html', {'error': 'Authentication failed'})
            except Exception as e:
                return render(request, 'store/signup.html', {'error': str(e)})
        else:
            return render(request, 'store/signup.html', {'error': 'Passwords do not match'})

    return render(request, 'store/signup.html')




def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')
    return HttpResponse("Invalid request method.", status=400)

@login_required
def home(request):
    user = request.user
    products = Product.objects.all()
    orders = Order.objects.filter(user=request.user)
    return render(request, 'store/home.html', {'products': products, 'orders': orders})