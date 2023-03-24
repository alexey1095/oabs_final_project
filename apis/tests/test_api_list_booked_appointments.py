from rest_framework.test import APITestCase
from django.urls import reverse
import json

from users_app.models_factory import PatientFactory
from users_app.models_factory import DoctorFactory
from users_app.models_factory import DoctorTypeFactory
from users_app.models_factory import UserFactory


from appointments_app.models_factory import AppointmentFactory

from ..serializers import *

from datetime import datetime


class ListBookedAppointmentsAPITest(APITestCase):

    ''' Example of response

    [
    {
        "appointment_date": "2022-12-28T07:00:00",
        "doctor": 1
    },
    {
        "appointment_date": "2022-12-28T07:20:00",
        "doctor": 1
    }]

    '''

    good_url = reverse('apis:list_booked_appointments', kwargs={
                       'doctor_id': '1', 'year': '2022', 'week_number': '52'})
   

    def setUp(self):

        # self.doctor1 = DoctorFactory.create()
        self.patient1 = PatientFactory.create()
        self.appointment1 = AppointmentFactory.create(patient =  self.patient1,
            appointment_date=datetime(2022, 12, 28, 7, 00, 00))  # .create()

        # second appointment with the same doctor as in previous appointment but different patient
        self.appointment2 = AppointmentFactory.create(patient =  self.patient1,
            appointment_date=datetime(2022, 12, 28, 7, 20, 00), doctor= self.appointment1.doctor)  # .create()
        
        self.client.login(username=self.patient1.user.username,
                          password='fnfh!djdf8JJDSlfkd.sofidold73')

        self.response = self.client.get(
            self.good_url,  format='json')
        self.response.render()

        self.data = json.loads(self.response.content)



    def tearDown(self):
        self.client.logout()
        User.objects.all().delete()
        DoctorType.objects.all().delete()
        Doctor.objects.all().delete()

        Appointment.objects.all().delete()

        UserFactory.reset_sequence(0)
        DoctorTypeFactory.reset_sequence(0)
        DoctorFactory.reset_sequence(0)
        PatientFactory.reset_sequence(0)
        AppointmentFactory.reset_sequence(0)

    def test_apiBookAppointmentReturnSuccess(self):

        self.assertEqual(self.response.status_code, 200)


    def test_apiNumberAppointmentBooked(self):
        self.assertEqual(len(self.data), 2)


        #
