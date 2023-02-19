from django.urls import path
from . import views


app_name = 'appointments_app'


urlpatterns = [

    # generate and show a list of doctors
    path('doctors/', views.doctor_list_view, name='doctor_list_view'),

    # return week calendar webpage for a given doctor for current week with next
    # and previous week buttons
    path('<int:doctor_id>/', views.appointment_view, name='appointment_view'),

    # generate and send week calendar --this url is to be accessed via
    # XMLHttpRequest from the week_calendar.html webpage
    path('calendar/<int:doctor_id>/<int:year>/<int:week_number>/',
         views.send_week_calendar,
         name='send_week_calendar'),

    # book an appointment
    path('book/', views.book_appointment, name='book_appointment'),

    # cancel an appointment
    path('cancel/', views.cancel_appointment, name='cancel_appointment'),
]
