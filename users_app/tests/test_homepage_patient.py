
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
from appointments_app.models import WishList
from users_app.models import Doctor
from users_app.models import Patient
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


class TestHomePagePatient(TestCase):

    good_url = reverse('appointments_app:book_appointment')

    response = None

    def setUp(self):
        patients_group = Group()
        patients_group.name = 'patients'
        patients_group.save()
        self.patient1 = PatientFactory.create()
        self.patient1.user.groups.add(patients_group)
        self.patient2 = PatientFactory.create()
        self.doctor1 = DoctorFactory.create()
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
        WishList.objects.all().delete()
        WishListStatus.objects.all().delete()
        User.objects.all().delete()
        

    def test_homePagePatientReturnSuccess(self):

        response_get = self.client.get(reverse(
            'users_app:home_page'))

        self.assertEqual(response_get.status_code, 200)

    def test_homePagePatientHasListOfAppointments(self):

        response_get = self.client.get(reverse(
            'users_app:home_page'))

        self.assertContains(
            response_get, "<th scope='col'>Appointment Date", html=True)

    def test_homePagePatientHasCorrectAppointmentRecord(self):

        response_get = self.client.get(reverse(
            'users_app:home_page'))

        appointment = Appointment.objects.get(
            doctor=self.doctor1,
            appointment_date=self.appointment_date,
            symptoms="test_symptoms"
        )

        self.assertContains(
            response_get, "<td>"+f'{appointment.appointment_date:%d/%m/%Y %H:%M}'+"</td>", html=True)

        self.assertContains(response_get, "<td>Requested</td>", html=True)

        self.assertContains(response_get, "Dr. " +
                            f'{self.doctor1.user.last_name}', html=True)       


    
    def test_homePagePatientHasCorrectWishListRecord(self):

        WishList.objects.create(
            patient=self.patient1,
            doctor=self.doctor1,
            appointment_date=self.appointment_date,
            symptoms="test_symptoms"            
            )
        
        self.wishlist_entry = WishList.objects.get(            
            doctor=self.doctor1,
            appointment_date=self.appointment_date,
            symptoms="test_symptoms"            
            )
        
        response_get = self.client.get(reverse(
            'users_app:home_page'))
        
        self.assertContains(
            response_get, "<td>"+f'{self.wishlist_entry.appointment_date:%d/%m/%Y %H:%M}'+"</td>", html=True)
        
        self.assertContains(response_get, "<td>Waiting</td>", html=True)

        self.assertContains(response_get, "Dr. " +
                            f'{self.doctor1.user.last_name}', html=True)
        

    def test_homePagePatientUseCorrectTemplate(self):
        
        response_get = self.client.get(reverse(
            'users_app:home_page'))
        
        self.assertTemplateUsed(response_get, 'home_patient.html')
        
    