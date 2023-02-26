from django.shortcuts import render

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required

from django.urls import reverse

from django.contrib import messages

from datetime import datetime

# remove this
from django.http import HttpResponse

from django.http import HttpResponseRedirect

from django.http import HttpResponseNotFound

from .models import Patient, Doctor

from appointments_app.models import Appointment
from appointments_app.models import WishList

from django.contrib.auth.models import Group


from . import forms

# Create your views here.

def registration_view(request):
    ''' Patient registration view'''

    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                
                # adding a new user to a 'patients' group
                patients_group = Group.objects.get(name='patients') 
                user.groups.add(patients_group)

                user.save()

                # adding new user to patient table
                patient = Patient(
                    user=user,
                    dob = form.cleaned_data['dob'],
                    home_address = form.cleaned_data['home_address'],
                    home_phone = form.cleaned_data['home_phone'] )
                
                patient.save()

                
            except Exception:                                
                    messages.error(
                         request, "Sorry, there was a problem during registration process. ")
                    return HttpResponseRedirect(reverse("users_app:registration_page"))
                    
            messages.success(request, "Your registration has been successful.")
            return HttpResponseRedirect(reverse("users_app:login_page"))

    else:
        form = forms.RegistrationForm()

    return render(request, 'registration.html', {'registration_form': form})


def login_view(request):
    ''' User login view'''

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
                    messages.error(
                        request, "Sorry, your account is not active.")

            else:
                messages.error(
                    request, "The entered either login or password is invalid. ")
    else:
        form = forms.LoginForm()

    return render(request, 'login.html', {'login_form': form})


@login_required(login_url='users_app:login_page')
def logout_view(request):
    ''' Logout view provides the logout functionality'''
    logout(request)

    messages.success(request, "You are successfully logged out.")
    return HttpResponseRedirect(reverse("users_app:login_page"))


@login_required(login_url='users_app:login_page')
def home_view(request):
    ''' Serve the home page for users depending on the group they belongs to'''

    # user belongs to "patients" group
    if request.user.groups.filter(name='patients').exists():

        try:
            patient = Patient.objects.get(user=request.user)
            appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date')[:20]
            wishlist = WishList.objects.filter(patient=patient).order_by('-appointment_date')[:20]


        except Patient.DoesNotExist:
            return HttpResponseNotFound("Error: Patient_id not found.")
        
        # except Appointment.DoesNotExist:
        #     return HttpResponseNotFound("Error: Appointment not found.")
        
        except Exception:
            return HttpResponseNotFound("Error: DB error .")

        # try:
            # limit number to 20 records
        # getting appointments for the patient, order them form newest to oldest and slicing the first 20
        #appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date')[:20]
        # except Appointment.
        #     return HttpResponseNotFound("Error: Patient_id not found.")

        return render(request,
                      'home_patient.html', 
                      context={'user': request.user, 
                               'appointments': appointments,
                               'wishlist': wishlist})

    # user belongs to "doctors" group
    elif request.user.groups.filter(name='doctors').exists():


        ''' return week calendar webpage for a given doctor for current 
        week with next and previous week buttons'''

        # get the current week number
        week_number = datetime.now().isocalendar().week

        # get the current year
        year = datetime.now().year

        doctor = request.user

        try:
            query_set = Doctor.objects.get(user=doctor)
            first_name = query_set.user.first_name
            last_name = query_set.user.last_name
            doctor_name = "Dr. " + first_name + " " + last_name
        
        except Doctor.DoesNotExist:
            return HttpResponseNotFound("Error: Doctor_id not found.")

        except Exception:
            return HttpResponseNotFound("Error: something wrong")

        return render(request, 'home_doctor.html', context={
            "doctor_id": query_set.pk,
            "doctor_name": doctor_name,
            "year": year,
            "week_number": week_number,
        })




        # return render(request, 'home_doctor.html', {'user': request.user})

    # something wrong - no group assigned to user
    else:
        return HttpResponseNotFound('<h1>No group assigned to the user</h1>')
