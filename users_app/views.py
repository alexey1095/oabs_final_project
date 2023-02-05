from django.shortcuts import render

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required

from django.urls import reverse

from django.contrib import messages

# remove this
from django.http import HttpResponse

from django.http import HttpResponseRedirect

from django.http import HttpResponseNotFound


from . import forms

# Create your views here.


def login_view(request):

    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("users_app:home_page"))
                else:
                    messages.error(request, "Sorry, your account is not active.")

            else:
                messages.error(request, "The entered either login or password is invalid. ")
    else:
        form = forms.LoginForm()


    
    return render(request, 'login.html', {'login_form': form})


@login_required
def logout_view(request):
    logout(request)
    
    messages.success(request, "You are successfully logged out.")
    return HttpResponseRedirect(reverse("users_app:login_page"))


@login_required
def home_view(request):

    # when a user belongs to "patients" group
    if request.user.groups.filter(name='patients').exists():
        return render(request, 'home_patient.html', {'user': request.user})
    elif request.user.groups.filter(name='doctors').exists():
        return render(request, 'home_doctor.html', {'user': request.user})
    else:
        return HttpResponseNotFound('<h1>No group assigned to the user</h1>')
