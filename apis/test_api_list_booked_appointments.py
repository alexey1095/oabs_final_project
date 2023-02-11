from rest_framework.test import APITestCase
from django.urls import reverse
import json

from .models_factory import DoctorFactory, UserFactory, DoctorTypeFactory, PatientFactory, AppointmentFactory, AppointmentStatusFactory
from .serializers import *

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

    good_url = reverse('list_booked_appointments', kwargs={
                       'doctor_id': '1', 'year': '2022', 'week_number': '52'})
   

    def setUp(self):

        # self.doctor1 = DoctorFactory.create()
        # self.patient1 = PatientFactory.create()
        self.appointment1 = AppointmentFactory.create(
            appointment_date=datetime(2022, 12, 28, 7, 00, 00))  # .create()

        # second appointment with the same doctor as in previous appointment but different patient
        self.appointment2 = AppointmentFactory.create(
            appointment_date=datetime(2022, 12, 28, 7, 20, 00), doctor= self.appointment1.doctor)  # .create()

        self.response = self.client.get(
            self.good_url,  format='json')
        self.response.render()

        self.data = json.loads(self.response.content)



    def tearDown(self):
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