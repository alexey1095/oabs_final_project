from datetime import datetime
from django.test import TestCase
from django.urls import reverse

from users_app.models_factory import PatientFactory
from users_app.models_factory import DoctorFactory
from appointments_app.models_factory import WishListStatusFactory
from appointments_app.models_factory import AppointmentStatusFactory
from appointments_app.models_factory import AppointmentFactory
from appointments_app.models import WishListStatus

#from appointments_app.models_factory import
from users_app.models import Doctor
from users_app.models import Patient
from ..models import AppointmentStatus
from ..models import Appointment
from ..models import WishList
from django.contrib.auth.models import User
from django.db.models import Q

class TestWishList(TestCase):

    good_url = reverse('appointments_app:add_to_wishlist')

    response = None

    def setUp(self):
        
        self.patient1 = PatientFactory.create()
        self.patient2 = PatientFactory.create()
        self.doctor1 = DoctorFactory.create()
        WishListStatusFactory.create(status='Waiting')     
        WishListStatusFactory.create(status='Available')
        WishListStatusFactory.create(status='Booked')

        AppointmentStatusFactory.create(status='Requested')    
        AppointmentStatusFactory.create(status='Confirmed')
        AppointmentStatusFactory.create(status='Cancelled_by_patient')       

        self.appointment = AppointmentFactory(patient =self.patient1,
                                              doctor=self.doctor1,
                                              appointment_date = datetime(2022,1,20,7,0))
        

        self.appointment_date = '2022-01-20T07:00'

        

        data = {'doctor': self.doctor1.pk,
                'appointment_date': self.appointment_date,
                'symptoms': "test_symptoms",
                'submit': 'Submit'}
        

        self.client.login(username=self.patient1.user.username,
                          password='fnfh!djdf8JJDSlfkd.sofidold73')
        

        self.response = self.client.post(self.good_url, data=data, follow=True)

        self.wishlist_entry = WishList.objects.get(
            doctor=self.doctor1,
            appointment_date=self.appointment_date,
            symptoms="test_symptoms"            
            )



        
        

    def teardown(self):
        self.client.logout()
        AppointmentStatus.objects.all().delete()
        Appointment.objects.all().delete()
        Patient.objects.all().delete()
        Doctor.objects.all().delete()
        User.objects.all().delete()
        WishListStatus.objects.all().delete()
        WishList.objects.all().delete()

    def test_wishListReturnGetNotAllowed(self):

        response = self.client.get(self.good_url)
        self.assertEqual(response.status_code, 405)


    def test_addTimeSlotToWishList(self):

       

        self.assertEqual(self.wishlist_entry.wishlist_status.status, 'Waiting')
        self.assertEqual(self.wishlist_entry.doctor, self.doctor1)


    def test_wishlistEntryChangeStatusToAvailbleCorrectly(self):

        # cancelled_status = AppointmentStatus.objects.get(
        #     status='Cancelled_by_patient')

        # self.appointment.appointment_status=cancelled_status

        data = {'doctor': self.doctor1.pk,
                'appointment_date': self.appointment_date,               
                'submit': 'Submit'}
        
        self.response = self.client.post(reverse('appointments_app:cancel_appointment'), data=data, follow=True)

        # appointment = Appointment.objects.get(
        #     doctor=self.doctor1,
        #     appointment_date=self.appointment_date,
        #     symptoms="test_symptoms"            
        #     )               

        self.wishlist_entry = WishList.objects.get(
            doctor=self.doctor1,
            appointment_date=self.appointment_date,
            symptoms="test_symptoms"            
            )

        

        self.assertEqual(self.wishlist_entry.wishlist_status.status, 'Available')








    # def test_WishListEntryHasCorrectStatusWaiting(self):

    #     wishlist_entry = WishList.objects.get(
    #         doctor=self.doctor1,
    #         appointment_date=self.appointment_date,
    #         symptoms="test_symptoms"            
    #         )

                




    # def test_requestDaysOffViewUseCorrectTemplate(self):
        
    #     self.assertTemplateUsed(self.response, 'request_daysoff.html')


    # def test_requestDaysOffPOST(self):

    #     login_status=self.client.login(username=self.patient1.user.username, password='fnfh!djdf8JJDSlfkd.sofidold73')

    #     date_from = '2023-04-20'
    #     date_to = '2023-04-25'

    #     data = {'date_from': date_from,
    #                  'date_till': date_to,
    #                  'submit':'Submit'}
        

    #     response = self.client.post(self.good_url, data=data, follow=False)
        
    #     daysoff = DaysOff.objects.get(
    #         Q(date_time_from=date_from),
    #         Q(date_time_till= date_to)
    #         )

    #     self.assertEqual(daysoff.doctor, self.doctor1)
    #     #self.assertRedirects(response, '/accounts/login/?next=/sekrit/')

      