from django import forms
from .models import Booking
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model
User = get_user_model()


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['room', 'check_in', 'check_out']  # Fields shown in the form
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),  # Date picker for check-in
            'check_out': forms.DateInput(attrs={'type': 'date'}),  # Date picker for check-out
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')
        
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    phone_number = forms.CharField(max_length=15)

    class Meta:
        model =  User

        fields = ['username','email','password']