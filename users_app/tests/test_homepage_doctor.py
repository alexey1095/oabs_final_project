from datetime import datetime
from datetime import timedelta
from django.test import TestCase
from django.urls import reverse
from django.test import Client
from users_app.models_factory import PatientFactory
from users_app.models_factory import DoctorFactory
from appointments_app.models_factory import WishListStatusFactory
from appointments_app.models_factory import AppointmentStatusFactory
from appointments_app.models_factory import DaysOffStatusFactory
from appointments_app.models import WishListStatus
from appointments_app.models import Appointment
from users_app.models import Doctor
from users_app.models import Patient
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


class TestHomePageDoctor(TestCase):

    good_url = reverse('appointments_app:book_appointment')

    response = None

    def setUp(self):

        doctors_group = Group()
        doctors_group.name = 'doctors'
        doctors_group.save()

        self.patient1 = PatientFactory.create()
        self.patient2 = PatientFactory.create()

        self.doctor1 = DoctorFactory.create()
        self.doctor1.user.groups.add(doctors_group)

        WishListStatusFactory.create(status='Waiting')
        WishListStatusFactory.create(status='Available')
        WishListStatusFactory.create(status='Booked')

        DaysOffStatusFactory.create(status='Booked')
        DaysOffStatusFactory.create(status='Cancelled')

        AppointmentStatusFactory.create(status='Requested')
        AppointmentStatusFactory.create(status='Confirmed')
        AppointmentStatusFactory.create(status='Cancelled_by_patient')

        self.client.login(username=self.patient1.user.username,
                          password='fnfh!djdf8JJDSlfkd.sofidold73')

         # determine today date
        day = datetime.now()

        # get the weekday
        weekday = datetime.now().isoweekday() 
        
        # if today is Saturday or Sunday then take the next monday as the current date
        if weekday == 6 or weekday ==7:
            day += timedelta(days=8 - day.isoweekday())

            
        self.date_now = day
        self.appointment_date = f'{self.date_now:%Y-%m-%d}' + " 07:20"
        # this is the same date but in different format
        self.booked_appointment = f'{self.date_now:%d-%m-%Y}' + " 07:20"

        self.availbale_appointment = f'{self.date_now:%d-%m-%Y}' + " 07:00"

        data = {'doctor': self.doctor1.pk,
                'appointment_date': self.appointment_date,
                'symptoms': "test_symptoms",
                'submit': 'Submit'}

        self.response = self.client.post(self.good_url, data=data, follow=True)

        self.client_doctor1 = Client()
        self.client_doctor1.login(username=self.doctor1.user.username,
                                  password='fnfh!djdf8JJDSlfkd.sofidold73')

        self.client_patient2 = Client()
        self.client_patient2.login(username=self.patient2.user.username,
                                   password='fnfh!djdf8JJDSlfkd.sofidold73')

    def teardown(self):
        self.client.logout()
        Patient.objects.all().delete()
        Doctor.objects.all().delete()
        Appointment.objects.all().delete()
        User.objects.all().delete()
        WishListStatus.objects.all().delete()

    def test_homePageDoctorReturnSuccess(self):

        response_get = self.client_doctor1.get(reverse(
            'users_app:home_page'))

        self.assertEqual(response_get.status_code, 200)

    def test_homePageDoctorUseCorrectTemplate(self):

        response_get = self.client_doctor1.get(reverse(
            'users_app:home_page'))

        self.assertTemplateUsed(response_get, 'home_doctor.html')

    def test_confirmedAppointmentHasCorrectLightBlueColour(self):

        url_confirm_appointment = reverse(
            'appointments_app:confirm_appointment')

        data = {'patient': self.patient1.pk,
                'appointment_date': self.appointment_date,
                'submit': 'Submit'}

        response_post = self.client_doctor1.post(
            url_confirm_appointment, data=data, follow=True)

        appointment = Appointment.objects.get(
            doctor=self.doctor1,
            appointment_date=self.appointment_date,
            symptoms="test_symptoms"
        )

        response_get = self.client_doctor1.get(reverse(
            'appointments_app:send_week_calendar',
            kwargs={
                'doctor_id': self.doctor1.pk,
                'year': f'{self.date_now:%Y}',
                'week_number': self.date_now.isocalendar().week}))

        self.assertContains(
            response_get,
            "<td class='table-info' data-date="+"'" +
            f'{self.booked_appointment}'+"'" +
            " data-patient_id=" + "'"+f'{self.patient1.pk}'+"'" +
            " data-patient_name="+"'"+f'{self.patient1.user.first_name} {self.patient1.user.last_name}'+"'" +
            " data-symptoms="+"'" +
            f'{appointment.symptoms}'+"'" + ">07:20</td>",
            html=True)

    def test_unconfirmedAppointmentHasCorrectLightYellowColour(self):

        appointment = Appointment.objects.get(
            doctor=self.doctor1,
            appointment_date=self.appointment_date,
            symptoms="test_symptoms"
        )

        response_get = self.client_doctor1.get(reverse(
            'appointments_app:send_week_calendar',
            kwargs={
                'doctor_id': self.doctor1.pk,
                'year': f'{self.date_now:%Y}',
                'week_number': self.date_now.isocalendar().week}))

        self.assertContains(
            response_get,
            "<td class='table-warning' data-date="+"'" +
            f'{self.booked_appointment}'+"'" +
            " data-patient_id=" + "'"+f'{self.patient1.pk}'+"'" +
            " data-patient_name="+"'"+f'{self.patient1.user.first_name} {self.patient1.user.last_name}'+"'" +
            " data-symptoms="+"'" +
            f'{appointment.symptoms}'+"'" + ">07:20</td>",
            html=True)

    def test_templateContent(self):

        self.assertContains(
            self.response, "if (cell.className == 'table-success')")
        self.assertContains(
            self.response, "<button type='button' class='btn btn-success float-end btn-lg' id='btnNextWeek'> &ensp; &ensp;Next Week &#x3e;&#x3e;</button>", html=True)
        self.assertContains(
            self.response, "<button type='button' class='btn btn-success float-start btn-lg' id='btnPreviousWeek'>&#x3c;&#x3c; Previous Week</button>", html=True)

        