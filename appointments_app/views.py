from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotAllowed,  HttpResponseBadRequest, HttpResponseNotFound
from isoweek import Week
from .calendar_html import WeekAppointmentCalendar
from datetime import timedelta
from datetime import datetime, time
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.db.models import Q
from datetime import datetime

from . import models

from users_app.models import Doctor, Patient

from . import forms

# Create your views here.


def doctor_list_view(request):
    query_set = Doctor.objects.only('user')
    return render(request, "list_doctors.html", context={'doctors_list': query_set})


# @login_required
def appointment_view(request, doctor_id):

    # get the current week number
    week_number = datetime.now().isocalendar().week

    # get the current year
    year = datetime.now().year

    # doctor_id
    # doctor_id = 1

    try:
        query_set = Doctor.objects.get(pk=doctor_id)
        first_name = query_set.user.first_name
        last_name = query_set.user.last_name
        doctor_name = "Dr. " + first_name + " " + last_name
    except Doctor.DoesNotExist:
        return HttpResponseNotFound("Error: Doctor_id not found.")

    except Exception:
        return HttpResponseNotFound("Error: something wrong")

    # symptoms_form = forms.SymptomsForm()
    # hidden_fields_form = forms.DoctorAndAppointmentDateForm()

    return render(request, 'week_calendar.html', context={
        "doctor_id": doctor_id,
        "doctor_name": doctor_name,
        "year": year,
        "week_number": week_number,
        # "symptoms_form":symptoms_form,
        # "hidden_fields_form":  hidden_fields_form
    })


# @login_required
def send_week_calendar(request, doctor_id, year, week_number):
    ''' # generate and send week calendar --this url is to be accessed via XMLHttpRequest from the week_calendar.html webpage '''

    # Here the doctor_id needs to be checked to confirm that it exists

    # get the date for the start and end for the given week
    w = Week(year, week_number)
    week_start_date = w.monday()
    week_end_date = w.sunday()

    weekAppointmentCal = WeekAppointmentCalendar(

        appointment_duration_minutes=timedelta(hours=0, minutes=20, seconds=0),
        opening_hours_from=time(7, 0, 0),
        opening_hours_till=time(7, 40, 0)
    )

    # user_id = request.user.id

    patient_id = Patient.objects.get(user=request.user).pk

    # calendar._generateOneDayColumn('17')
    week_html_table = weekAppointmentCal.generate(
        patient_id,
        doctor_id,
        week_start_date,
        week_end_date
    )

    return HttpResponse(week_html_table, content_type="text/html", status=200)


# @login_required
def book_appointment(request):

    if request.method != 'POST':
        return HttpResponseNotAllowed(('POST',))

    form = forms.BookNewAppointment(request.POST)

    if not form.is_valid():
        messages.error(request, "Error: " + form.errors)
        return HttpResponseRedirect(reverse("appointment_view"))

    try:
        patient = Patient.objects.get(user=request.user)
        patient_id = patient.pk

    except Patient.DoesNotExist:
        return HttpResponseNotFound("Error: You are not registered as a patient.")

    except Exception:
        return HttpResponseNotFound("Error: something wrong")

    try:
        # new_appointment = models.Appointment(
        #     doctor=form.cleaned_data['doctor'],
        #     appointment_date = form.cleaned_data['appointment_date'],
        #     patient = request.user,
        #     symptoms= form.cleaned_data['symptoms']
        # )

        new_appointment = form.save(commit=False)
        new_appointment.patient = patient
        new_appointment.save()

    except IntegrityError:
        messages.error(request, "Error: DB Integrity error ")

    doctor_id = request.POST['doctor']

    return HttpResponseRedirect(reverse("appointments_app:appointment_view", args=(doctor_id,)))

    # check if the time slot is availble for booking
    # models.Appointment.objects.filter(
    #     doctor=form.cleaned_data['doctor'],
    #     appointment_date = form.cleaned_data['appointment_date'],)

    #    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    # doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    # appointment_date = models.DateTimeField(blank=False)
    # symptoms = models.CharField(max_length=256, blank=False)
    # request_date = models.DateTimeField(blank=False, auto_now_add=True)
    # appointment_status = models.ForeignKey(

    # if a GET (or any other method) we'll create a blank form

    # return
    # return;  render(request, 'name.html', {'form': form})


# class YourForm(forms.Form):
#     test = forms.CharField(label='A test label', widget=forms.Textarea(attrs={"placeholder":"Your Placeholder", "rows":6, "cols":45}), max_length=150)


# if request.method == "POST":
#     form = YourForm(request.POST)
#     if form.is_valid():
#         cleaned_test = form.cleaned_data["test"]


# @login_required
def cancel_appointment(request):

    if request.method != 'POST':
        return HttpResponseNotAllowed(('POST',))

    form = forms.CancelAppointment(request.POST)

    if not form.is_valid():
        messages.error(request, "Error: " + form.errors)
        return HttpResponseRedirect(reverse("appointment_view"))

    try:
        patient = Patient.objects.get(user=request.user)
        doctor = form.cleaned_data['doctor']
        appointment_date = form.cleaned_data['appointment_date']
        cancelled_status = models.AppointmentStatus.objects.get(
            status='Cancelled_by_patient')

        appointment = models.Appointment.objects.get(
            Q(patient=patient),
            Q(doctor=doctor),
            Q(appointment_date=appointment_date),
            Q(appointment_status="Confirmed") | Q(
                appointment_status="Requested")
        )

        appointment.appointment_status = cancelled_status
        appointment.save()

    except models.AppointmentStatus.DoesNotExist:
        return HttpResponseNotFound("Error: Appointment status does not exist.")

    except models.Appointment.DoesNotExist:
        return HttpResponseNotFound("Error: Appointment does not exist in the db")

    except Patient.DoesNotExist:
        return HttpResponseNotFound("Error: You are not registered as a patient.")

    except Exception:
        return HttpResponseNotFound("Error: something wrong")

    return HttpResponseRedirect(reverse("appointments_app:appointment_view", args=(doctor.pk,)))
