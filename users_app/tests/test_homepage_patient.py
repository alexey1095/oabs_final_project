
from datetime import datetime
from django.test import TestCase
from django.urls import reverse
from django.test import Client

from users_app.models_factory import PatientFactory
from users_app.models_factory import DoctorFactory
from appointments_app.models_factory import WishListStatusFactory
from appointments_app.models_factory import AppointmentStatusFactory
from appointments_app.models_factory import DaysOffStatusFactory
from appointments_app.models import WishListStatus
from appointments_app.models import Appointment
from appointments_app.models import AppointmentStatus
from appointments_app.models import WishList

# from appointments_app.models_factory import
from users_app.models import Doctor
from users_app.models import Patient
# from ..models import DaysOff
from django.contrib.auth.models import User
from django.db.models import Q

from django.contrib.auth.models import Group


class TestHomePagePatient(TestCase):

    good_url = reverse('appointments_app:book_appointment')

    response = None

    def setUp(self):

        patients_group = Group()
        patients_group.name = 'patients'
        patients_group.save()

        self.patient1 = PatientFactory.create()
        self.patient1.user.groups.add(patients_group)

        self.patient2 = PatientFactory.create()
        self.doctor1 = DoctorFactory.create()
        WishListStatusFactory.create(status='Waiting')
        WishListStatusFactory.create(status='Available')
        WishListStatusFactory.create(status='Booked')

        DaysOffStatusFactory.create(status='Booked')
        DaysOffStatusFactory.create(status='Cancelled')

        AppointmentStatusFactory.create(status='Requested')
        AppointmentStatusFactory.create(status='Confirmed')
        AppointmentStatusFactory.create(status='Cancelled_by_patient')

        self.client.login(username=self.patient1.user.username,
                          password='fnfh!djdf8JJDSlfkd.sofidold73')

        self.date_now = datetime.now()
        # self.appointment_date =  datetime.now()#'2023-04-20'
        self.appointment_date = f'{self.date_now:%Y-%m-%d}' + " 07:20"
        # this is the same date but in different format
        self.booked_appointment = f'{self.date_now:%d-%m-%Y}' + " 07:20"

        self.availbale_appointment = f'{self.date_now:%d-%m-%Y}' + " 07:00"

        data = {'doctor': self.doctor1.pk,
                'appointment_date': self.appointment_date,
                'symptoms': "test_symptoms",
                'submit': 'Submit'}

        self.response = self.client.post(self.good_url, data=data, follow=True)

        self.client_doctor1 = Client()
        self.client_doctor1.login(username=self.doctor1.user.username,
                                  password='fnfh!djdf8JJDSlfkd.sofidold73')

        self.client_patient2 = Client()
        self.client_patient2.login(username=self.patient2.user.username,
                                   password='fnfh!djdf8JJDSlfkd.sofidold73')

    def teardown(self):
        self.client.logout()
        Patient.objects.all().delete()
        Doctor.objects.all().delete()
        Appointment.objects.all().delete()
        WishList.objects.all().delete()
        WishListStatus.objects.all().delete()
        User.objects.all().delete()
        

    def test_homePagePatientReturnSuccess(self):

        response_get = self.client.get(reverse(
            'users_app:home_page'))

        self.assertEqual(response_get.status_code, 200)

    def test_homePagePatientHasListOfAppointments(self):

        response_get = self.client.get(reverse(
            'users_app:home_page'))

        self.assertContains(
            response_get, "<th scope='col'>Appointment Date", html=True)

        # appointment = Appointment.objects.get(
        #     doctor=self.doctor1,
        #     appointment_date=self.appointment_date,
        #     symptoms="test_symptoms"
        # )

        # self.assertContains(
        #     response_get, "<td>"+f'appointment.appointment_date'+"</td>", html=True)

    def test_homePagePatientHasCorrectAppointmentRecord(self):

        response_get = self.client.get(reverse(
            'users_app:home_page'))

        appointment = Appointment.objects.get(
            doctor=self.doctor1,
            appointment_date=self.appointment_date,
            symptoms="test_symptoms"
        )

        self.assertContains(
            response_get, "<td>"+f'{appointment.appointment_date:%d/%m/%Y %H:%M}'+"</td>", html=True)

        self.assertContains(response_get, "<td>Requested</td>", html=True)

        self.assertContains(response_get, "Dr. " +
                            f'{self.doctor1.user.last_name}', html=True)
        


    
    def test_homePagePatientHasCorrectWishListRecord(self):

        WishList.objects.create(
            patient=self.patient1,
            doctor=self.doctor1,
            appointment_date=self.appointment_date,
            symptoms="test_symptoms"            
            )
        
        self.wishlist_entry = WishList.objects.get(            
            doctor=self.doctor1,
            appointment_date=self.appointment_date,
            symptoms="test_symptoms"            
            )
        
        response_get = self.client.get(reverse(
            'users_app:home_page'))
        
        self.assertContains(
            response_get, "<td>"+f'{self.wishlist_entry.appointment_date:%d/%m/%Y %H:%M}'+"</td>", html=True)
        
        self.assertContains(response_get, "<td>Waiting</td>", html=True)

        self.assertContains(response_get, "Dr. " +
                            f'{self.doctor1.user.last_name}', html=True)
        

    def test_homePagePatientUseCorrectTemplate(self):
        
        response_get = self.client.get(reverse(
            'users_app:home_page'))
        
        self.assertTemplateUsed(response_get, 'home_patient.html')
        
    #     url_confirm_appointment = reverse(
    #         'appointments_app:confirm_appointment')

    #     data = {'patient': self.patient1.pk,
    #             'appointment_date': self.appointment_date,
    #             'submit': 'Submit'}

    #     response = self.client_doctor1.post(
    #         url_confirm_appointment, data=data, follow=True)

    #     appointment = Appointment.objects.get(
    #         doctor=self.doctor1,
    #         appointment_date=self.appointment_date,
    #         symptoms="test_symptoms"
    #     )

    #     self.assertEqual(appointment.appointment_status.status, 'Confirmed')

    # def test_bookedAppointmentHasCorrectBlueColorForOwner(self):

    #     self.test_confirmAppointment()

    #     response_get = self.client.get(reverse(
    #         'appointments_app:send_week_calendar',
    #         kwargs={
    #             'doctor_id': self.doctor1.pk,
    #             'year': f'{self.date_now:%Y}',
    #             'week_number': self.date_now.isocalendar().week}))

    #     self.assertContains(response_get,
    #                         "<td class='table-primary' data-date="+"'" +
    #                         f'{self.booked_appointment}'+"'"+">07:20</td>",
    #                         html=True)

    # def test_bookedNonConfirmedAppointmentHasCorrectRedColorForNonOwner(self):

    #     #self.test_confirmAppointment()

    #     response_get = self.client_patient2.get(reverse(
    #         'appointments_app:send_week_calendar',
    #         kwargs={
    #             'doctor_id': self.doctor1.pk,
    #             'year': f'{self.date_now:%Y}',
    #             'week_number': self.date_now.isocalendar().week}))

    #     self.assertContains(response_get,
    #                         "<td class='table-danger' data-date="+"'" +
    #                         f'{self.booked_appointment}'+"'"+">07:20</td>",
    #                         html=True)

    # def test_bookedConfirmedAppointmentHasCorrectRedColorForNonOwner(self):

    #         self.test_confirmAppointment()

    #         response_get = self.client_patient2.get(reverse(
    #             'appointments_app:send_week_calendar',
    #             kwargs={
    #                 'doctor_id': self.doctor1.pk,
    #                 'year': f'{self.date_now:%Y}',
    #                 'week_number': self.date_now.isocalendar().week}))

    #         self.assertContains(response_get,
    #                             "<td class='table-danger' data-date="+"'" +
    #                             f'{self.booked_appointment}'+"'"+">07:20</td>",
    #                             html=True)

    # def test_bookAppointmentReturnGetNotAllowed(self):

    #     response = self.client.get(self.good_url)
    #     self.assertEqual(response.status_code, 405)

    # def test_bookAppointmentWorksCorrectly(self):

    #     appointment = Appointment.objects.get(
    #         doctor=self.doctor1,
    #         appointment_date=self.appointment_date,
    #         symptoms="test_symptoms"
    #     )

    #     self.assertEqual(appointment.doctor, self.doctor1)

    # def test_sendWeekCalendarReturnSuccess(self):

    #     response_get = self.client.get(reverse(
    #         'appointments_app:send_week_calendar',
    #         kwargs={
    #             'doctor_id': self.doctor1.pk,
    #             'year': f'{self.date_now:%Y}',
    #             'week_number': datetime.now().isocalendar().week}))

    #     self.assertEqual(response_get.status_code, 200)

    # def test_bookedAppointmentHasCorrectlyYellowColor(self):
    #     response_get = self.client.get(reverse(
    #         'appointments_app:send_week_calendar',
    #         kwargs={
    #             'doctor_id': self.doctor1.pk,
    #             'year': f'{self.date_now:%Y}',
    #             'week_number': self.date_now.isocalendar().week}))

    #     self.assertContains(response_get,
    #                         "<td class='table-warning' data-date="+"'" +
    #                         f'{self.booked_appointment}'+"'"+">07:20</td>",
    #                         html=True)

    #     # "<td class='table-warning' data-date="+self.appointment_date)
    #     # self.assertContains( response_get, "<td class='table-success' data-date='03-03-2023 07:00'>07:00</td>", html=True)#"<td class='table-warning' data-date="+self.appointment_date)

    #     # <td class=\'table-success\' data-date=\'03-03-2023 07:00\'>07:00</td>

    # def test_availbleAppointmentHasCorrectGreenColor(self):
    #     response_get = self.client.get(reverse(
    #         'appointments_app:send_week_calendar',
    #         kwargs={
    #             'doctor_id': self.doctor1.pk,
    #             'year': f'{self.date_now:%Y}',
    #             'week_number': self.date_now.isocalendar().week}))

    #     # "<td class='table-warning' data-date="+self.appointment_date)
    #     # self.assertContains(
    #     #     response_get, "<td class='table-success' data-date='03-03-2023 07:00'>07:00</td>", html=True)
    #     # self.assertContains( response_get, "<td class='table-success' data-date='03-03-2023 07:00'>07:00</td>", html=True)#"<td class='table-warning' data-date="+self.appointment_date)

    #     # <td class=\'table-success\' data-date=\'03-03-2023 07:00\'>07:00</td>

    #     self.assertContains(response_get,
    #                         "<td class='table-success' data-date="+"'" +
    #                         f'{self.availbale_appointment}'+"'"+">07:00</td>",
    #                         html=True)

    # def test_bookAppointmentHTTPRedicrectCorrect(self):
    #     self.assertRedirects(
    #         self.response,
    #         reverse("appointments_app:appointment_view",
    #                 args=(self.doctor1.pk,))
    #     )

    # def test_cancelAppointmentWorksCorrectly(self):

    #     data = {'doctor': self.doctor1.pk,
    #             'appointment_date': self.appointment_date,
    #             'submit': 'Submit'}

    #     self.response = self.client.post(
    #         reverse('appointments_app:cancel_appointment'), data=data, follow=True)

    #     appointment = Appointment.objects.get(
    #         doctor=self.doctor1,
    #         appointment_date=self.appointment_date,
    #         symptoms="test_symptoms"
    #     )

    #     self.assertEqual(appointment.appointment_status.status,
    #                      'Cancelled_by_patient')

    # def test_templateContent(self):

    #     self.assertContains(
    #         self.response, "if (cell.className == 'table-success')")
    #     self.assertContains(self.response, "Next Week")

    # def test_daysOffHasCorrectGreyColor(self):
    #     self.date_from = f'{self.date_now:%Y-%m-%d}'
    #     self.date_to = f'{self.date_now:%Y-%m-%d}'

    #     data = {'date_from': self.date_from,
    #             'date_till': self.date_to,
    #             'submit': 'Submit'}

    #     self.response = self.client_doctor1.post(reverse('appointments_app:request_daysoff'), data=data, follow=True)

    #     response_get = self.client.get(reverse(
    #         'appointments_app:send_week_calendar',
    #         kwargs={
    #             'doctor_id': self.patient1.pk,
    #             'year': f'{self.date_now:%Y}',
    #             'week_number': self.date_now.isocalendar().week}))

    #     self.assertContains(response_get,
    #                         "<td class='table-secondary' data-date="+"'" +
    #                         f'{self.booked_appointment}'+"'"+">07:20</td>",
    #                         html=True)
