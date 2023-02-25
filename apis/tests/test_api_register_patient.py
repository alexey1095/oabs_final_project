from rest_framework.test import APITestCase
from django.urls import reverse
import json

from users_app.models_factory import PatientFactory
from users_app.models_factory import DoctorFactory
from users_app.models_factory import DoctorTypeFactory
from users_app.models_factory import UserFactory


from django.contrib.auth.models import User
from users_app.models import Patient

from appointments_app.models_factory import AppointmentFactory

from ..serializers import *

from datetime import datetime

from django.contrib.auth.models import Group


class RegisterPatientAPITest(APITestCase):

    ''' Example of response


    '''

    good_url = reverse('apis:register_patient')

    def setUp(self):

        patients_group = Group()
        patients_group.name = 'patients'
        patients_group.save()

        self.good_post_data = {'user': {'username': 'patient0',
                                        'password': 'vjfng8!ekrtjvf<KKS',
                                        'first_name': 'patient0_first_name',
                                        'last_name': 'patient0_last_name'},
                               'dob': '2000-01-01',
                               'home_address': 'patient0_home_address',
                               'home_phone': '0123456789',
                               }
        
        self.bad_post_data = {'user': {'username': 'patient123'}}

        self.response_post = self.client.post(
            self.good_url, self.good_post_data, format='json')
        self.response_post.render()

    def tearDown(self):

        Patient.objects.all().delete()
        User.objects.all().delete()


    def test_apiPatientRegistartionReturnSuccess(self):
    

        self.assertEqual(self.response_post.status_code, 201)

    # def test_apiNumberAppointmentBooked(self):
    #     self.assertEqual(len(self.data), 2)

        #
    
    def  test_apiPatientRegistrationReturnAllDataCorrect(self):

        data=json.loads(self.response_post.content)

        self.assertEqual(data['user']['username'], 'patient0')
        self.assertEqual(data['user']['first_name'], 'patient0_first_name')
        self.assertEqual(data['user']['last_name'], 'patient0_last_name')
        self.assertEqual(data['dob'], '2000-01-01')
        self.assertEqual(data['home_address'], 'patient0_home_address')
        self.assertEqual(data['home_phone'], '0123456789')





        
    def test_apiPatientRegistartionReturnFailOnBadRequest(self):

     
        self.response_post = self.client.post(
            self.good_url, self.bad_post_data, format='json')
        self.response_post.render()

    

        self.assertEqual(self.response_post.status_code, 400)

