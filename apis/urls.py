from django.urls import path
from apis import views

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
]
