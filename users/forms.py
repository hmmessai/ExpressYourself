from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.forms import AuthenticationForm
from .validators import validate_password
from django.core.validators import RegexValidator, EmailValidator

CustomUser = get_user_model()
ROLE_CHOICES = [
    ('buyer', 'Buyer'),
    ('seller', 'Seller'),
]

class CustomUserForm(forms.ModelForm):
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repeat Password'}),
        label='Confirm Password',
    )

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Role',
    )

    email = forms.EmailField(
        validators=[EmailValidator(message='Enter a valid email address.')],
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'user@example.com'})
    )
    phone_number = forms.CharField(
        validators=[RegexValidator(r'^09\d{8}$', message='Enter a valid phone number.')],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '09XXXXXXXX'})
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'user@example.com'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Doe'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '09XXXXXXXX'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        }
        labels = {
            'username': 'User Name',
            'email': 'Email Address',
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }
        help_texts = {
            'username': '',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with that email already exists.')
        return email

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password2'):
            raise forms.ValidationError('Passwords do not match')
        return cd.get('password2')
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)
        return password
    

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username'
        }),
        label='User Name'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        }),
        label='Password'
    )

    def confirm_login_allowed(self, user: AbstractBaseUser) -> None:
        return super().confirm_login_allowed(user)

    def clean(self):
        super().clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    "Incorrect username or password. Please try again.",
                    code='invalid_login'
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def get_user(self):
        return self.user_cache