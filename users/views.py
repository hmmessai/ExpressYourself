from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from users.models import CustomUser, CustomerProfile, SellerProfile
from store.models.order import Cart
from .forms import CustomUserForm, CustomLoginForm


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

                if role == 'seller':
                    user.is_staff = True

                user.save()

                cart = Cart.objects.create(user=user)

                if role == 'buyer':
                    user_profile = CustomerProfile.objects.create(user=user)
                elif role == 'seller':
                    user_profile = SellerProfile.objects.create(user=user)
                else:
                    user.delete()
                    return render(request, 'users/signup.html', {'form': form})
            except Exception as e:
                return render(request, 'users/signup.html', {'form': form})
            login(request, user)

            return redirect('home')
        return render(request, 'users/signup.html', {'form': form})
    




        # username = request.POST['username']
        # email = request.POST['email']
        # password1 = request.POST['password1']
        # password2 = request.POST['password2']
        # phone_number = request.POST['phone_number']
        # role = request.POST['role']

        # if password1 == password2:
        #     if CustomUser.objects.filter(username=username).exists():
        #         return render(request, 'users/signup.html', {'error': 'Username already exists'})
        #     if CustomUser.objects.filter(email=email).exists():
        #         return render(request, 'users/signup.html', {'error': 'Email already exists'})

        #     try:
        #         user = CustomUser.objects.create_user(username=username, email=email, password=password1, phone_number=phone_number)
        #         cart = Cart.objects.create(user=user)
                
        #         if role == 'Buyer':
        #             user_profile = CustomerProfile.objects.create(user=user)
        #         elif role == 'Seller':
        #             user_profile = SellerProfile.objects.create(user=user)
        #         else:
        #             user.delete()
        #             return render(request, 'users/signup.html', {'error': 'Invalid role selected'})
                
        #         user.save()
        #         user_profile.save()

        #         # authenticate and login user
        #         user = authenticate(username=username, password=password1)
        #         if user is not None:
        #             login(request, user)
        #             return redirect('home')
        #         else:
        #             return render(request, 'users/signup.html', {'error': 'Authentication failed'})
        #     except Exception as e:
        #         return render(request, 'users/signup.html', {'error': str(e)})
        # else:
        #     return render(request, 'users/signup.html', {'error': 'Passwords do not match'})


class LogOutView(View):
    """
    Log out view
    """
    def post(self, request):
        logout(request)
        return redirect('index')