from django import forms
from django.contrib.auth import get_user_model
from .validators import validate_phone_number

CustomUser = get_user_model()

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'username']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'user@example.com'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Doe'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '09XXXXXXXX'}),
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

    phone_number = forms.CharField(validators=[validate_phone_number])