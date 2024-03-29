from rest_framework.test import APITestCase
from django.urls import reverse
from users_app.models_factory import PatientFactory
from users_app.models_factory import DoctorFactory
from users_app.models_factory import DoctorTypeFactory
from users_app.models_factory import UserFactory
from ..serializers import *


class RequestDaysOffAPITest(APITestCase):

    good_url = reverse('apis:request_daysoff')

    def setUp(self):

        self.doctor1 = DoctorFactory.create()        
        self.client.login(username=self.doctor1.user.username,
                          password='fnfh!djdf8JJDSlfkd.sofidold73')

        self.good_post_data = {
            'doctor':self.doctor1.user.pk, 
            'date_from': '2023-02-20',
            'date_till': '2023-02-23',
        }

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

    def test_apiRequestDaysOffReturnSuccess(self):

        self.assertEqual(self.response_post.status_code, 201)        
