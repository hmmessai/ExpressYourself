from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from users.models import CustomUser, CustomerProfile, SellerProfile
from store.models.order import Cart


class ViewProfile(LoginRequiredMixin, View):
    """
    Views the Profile of the """
    def get(self, request):
        user = request.user
        if hasattr(user, 'customer_profile'):
            profile = user.customer_profile
        elif hasattr(user, 'seller_profile'):
            profile = user.seller_profile
        else:
            profile = None
        return render(request, 'users/view_profile.html', {'profile': profile})


class LoginView(View):
    """
    Login view to log into user account
    """
    def get(self, request):
        return render(request, 'users/login.html')
        
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'users/login.html', {'error': "Invalid email or password"})
        
    
class SignUpView(View):
    """
    Sign up view: to sign up a user.
    """
    def get(self, request):
        return render(request, 'users/signup.html')
    
    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone_number = request.POST['phone_number']
        role = request.POST['role']

        if password1 == password2:
            if CustomUser.objects.filter(username=username).exists():
                return render(request, 'users/signup.html', {'error': 'Username already exists'})
            if CustomUser.objects.filter(email=email).exists():
                return render(request, 'users/signup.html', {'error': 'Email already exists'})

            try:
                user = CustomUser.objects.create_user(username=username, email=email, password=password1, phone_number=phone_number)
                cart = Cart.objects.create(user=user)
                
                if role == 'Buyer':
                    user_profile = CustomerProfile.objects.create(user=user)
                elif role == 'Seller':
                    user_profile = SellerProfile.objects.create(user=user)
                else:
                    user.delete()
                    return render(request, 'users/signup.html', {'error': 'Invalid role selected'})
                
                user.save()
                user_profile.save()

                # authenticate and login user
                user = authenticate(username=username, password=password1)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    return render(request, 'users/signup.html', {'error': 'Authentication failed'})
            except Exception as e:
                return render(request, 'users/signup.html', {'error': str(e)})
        else:
            return render(request, 'users/signup.html', {'error': 'Passwords do not match'})


class LogOutView(View):
    """
    Log out view
    """
    def post(self, request):
        logout(request)
        return redirect('index')