from django.test import TestCase
from django.urls import reverse

from users_app.models_factory import DoctorFactory


class TestDoctorListView(TestCase):

    good_url = reverse('appointments_app:doctor_list_view')

    response = None

    def setUp(self):
        
        self.doctor1 = DoctorFactory.create()
        self.doctor2 = DoctorFactory.create()

        self.client.login(username=self.doctor1.user.username,
                          password='fnfh!djdf8JJDSlfkd.sofidold73')

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

    def test_templateContent(self):
        self.assertContains(self.response, "<p2> List of Doctors </p2>")
        self.assertContains(self.response,"onClick = function(doctor_id,object)")
       
