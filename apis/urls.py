from django.urls import path
from rest_framework.schemas import get_schema_view
from apis import views

app_name = 'apis'

urlpatterns = [

    # return a list of doctors
     path('doctors/',
         views.doctor_list,
         name='doctor_list'),

    # return a list of booked appointments for a given doctor, year and week number
     path('list_booked_appointments/<int:doctor_id>/<int:year>/<int:week_number>/',
         views.booked_appointments_list,
         name='list_booked_appointments'),


    # end point to book an apointment
     path('book_appointment/',
         views.book_appointment,
         name='book_appointment'),

    # end point to confirm an apointment
     path('confirm_appointment/<int:appointment_id>/',
         views.confirm_appointment,
         name='confirm_appointment'),

    # end point to register
     path('register_patient',
         views.register_patient,
         name='register_patient'),

     # end point to confirm an apointment
     # path('login',
     #     views.login,
     #     name='api_login'),

    # end point to request daysoff
    path('request_daysoff/',
         views.request_daysoff,
         name='request_daysoff'),


    # end point to add to wishlist
     path('add_to_wishlist/',
         views.add_to_wishlist,
         name='add_to_wishlist'),

    # API schema
     path('schema/',
         get_schema_view(
             title='Appointment REST API',
             description='API for interacting with online booking appointment system.',
             version='1.0'
         ),
         name='schema_view'),
]
