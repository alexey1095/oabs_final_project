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
        DaysOffStatusFactory.create(status='Cancelled')

        login_status = self.client.login(
            username=self.doctor1.user.username, password='fnfh!djdf8JJDSlfkd.sofidold73')

        self.date_from = '2023-04-20'
        self.date_to = '2023-04-25'

        data = {'date_from': self.date_from,
                'date_till': self.date_to,
                'submit': 'Submit'}

        self.response = self.client.post(self.good_url, data=data, follow=True)

        self.daysoff = DaysOff.objects.get(
            Q(date_from=self.date_from),
            Q(date_till=self.date_to)
        )

    def teardown(self):
        self.client.logout()
        DaysOff.objects.all().delete()
        Doctor.objects.all().delete()
        User.objects.all().delete()

    def test_requestDaysOffViewReturnSuccess(self):

        response = self.client.get(self.good_url)
        self.assertEqual(response.status_code, 200)

    def test_requestDaysOffViewUseCorrectTemplate(self):
        response = self.client.get(self.good_url)
        self.assertTemplateUsed(response, 'request_daysoff.html')

    def test_requestDaysOffPOST(self):       

        self.assertEqual(self.daysoff.doctor, self.doctor1)

    def test_cancel_daysOffReturnSuccess(self):

        pk = self.daysoff.pk
        cancel_url = reverse(
            'appointments_app:cancel_daysoff', kwargs={'pk': pk})

        response = self.client.get(cancel_url)

        daysoff = DaysOff.objects.get(
            Q(date_from=self.date_from),
            Q(date_till=self.date_to))
        
        self.assertEqual(daysoff.daysoff_status.status, 'Cancelled')


    def test_cancelDaysOffRedirectToCorrectURL(self):
        pk = self.daysoff.pk
        cancel_url = reverse(
            'appointments_app:cancel_daysoff', kwargs={'pk': pk})

        response = self.client.get(cancel_url)
        self.assertRedirects(
            self.response, 
            reverse("appointments_app:request_daysoff"))


    def test_templateContent(self):

        self.assertContains(self.response, "function checkform()")
        self.assertContains(
            self.response, "<form id='date_time_form' method='post'>")
