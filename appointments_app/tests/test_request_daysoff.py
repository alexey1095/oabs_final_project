from django.test import TestCase
from django.urls import reverse

from users_app.models_factory import DoctorFactory
from appointments_app.models_factory import DaysOffStatusFactory
from users_app.models import Doctor
from ..models import DaysOff
from django.contrib.auth.models import User
from django.db.models import Q

class TestRequestDaysOff(TestCase):

    good_url = reverse('appointments_app:request_daysoff')

    response = None

    def setUp(self):
        
        self.doctor1 = DoctorFactory.create()
        DaysOffStatusFactory.create(status='Booked')     
        

    def teardown(self):
        self.client.logout()
        Doctor.objects.all().delete()
        User.objects.all().delete()

    def test_requestDaysOffViewReturnSuccess(self):

        response = self.client.get(self.good_url)
        self.assertEqual(response.status_code, 200)

    def test_requestDaysOffViewUseCorrectTemplate(self):
        self.assertTemplateUsed(self.response, 'request_daysoff.html')


    def test_requestDaysOffPOST(self):

        login_status=self.client.login(username=self.doctor1.user.username, password='fnfh!djdf8JJDSlfkd.sofidold73')

        date_from = '2023-04-20'
        date_to = '2023-04-25'

        data = {'date_from': date_from,
                     'date_till': date_to,
                     'submit':'Submit'}
        

        response = self.client.post(self.good_url, data=data, follow=False)
        
        daysoff = DaysOff.objects.get(
            Q(date_time_from=date_from),
            Q(date_time_till= date_to)
            )

        self.assertEqual(daysoff.doctor, self.doctor1)

      