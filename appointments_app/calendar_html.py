
from datetime import timedelta
from datetime import datetime, time
# from django.db import models
from .models import Appointment
from django.db.models import Q

from isoweek import Week


class WeekAppointmentCalendar:

    def __init__(
        self,
        appointment_duration_minutes,
        opening_hours_from,
        opening_hours_till
    ):

        # date of the start and end of the week
        # self.week_start_date = week_start_date
        # self.week_end_date = week_end_date

        # length of appointments in minutes
        self.appointment_duration_minutes = appointment_duration_minutes

        # opening hours from
        self.opening_hours_from = opening_hours_from
        self.opening_hours_till = opening_hours_till

        # id of the logged user
        self.user_id = None

        self.doctor_id = None

    def _addCell(self, appointment_date_time, color):
        ''' Add html table cell with specified colour'''

        td = "<tr>"

        if color == "green":
            td += "<td class='table-success'"
        elif color == "grey":
            td += "<td class='table-secondary'"
        elif color == "red":
            td += "<td class='table-danger'"
        elif color == "blue":
            td += "<td class='table-primary'"
        else:
            td += "<td"

        td += " data-date=" + "'" + \
            f'{appointment_date_time:%d-%m-%Y %H:%M}'+"'"+" >"

        # atime is the object that contains only time (no date)
        atime = appointment_date_time.time()

        # td += f'{atime.hour}:{atime.minute}' + "</td>" + "</tr>"
        td += f'{atime:%H}:{atime:%M}' + "</td>" + "</tr>"

        return td

    def _get_colour(self, queryset_list):

        # Comment: queryset_list should contain only those appointments that have status of either 'Requested' or 'Confirmed'

        colours_dict = {}

        for dic in queryset_list:
            if dic['patient_id'] == self.user_id:
                # this is an appointment registered by this user so it should be blue
                colours_dict[dic['appointment_date']] = 'blue'

            else:
                # this is for appointments booked by someone else
                colours_dict[dic['appointment_date']] = 'red'

        return colours_dict

    def _generateOneDayColumnHTML(self, day_of_month):
        ''' Generate html table for one day with timeslots'''

        # select all appointments booked for the period from the sent date to the next 24 hours
        # ADD TRY block here
        queryset_dict = Appointment.objects.filter(
            Q(appointment_date__range=[
              day_of_month, day_of_month+timedelta(days=1)]),
            Q(doctor=self.doctor_id),
            Q(appointment_status="Confirmed") | Q(
                appointment_status="Requested")
        ).order_by('appointment_date').values()

        colours_dict = self._get_colour(queryset_dict)

        tbl = "<td>"

        tbl += f'{day_of_month:%d}'  # str(day_of_month)

        tbl += "<table class='table table-hover one-day-column'><tbody>"

        # start time of the first appointment in the given day
        current_appointment_date_time = datetime.combine(
            day_of_month, self.opening_hours_from)

        closing_time = datetime.combine(
            day_of_month, self.opening_hours_till)

        while current_appointment_date_time <= closing_time and (closing_time - current_appointment_date_time) >= self.appointment_duration_minutes:

            try:

                # check if the current date has been already booked
                color = colours_dict[current_appointment_date_time]
            except KeyError:
                # when the date is not in the dict it means the date/time is free for booking
                color = 'green'

            tbl += self._addCell(current_appointment_date_time, color)

            current_appointment_date_time = current_appointment_date_time + \
                self.appointment_duration_minutes

        tbl += " </tbody></table></td>"

        return tbl

    def _createTableHeader(self, week_start_date):
        ''' Generate the header of the html-table '''

        html_table = '''<table class='table' id='table_calendar'>
            <thead>
                <tr>
            <th class='text-center' colspan='7'>'''

        html_table += f'{week_start_date:%B} {week_start_date.year}'

        html_table += '''</th>
                </tr>
                <tr>
                    <th scope="col">Mon</th>
                    <th scope="col">Tue</th>
                    <th scope="col">Wed</th>
                    <th scope="col">Thu</th>
                    <th scope="col">Fri</th>
                    <th scope="col">Sat</th>
                    <th scope="col">Sun</th>
                </tr>
            </thead>'''

        html_table += '''<tbody class='table-group-divider'> <tr>'''

        return html_table

    def generate(self, user_id, doctor_id, week_start_date, week_end_date):
        ''' Generate html-week calendar'''

        self.user_id = user_id

        self.doctor_id = doctor_id

        # self._get_colours(week_start_date, week_end_date)

        week_calendar_html = self._createTableHeader(week_start_date)

        current_date = week_start_date

        while current_date <= week_end_date:

            week_calendar_html += self._generateOneDayColumnHTML(current_date)

            current_date = current_date+timedelta(days=1)

        week_calendar_html += "</tr></tbody></table>"

        return week_calendar_html


# ----------- Testing ---------------------------
# if __name__ == "__main__":

#     week_number = 1

#     w = Week(2021, week_number)
#     week_start_date = w.monday()
#     week_end_date = w.sunday()

#     weekAppointmentCal = WeekAppointmentCalendar(

#         appointment_duration_minutes=timedelta(hours=0, minutes=20, seconds=0),
#         opening_hours_from=time(7, 0, 0),
#         opening_hours_till=time(7, 40, 0)
#     )

#     weekAppointmentCal._get_colours(week_start_date, week_end_date)
#     week_html = weekAppointmentCal.generate(week_start_date, week_end_date)

#     print(week_html)
