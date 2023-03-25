from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from django.http import HttpResponseNotFound
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
from users_app.models import Patient
from users_app.models import Doctor
from . import forms


@login_required(login_url='users_app:login_page')
def doctor_list_view(request):
    ''' Show list of doctors with buttons to book appointments'''

    query_set = Doctor.objects.only('user')
    return render(
        request, "list_doctors.html",
        context={'doctors_list': query_set}
    )


@login_required(login_url='users_app:login_page')
def appointment_view(request, doctor_id):
    ''' return week calendar webpage for a given doctor for current 
    week with next and previous week buttons'''

    # determine today date
    day = datetime.now()

    # get the weekday
    weekday = datetime.now().isoweekday() 
    
    # if today is Saturday or Sunday then take the next monday as the current date
    if weekday == 6 or weekday ==7:
        day += timedelta(days=8 - day.isoweekday())

    # get the week number
    week_number = day.isocalendar().week

    # get the year
    year = day.year   

    try:
        query_set = Doctor.objects.get(pk=doctor_id)
        first_name = query_set.user.first_name
        last_name = query_set.user.last_name
        doctor_name = "Dr. " + first_name + " " + last_name

    except Doctor.DoesNotExist:
        return HttpResponseNotFound("Error: Doctor_id not found.")

    except Exception:
        return HttpResponseNotFound("Error: something wrong")

    return render(request, 'week_calendar.html', context={
        "doctor_id": doctor_id,
        "doctor_name": doctor_name,
        "year": year,
        "week_number": week_number,
    })


@login_required(login_url='users_app:login_page')
def send_week_calendar(request, doctor_id, year, week_number):
    ''' # generate and send week calendar --this url is to be accessed 
    via XMLHttpRequest from the week_calendar.html webpage '''

    # Here the doctor_id needs to be checked to confirm that it exists

    # get the date for the start and end for the given week
    w = Week(year, week_number)
    week_start_date = w.monday()
    week_end_date = w.sunday()

    weekAppointmentCal = WeekAppointmentCalendar(

        appointment_duration_minutes=timedelta(hours=0, minutes=20, seconds=0),
        opening_hours_from=time(7, 0, 0),
        opening_hours_till=time(17, 0, 0)
    )

    try:
        # the user may be not found in the Patient table either because this patient does not exist (geniun error)
        # or because the logged user is a doctor
        patient_id = Patient.objects.get(user=request.user).pk

    except Patient.DoesNotExist:

        try:
            # checking if the current user is a doctor?
            Doctor.objects.get(user=request.user)
            # when the logged-in user is a docotr we set the patient_id to -100 for the correct
            # color of cells determination in the week calendar
            patient_id = '-100'
        except Doctor.DoesNotExist:
            return HttpResponseNotFound("Error: User_id not found.")

        except Exception:
            return HttpResponseNotFound("Error: something wrong")

    # calendar._generateOneDayColumn('17')
    week_html_table = weekAppointmentCal.generate(
        patient_id,
        doctor_id,
        week_start_date,
        week_end_date
    )

    return HttpResponse(week_html_table, content_type="text/html", status=200)


@login_required(login_url='users_app:login_page')
def book_appointment(request):

    if request.method != 'POST':
        return HttpResponseNotAllowed(('POST',))

    form = forms.BookNewAppointment(request.POST)

    if not form.is_valid():
        messages.error(request, "Error: " + form.errors)
        return HttpResponseRedirect(reverse("appointment_view"))

    try:
        patient = Patient.objects.get(user=request.user)
        #patient_id = patient.pk

    except Patient.DoesNotExist:
        return HttpResponseNotFound("Error: You are not registered as a patient.")

    except Exception:
        return HttpResponseNotFound("Error: something wrong")

    try:
        new_appointment = form.save(commit=False)
        new_appointment.patient = patient
        new_appointment.save()

    except IntegrityError:
        messages.error(request, "Error: DB Integrity error ")

    doctor_id = form.cleaned_data['doctor'].pk
    appointment_date = form.cleaned_data['appointment_date']


    # now when a new appointment is booked we need to check whether 
    # this appointment was in the the waiting list for the current user
    # and possibly other users
    wishlist = models.WishList.objects.filter(
            Q(doctor=doctor_id),
            Q(appointment_date=appointment_date),
            Q(wishlist_status="Available"))
        
    
    waiting_status = models.WishListStatus.objects.get(status="Waiting")
    booked_status = models.WishListStatus.objects.get(status="Booked")
        
        
    # set 'waiting' status for all the rest patients who might have 
    # this time slot in their wish lists
    for entry in wishlist:
        if entry.patient.user == request.user:
            # this is the case when the current user had this timeslot in their 
            # wish list and they have just booked it
            entry.wishlist_status= booked_status
        else:
            # for all the rest patient set to 'waiting ' again
            entry.wishlist_status= waiting_status
        entry.save()


    return HttpResponseRedirect(reverse("appointments_app:appointment_view", args=(doctor_id,)))

    
@login_required(login_url='users_app:login_page')
def cancel_appointment(request):
    ''' Cancel appointment'''

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


        # now we ned to check if the cancelled appointment was added to 
        # wish list by someone else

        wishlist = models.WishList.objects.filter(
            Q(doctor=doctor),
            Q(appointment_date=appointment_date),
            Q(wishlist_status="Waiting"))
        
        available_status = models.WishListStatus.objects.get(status="Available")
        
        
        for entry in wishlist:
            entry.wishlist_status= available_status
            entry.save()

    except models.AppointmentStatus.DoesNotExist:
        return HttpResponseNotFound("Error: Appointment status does not exist.")

    except models.Appointment.DoesNotExist:
        return HttpResponseNotFound("Error: Appointment does not exist in the db")

    except Patient.DoesNotExist:
        return HttpResponseNotFound("Error: You are not registered as a patient.")

    except Exception:
        return HttpResponseNotFound("Error: something wrong")

    return HttpResponseRedirect(reverse("appointments_app:appointment_view", args=(doctor.pk,)))


@login_required(login_url='users_app:login_page')
def confirm_appointment(request):
    ''' This is for doctors to confirm appointment'''

    if request.method != 'POST':
        return HttpResponseNotAllowed(('POST',))

    try:
        # checking if the current user is a doctor - only doctors can confirm appointments
        Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        return HttpResponseNotFound("Error: current user is not a doctor -- appointment cannot be confirmed.")

    form = forms.ConfirmAppointment(request.POST)

    if not form.is_valid():
        messages.error(request, "Error: " + f'{form.errors}')
        return HttpResponseRedirect(reverse("users_app:home_page"))

    try:
        patient = form.cleaned_data['patient']
        doctor = Doctor.objects.get(user=request.user)
        appointment_date = form.cleaned_data['appointment_date']
        confirmed_status = models.AppointmentStatus.objects.get(
            status='Confirmed')

        appointment = models.Appointment.objects.get(
            Q(patient=patient),
            Q(doctor=doctor),
            Q(appointment_date=appointment_date),
            Q(appointment_status="Requested")
        )

        appointment.appointment_status = confirmed_status
        appointment.save()

    except models.AppointmentStatus.DoesNotExist:
        return HttpResponseNotFound("Error: Appointment status does not exist.")

    except models.Appointment.DoesNotExist:
        return HttpResponseNotFound("Error: Appointment does not exist in the db")

    except models.Doctor.DoesNotExist:
        return HttpResponseNotFound("Error: Doctor does not exist in the db")

    except Patient.DoesNotExist:
        return HttpResponseNotFound("Error: You are not registered as a patient.")

    except Exception:
        return HttpResponseNotFound("Error: something wrong")

    return HttpResponseRedirect(reverse("users_app:home_page"))

@login_required(login_url='users_app:login_page')
def request_daysoff(request):
    ''' This is for doctors to request days off'''

    try:
        # checking if the current user is a doctor - only doctors can request daysoff
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        return HttpResponseNotFound("Error: current user is not a doctor -- access denied.")

    if request.method == 'POST':

        form = forms.RequestDaysOffForm(request.POST)

        if not form.is_valid():
            messages.error(request, "Error: " + f'{form.errors}')
            return HttpResponseRedirect(reverse("appointments_app:request_daysoff"))

        date_from = form.cleaned_data['date_from']
        date_till = form.cleaned_data['date_till']

        #if date_from >= date_till:
        if date_from > date_till:
            messages.error(
                request, "Error: the date From should be less than date To")
            return HttpResponseRedirect(reverse("users_app:home_page"))

        try:
            new_daysoff = form.save(commit=False)
            new_daysoff.doctor = doctor
            new_daysoff.save()

        except IntegrityError:
            messages.error(
                request, "Error: DB Integrity error - unable to create a daysoff record.")
            return HttpResponseRedirect(reverse("appointments_app:request_daysoff"))

        except Exception:
            messages.error(
                request, "Error: db internal error - unable to create a daysoff record.")
            return HttpResponseRedirect(reverse("appointments_app:request_daysoff"))

        messages.success(
            request, "Your days off have been successfully booked .")
        return HttpResponseRedirect(reverse("appointments_app:request_daysoff"))

    else:
        form = forms.RequestDaysOffForm()

    daysoff_list = models.DaysOff.objects.filter(
        doctor=doctor).order_by('-date_from')[:20]

    return render(request, 'request_daysoff.html', {'daysoff_form': form,
                                                    'daysoff_list': daysoff_list})

@login_required(login_url='users_app:login_page')
def cancel_daysoff(request, pk):
    '''Cancel daysoff'''

    if request.method != 'GET':
        return HttpResponseNotAllowed(('GET',))
    

     # checking if the current user is a doctor - only doctors can cancel daysoff
    try:
        doctor = Doctor.objects.get(user=request.user)

        status_cancelled = models.DaysOffStatus.objects.get(status='Cancelled')

        daysoff = models.DaysOff.objects.get(pk=pk)

        # check if the doctor who booked a daysoff is the same doctor 
        # who is requesting the daysoff cancel       

        if daysoff.doctor != doctor:
            return HttpResponseNotFound("Error: the daysoff can be cancelled only by the same doctor who ownes the daysoff")
        
        daysoff.daysoff_status = status_cancelled
        daysoff.save()

    except Doctor.DoesNotExist:
        return HttpResponseNotFound("Error: current user is not a doctor -- access denied.")
    
    except models.DaysOffStatus.DoesNotExist:
        return HttpResponseNotFound("Error: the requested daysoff status does not exist")
    
    except models.DaysOff.DoesNotExist:
        return HttpResponseNotFound("Error: the requested daysoff period does not exist")  

    return HttpResponseRedirect(reverse("appointments_app:request_daysoff"))


@login_required(login_url='users_app:login_page')
def add_to_wishlist(request):
    ''' Adding a booked appointment into wishlist'''
    
    if request.method != 'POST':
        return HttpResponseNotAllowed(('POST',))

    form = forms.AddToWishList(request.POST)

    if not form.is_valid():
        messages.error(request, "Error: " + form.errors)
        return HttpResponseRedirect(reverse("appointment_view"))    

    try:
        patient = Patient.objects.get(user=request.user)        

    except Patient.DoesNotExist:
        return HttpResponseNotFound("Error: You are not registered as a patient.")

    except Exception:
        return HttpResponseNotFound("Error: something wrong")

    try:
        new_wishlist_record = form.save(commit=False)
        new_wishlist_record.patient = patient
        new_wishlist_record.save()

    except IntegrityError:
        messages.error(request, "Error: DB Integrity error ")

    except Exception:
        messages.error(request, "Error: DB error ")


    doctor_id = request.POST['doctor']

    messages.success(
            request, "The appointment has been added to the wish list - Yous will be notified should this timeslot become availble..")

    return HttpResponseRedirect(reverse("appointments_app:appointment_view", args=(doctor_id,)))
