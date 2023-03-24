from rest_framework.test import APITestCase
from django.urls import reverse
import json

from users_app.models_factory import PatientFactory
from users_app.models_factory import DoctorFactory
from users_app.models_factory import DoctorTypeFactory
from users_app.models_factory import UserFactory

from ..serializers import *


class DoctorListAPITest(APITestCase):

    
    good_url = reverse('apis:doctor_list')

    def setUp(self):

        self.doctor1 = DoctorFactory.create()
        self.doctor2 = DoctorFactory.create()
        self.doctor3 = DoctorFactory.create()

        self.patient1 = PatientFactory.create()       

        self.client.login(username=self.patient1.user.username,
                          password='fnfh!djdf8JJDSlfkd.sofidold73')

        self.response = self.client.get(self.good_url, format='json')
        self.response.render()
        self.data = json.loads(self.response.content)

        

    def tearDown(self):
        self.client.logout()
        User.objects.all().delete()
        DoctorType.objects.all().delete()
        Doctor.objects.all().delete()

        UserFactory.reset_sequence(0)
        DoctorTypeFactory.reset_sequence(0)
        DoctorFactory.reset_sequence(0)

    def test_apiDoctorListReturnSuccess(self):

        self.assertEqual(self.response.status_code, 200)

        #

    def test_apiNumberDoctorIsCorrect(self):
        self.assertEqual(len(self.data), 3)

    def test_apiDataIsCorrect(self):
        self.assertEqual(self.data[0]['doctor_name']
                         ['first_name'], 'first_name_0')
        self.assertEqual(self.data[1]['doctor_name']
                         ['last_name'], 'last_name_1')
        self.assertEqual(self.data[2]['details']['type'], 'doctor_type_2')

    def test_apiDoctorListAllKeysArePresent(self):

        self.assertEqual(set(self.data[0].keys()), set(
            ['pk', 'doctor_name', 'details']))
