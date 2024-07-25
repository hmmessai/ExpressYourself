from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from .validators import validate_password
from django.core.validators import RegexValidator, EmailValidator

CustomUser = get_user_model()

class CustomUserForm(forms.ModelForm):
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repeat Password'}),
        label='Confirm Password',
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
        validators = {
            'email': [EmailValidator(message='Enter a valid email address.')],
            'phone_number': [RegexValidator(r'^09\d{8}$', message='Enter a valid phone number.')],
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
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

        widgets = {
                'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
                'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            }

        labels = {
            'username': 'User Name',
            'password': 'Password',
        }