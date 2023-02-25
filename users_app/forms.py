from django import forms
from django.contrib.auth.models import User

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

# class LoginForm(forms.Form):
#     # 150 is from max length of Django https://docs.djangoproject.com/en/4.1/ref/contrib/auth/#user-model
#     username = forms.CharField(max_length=150)

#     # max length https://www.djangoproject.com/weblog/2013/sep/15/security/
#     password = forms.CharField(max_length=4096)


# AR

# class LoginForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput())

#     class Meta:
#         model = User
#         fields = ('username', 'password')

#         help_texts = {
#             'username': None,
#             'password': None}


# this potentially can be extended lated by
# confirm_login_allowed(user)

# class LoginForm(AuthenticationForm):
#     #password = forms.CharField(widget=forms.PasswordInput())

#     pass
#     # class Meta:
#     #     #model = User
#     #     #fields = ('username', 'password')

#     #     help_texts = {
#     #         'username': None,
#     #         'password': None}


class LoginForm(forms.Form):
    ''' Login form used in the login view'''
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=150, widget=forms.PasswordInput)


# class RegistrationForm(forms.Form):
#     username = forms.CharField(label='Username', max_length=150)
#     password = forms.CharField(
#         label='Password', max_length=150, widget=forms.PasswordInput)
#     first_name = forms.CharField(label='First name: ', max_length=150)
#     last_name = forms.CharField(label='Last name: ', max_length=150)
#     dob = forms.DateField(label='Date of birth:')
#     home_address = forms.CharField(
#         label='Home address:', max_length=256, widget=forms.Textarea(attrs={"rows": "5"}))
#     home_phone = forms.CharField(label='Phone number:', max_length=20)


class RegistrationForm(UserCreationForm):

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

        
