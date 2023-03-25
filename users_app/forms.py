from django import forms
from django.contrib.auth.models import User

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    ''' Login form used in the login view'''
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=150, widget=forms.PasswordInput)


class RegistrationForm(UserCreationForm):
    ''' Registration form'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    dob = forms.DateField()
    home_address = forms.CharField(
        max_length=256, widget=forms.Textarea(attrs={"rows": "5"}))
    home_phone = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name',
                  'last_name', 'dob', 'home_address', 'home_phone')
        labels = {'first_name': 'First name:', 'last_name': 'Last name:',
                  'dob': 'Date of Birth:', 'home_address': 'Home address:', 'home_phone': 'Home phone:', }

        
