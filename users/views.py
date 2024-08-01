from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from users.models import CustomUser, CustomerProfile, SellerProfile
from store.models.order import Cart
from .forms import CustomUserForm, CustomLoginForm
from utilities.otp import send_otp, verify_phone_number


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
        form = CustomLoginForm()
        return render(request, 'users/login.html', {'form': form})
        
    def post(self, request):
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        return render(request, 'users/login.html', {'form': form})
            
    
class SignUpView(View):
    """
    Sign up view: to sign up a user.
    """
    def get(self, request):
        form = CustomUserForm()
        return render(request, 'users/signup.html', {'form': form})
    
    def post(self, request):
        form = CustomUserForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            username = cleaned_data['username']
            email = cleaned_data['email']
            first_name = cleaned_data['first_name']
            last_name = cleaned_data['last_name']
            phone_number = cleaned_data['phone_number']
            password = cleaned_data['password']
            role = cleaned_data['role']
            

            try:
                user = CustomUser(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=phone_number
                )
                user.set_password(password)
                user.is_active = False

                if role == 'seller':
                    user.is_staff = True

                user.save()
                print('user saved')

                code = send_otp(phone_number)
                if code:
                    return render(request, 'users/otp_verify.html', {'code': code, 'role': role, 'phone_number': phone_number })
                else:
                    user.delete()
                    return render(request, 'users/signup.html', {'form': form, 'error': 'Phone verification not successful. Try again.'})
            except Exception as e:
                print('inside exception')
                print(e)
                user.delete()
                return render(request, 'users/signup.html', {'form': form, 'error': 'Signup not successful'})
            # login(request, user)

            # return redirect('home')
        return render(request, 'users/signup.html', {'form': form})


class LogOutView(View):
    """
    Log out view
    """
    def post(self, request):
        logout(request)
        return redirect('index')
    
def verify_phone(request):
    user = request.user
    role = 'buyer'
    if request.method == 'POST':
        code = request.POST.get('code')
        if verify_phone_number(code):
            user.is_active = True
            user.save()
            cart = Cart.objects.create(user=user)
            if role == 'buyer':
                user_profile = CustomerProfile.objects.create(user=user)
            elif role == 'seller':
                user_profile = SellerProfile.objects.create(user=user)
            else:
                user.delete()
                return render(request, 'users/signup.html', {'error': 'Invalid role selected'})
            login(request, user)
            return redirect('home')  # Or your desired success page
        else:
            user.delete()
            return render(request, 'users/verify_otp.html', {'error': 'Invalid or expired OTP'})
    return render(request, 'users/verify_otp.html')