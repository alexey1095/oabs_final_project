from rest_framework.test import APITestCase
from django.urls import reverse
from datetime import datetime

from users_app.models_factory import PatientFactory
from appointments_app.models_factory import AppointmentFactory
from appointments_app.models_factory import AppointmentStatusFactory
from users_app.models_factory import DoctorFactory
from users_app.models_factory import DoctorTypeFactory
from users_app.models_factory import UserFactory

from django.test import Client

# from ..models_factory import DoctorFactory, UserFactory, DoctorTypeFactory, PatientFactory
from ..serializers import *


from django.core.management.base import BaseCommand
# https://giovanis.me/post/django-factory/


class Command(BaseCommand):
    help = 'Seeds the database.'

    def handle(self, *args, **options):
        for _ in range(8):
            AppointmentStatusFactory.create(status='Requested')
            AppointmentStatusFactory.create(status='Confirmed')


class BookAppointmentAPITest(APITestCase):

    def setUp(self):

        self.doctor1 = DoctorFactory.create()
        # self.patient1 = PatientFactory.create()

        self.appointment1 = AppointmentFactory.create(
            appointment_date=datetime(2022, 12, 28, 7, 00, 00), doctor=self.doctor1)  # .create()

        AppointmentStatusFactory.create(status='Requested')

        AppointmentStatusFactory.create(status='Confirmed')

        # self.client = Client()
        login_status = self.client.login(
            username=self.doctor1.user.username, password='fnfh!djdf8JJDSlfkd.sofidold73')
        # login_status=self.client.login(username=self.doctor1.user.username, password=self.doctor1.user.password)
        #
        # login_status= self._client.force_authenticate(user=self.doctor1.user)

        self.good_url = reverse('apis:confirm_appointment', kwargs={
                                'appointment_id': self.appointment1.pk})

        # sending empty data
        self.good_patch_data = {}

        self.response_patch = self.client.patch(
            self.good_url, self.good_patch_data, format='json')
        self.response_patch.render()

    def tearDown(self):
        self.client.logout()
        User.objects.all().delete()
        DoctorType.objects.all().delete()
        Doctor.objects.all().delete()

        UserFactory.reset_sequence(0)
        DoctorTypeFactory.reset_sequence(0)
        DoctorFactory.reset_sequence(0)
        PatientFactory.reset_sequence(0)

    def test_apiConfirmAppointmentReturnSuccess(self):

        self.assertEqual(self.response_patch.status_code, 201)
