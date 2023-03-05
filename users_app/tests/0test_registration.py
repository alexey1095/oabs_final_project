from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .. models import Patient
from django.contrib.auth.models import Group

from users_app.models_factory import DoctorFactory


class TestRegistrationView(TestCase):

    good_url = reverse('users_app:registration_page')

    response = None

    def setUp(self):
       


        patients_group = Group()
        patients_group.name = 'patients'
        patients_group.save()
        
        
        # self.doctor1 = DoctorFactory.create()
        # self.doctor2 = DoctorFactory.create()
       

    def teardown(self):
        #self.client.logout()
        Patient.objects.all().delete()
        User.objects.all().delete()

    def test_registrationViewReturnSuccess(self):

        response = self.client.get(self.good_url)
        self.assertEqual(response.status_code, 200)

    def test_registration(self):

        user_data = {'username': 'patient0',
                     'password1': 'vjfng8!ekrtjvf<KKS',
                     'password2': 'vjfng8!ekrtjvf<KKS',
                     'first_name': 'patient0_first_name',
                     'last_name': 'patient0_last_name',
                     'dob':'01/05/2000',
                     'home_address':'patient0_home_address',
                     'home_phone':'0123456789',
                     'submit':'Submit'}
        

        response = self.client.post(self.good_url, data=user_data, follow=True)
        user = User.objects.get(username='patient0')

        self.assertEqual(user.username, 'patient0')


       