from django.test import TestCase
from django.urls import reverse

from users_app.models_factory import DoctorFactory


class TestDoctorListView(TestCase):

    good_url = reverse('appointments_app:doctor_list_view')

    response = None

    def setUp(self):
        
        self.doctor1 = DoctorFactory.create()
        self.doctor2 = DoctorFactory.create()
        self.response = self.client.get(self.good_url)

    def teardown(self):
        pass

    def test_doctorListViewReturnSuccess(self):

        self.assertEqual(self.response.status_code, 200)

    def test_doctorListViewUseCorrectTemplate(self):
        self.assertTemplateUsed(self.response, 'list_doctors.html')
        # print(self.response.context['doctors_list'])

    def test_doctorListViewReturnsCorrectNumberDoctors(self):
        self.assertEqual(len(self.response.context['doctors_list']), 2)
       
