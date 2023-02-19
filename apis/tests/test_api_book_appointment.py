from rest_framework.test import APITestCase
from django.urls import reverse


from users_app.models_factory import PatientFactory
from users_app.models_factory import DoctorFactory
from users_app.models_factory import DoctorTypeFactory
from users_app.models_factory import UserFactory

# from ..models_factory import DoctorFactory, UserFactory, DoctorTypeFactory, PatientFactory
from ..serializers import *


class BookAppointmentAPITest(APITestCase):

    good_url = reverse('apis:book_appointment')

    def setUp(self):

        self.doctor1 = DoctorFactory.create()
        self.patient1 = PatientFactory.create()

        self.good_post_data = {
            'appointment_date': '2023-02-20T07:00:00',
            'symptoms': 'test_symptoms',
            'patient': '1',
            'doctor': '1'}

        self.response_post = self.client.post(
            self.good_url, self.good_post_data, format='json')
        self.response_post.render()

    def tearDown(self):
        User.objects.all().delete()
        DoctorType.objects.all().delete()
        Doctor.objects.all().delete()

        UserFactory.reset_sequence(0)
        DoctorTypeFactory.reset_sequence(0)
        DoctorFactory.reset_sequence(0)
        PatientFactory.reset_sequence(0)

    def test_apiBookAppointmentReturnSuccess(self):

        self.assertEqual(self.response_post.status_code, 201)

        #
