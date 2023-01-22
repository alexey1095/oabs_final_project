from django import forms
from django.contrib.auth.models import User

from django.contrib.auth.forms import AuthenticationForm


# class LoginForm(forms.Form):
#     # 150 is from max length of Django https://docs.djangoproject.com/en/4.1/ref/contrib/auth/#user-model
#     username = forms.CharField(max_length=150)

#     # max length https://www.djangoproject.com/weblog/2013/sep/15/security/
#     password = forms.CharField(max_length=4096)












#AR

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
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=150, widget=forms.PasswordInput)