
from datetime import timedelta
from datetime import datetime, time
# from django.db import models
from .models import Appointment
from .models import DaysOff
from django.db.models import Q

from users_app.models import Patient

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

    def _addCell_for_patient(self, appointment_date_time, color):
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
        elif color == "light_blue":
            td += "<td class='table-info'"
        elif color == "yellow":
            td += "<td class='table-warning'"
        else:
            td += "<td"

        td += " data-date=" + "'" + \
            f'{appointment_date_time:%d-%m-%Y %H:%M}'+"'"+" >"

        # atime is the object that contains only time (no date)
        atime = appointment_date_time.time()

        td += f'{atime:%H}:{atime:%M}' + "</td>" + "</tr>"

        return td

    def _addCell_for_doctor(self, appointment_date_time, color, patient_id, symptoms):
        ''' Add html table cell with specified colour'''

        # we need to retreive the patient name only for those cells where patient name is not equal to NA
        # Ibelieve NA can be only for those cells that are booked by doctors
        patient_name = "NA"
        if patient_id != "NA":
            try:
                patient = Patient.objects.get(pk=patient_id)
                patient_name = patient.user.first_name + " " + patient.user.last_name
            except Patient.DoesNotExist:
                patient_name = "Error: patient not found"

        td = "<tr>"

        if color == "green":
            td += "<td class='table-success'"
        elif color == "grey":
            td += "<td class='table-secondary'"
        elif color == "red":
            td += "<td class='table-danger'"
        elif color == "blue":
            td += "<td class='table-primary'"
        elif color == "light_blue":
            td += "<td class='table-info'"
        elif color == "yellow":
            td += "<td class='table-warning'"
        else:
            td += "<td"

        td += " data-date=" + "'" + \
            f'{appointment_date_time:%d-%m-%Y %H:%M}'+"'"

        td += " data-patient_id=" + "'"+f'{patient_id}'+"'"

        td += " data-patient_name=" + "'"+f'{patient_name}'+"'"

        td += " data-symptoms=" + "'"+f'{symptoms}'+"'"+" >"

        # atime is the object that contains only time (no date)
        atime = appointment_date_time.time()

        td += f'{atime:%H}:{atime:%M}' + "</td>" + "</tr>"

        return td

    def _get_colour_for_patient(self, queryset_list):

        # Comment: queryset_list should contain only those appointments
        # that have status of either 'Requested' or 'Confirmed'

        colours_dict = {}

        for dic in queryset_list:
            if dic['patient_id'] == self.user_id:

                if dic['appointment_status_id'] == 'Requested':
                    # this is when appointment requested by a patient by not confirmed yet
                    # colours_dict[dic['appointment_date']] = 'yellow'
                    colours_dict[dic['appointment_date']] = {}
                    colours_dict[dic['appointment_date']]['colour'] = 'yellow'
                elif dic['appointment_status_id'] == 'Confirmed':
                    # this is an appointment registered by this user so it should be blue
                    # colours_dict[dic['appointment_date']] = 'blue'

                    colours_dict[dic['appointment_date']] = {}
                    colours_dict[dic['appointment_date']]['colour'] = 'blue'
                else:
                    # this is when something wrong - appointment has a status which is neither requested nor confirmed..

                    colours_dict[dic['appointment_date']] = {}
                    colours_dict[dic['appointment_date']]['colour'] = 'unknown'

            else:
                # this is for appointments booked by someone else
                colours_dict[dic['appointment_date']] = {}
                colours_dict[dic['appointment_date']]['colour'] = 'red'

        return colours_dict

    def _get_colour_for_doctor(self, queryset_list):

        # Comment: queryset_list should contain only those appointments
        # that have status of either 'Requested' or 'Confirmed'

        # the reason to have tow function

        colours_dict = {}

        for dic in queryset_list:
            # if dic['patient_id'] == self.user_id:

            if dic['appointment_status_id'] == 'Requested':
                # this is when appointment requested by a patient by not confirmed yet
                colours_dict[dic['appointment_date']] = {}
                colours_dict[dic['appointment_date']]['colour'] = 'yellow'
                colours_dict[dic['appointment_date']
                             ]['patient_id'] = dic['patient_id']
                colours_dict[dic['appointment_date']
                             ]['symptoms'] = dic['symptoms']

                # colours_dict[dic['symptoms']] = dic['symptoms']

            elif dic['appointment_status_id'] == 'Confirmed':
                # this is an appointment registered by this user so it should be blue
                colours_dict[dic['appointment_date']] = {}
                colours_dict[dic['appointment_date']]['colour'] = 'light_blue'
                colours_dict[dic['appointment_date']
                             ]['patient_id'] = dic['patient_id']
                colours_dict[dic['appointment_date']
                             ]['symptoms'] = dic['symptoms']

            else:
                # this is when something wrong - appointment has a status which is neither requested nor confirmed..
                colours_dict[dic['appointment_date']] = {}
                colours_dict[dic['appointment_date']]['colour'] = 'unknown'
                colours_dict[dic['appointment_date']]['patient_id'] = 'unknown'
                colours_dict[dic['appointment_date']]['symptoms'] = 'unknown'

            # else:
            #     # this is for appointments booked by someone else
            #     colours_dict[dic['appointment_date']] = 'red'

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

        # user_id is set to -100 for doctor
        if self.user_id != '-100':
            colours_dict = self._get_colour_for_patient(queryset_dict)
        else:
            colours_dict = self._get_colour_for_doctor(queryset_dict)

        tbl = "<td>"

        tbl += f'{day_of_month:%d}'

        tbl += "<table class='table table-hover one-day-column'><tbody>"

        # start time of the first appointment in the given day
        current_appointment_date_time = datetime.combine(
            day_of_month, self.opening_hours_from)

        closing_time = datetime.combine(
            day_of_month, self.opening_hours_till)

        while current_appointment_date_time <= closing_time and (
                closing_time - current_appointment_date_time) >= self.appointment_duration_minutes:

            try:

                # checking whether the 'current_appointment_date_time' is booked as day off for the doctor 
                daysoff = DaysOff.objects.filter(
                    doctor=self.doctor_id,
                    date_from__lte=current_appointment_date_time.date(), 
                    date_till__gte=current_appointment_date_time.date(),
                    daysoff_status='Booked')
                
                if daysoff:
                    color = 'grey'
                    
                    if self.user_id == '-100':
                        patient_id = 'NA'
                        symptoms = 'NA'
                else:                                                    
                    # check if the current date has been already booked then the colour should be
                    # either red or blue
                    color = colours_dict[current_appointment_date_time]['colour']

                # the below two fields we need only for doctors
                if self.user_id == '-100' and not daysoff:
                    patient_id = colours_dict[current_appointment_date_time]['patient_id']
                    symptoms = colours_dict[current_appointment_date_time]['symptoms']

            except KeyError:
                # when the date is not in the dict it means the date/time is free for booking
                color = 'green'

                if self.user_id == '-100':
                    patient_id = 'NA'
                    symptoms = 'NA'

            except Exception:
                pass

            if self.user_id != '-100':
                tbl += self._addCell_for_patient(
                    current_appointment_date_time, color)
            else:
                tbl += self._addCell_for_doctor(
                    current_appointment_date_time, color, patient_id, symptoms)

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
