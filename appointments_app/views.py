from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from isoweek import Week
from .calendar_html import WeekAppointmentCalendar
from datetime import timedelta
from datetime import datetime, time

# Create your views here.

# @login_required


def appointment_view(request):

    # get the current week number
    week_number = datetime.now().isocalendar().week

    # get the current year
    year = datetime.now().year

    # doctor_id
    doctor_id = 1

    return render(request, 'week_calendar.html', context={"doctor_id": doctor_id, "year": year, "week_number": week_number})


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

    # calendar._generateOneDayColumn('17')
    week_html_table = weekAppointmentCal.generate(
        week_start_date, week_end_date)

    return HttpResponse(week_html_table, content_type="text/html", status=200)


# @login_required
def book_appointment(request):
    pass