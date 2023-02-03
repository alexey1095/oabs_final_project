from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotAllowed,  HttpResponseBadRequest
from isoweek import Week
from .calendar_html import WeekAppointmentCalendar
from datetime import timedelta
from datetime import datetime, time

from . import forms

# Create your views here.

# @login_required


def appointment_view(request):

    # get the current week number
    week_number = datetime.now().isocalendar().week

    # get the current year
    year = datetime.now().year

    # doctor_id
    doctor_id = 1

    doctor_name = "Dr. Luis"

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

    # week_number = 1

    # get the date for the start and end for the given week
    w = Week(year, week_number)
    week_start_date = w.monday()
    week_end_date = w.sunday()

    weekAppointmentCal = WeekAppointmentCalendar(

        appointment_duration_minutes=timedelta(hours=0, minutes=20, seconds=0),
        opening_hours_from=time(7, 0, 0),
        opening_hours_till=time(7, 40, 0)
    )

    user_id = request.user.id

    # calendar._generateOneDayColumn('17')
    week_html_table = weekAppointmentCal.generate(
        user_id,
        week_start_date,
        week_end_date
    )

    return HttpResponse(week_html_table, content_type="text/html", status=200)


# @login_required
def book_appointment(request):

    # #if this is a POST request we need to process the form data

    if request.method == 'POST':

        symptoms = request.POST['symptoms']
        doctor_id = request.POST['doctor_id']

        try:
            appointment_datetime = datetime.strptime(
                request.POST['appointment_date_str'],
                '%d-%m-%Y %H:%M')

        except ValueError:
            return HttpResponseBadRequest("Error : The appointment date is in wrong format.")

        # create a form instance and populate it with data from the request:
        # form = NameForm(request.POST)
        # check whether it's valid:
        # if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:

        # return HttpResponseRedirect('/thanks/')
        # appointment_datetime = datetime.strptime(appointment_date_str, '%d-%m-%Y %H:%M')
        pass

    # if a GET (or any other method) we'll create a blank form
    else:
        return HttpResponseNotAllowed(('POST',))

    return
    # return;  render(request, 'name.html', {'form': form})



# class YourForm(forms.Form):
#     test = forms.CharField(label='A test label', widget=forms.Textarea(attrs={"placeholder":"Your Placeholder", "rows":6, "cols":45}), max_length=150)


# if request.method == "POST":
#     form = YourForm(request.POST)
#     if form.is_valid():
#         cleaned_test = form.cleaned_data["test"]