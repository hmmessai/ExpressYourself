# store/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from ..models.users import CustomerProfile, SellerProfile, CustomUser
from store.forms import SignUpForm

@login_required
def view_profile(request):
    user = request.user
    if hasattr(user, 'customerprofile'):
        profile = user.customerprofile
    elif hasattr(user, 'sellerprofile'):
        profile = user.sellerprofile
    else:
        profile = None
    return render(request, 'base.html', {'profile': profile})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('view_profile')
        else:
            return render(request, 'store/login.html', {'error': "Invalid email or password"})
    return render(request, 'store/login.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = CustomUser.objects.create_user(username=username, email=email, password=password1)
                user.save()
                user = authenticate(username=username, password=password1)
                if user is not None:
                    login(request, user)
                    return redirect('view_profile')
            except Exception as e:
                return render(request, 'store/signup.html', {'error': str(e)})
        else:
            return render(request, 'store/signup.html', {'error': 'Passwords do not match'})
    return render(request, 'store/signup.html')

