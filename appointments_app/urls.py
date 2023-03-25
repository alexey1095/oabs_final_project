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

     # confirm an appointment
    path('confirm/', views.confirm_appointment, name='confirm_appointment'),

    # request daysoff
    path('request_daysoff/', views.request_daysoff, name='request_daysoff'),

    # cancel daysoff
    path('cancel_daysoff/<int:pk>/', views.cancel_daysoff, name='cancel_daysoff'),

     # book an appointment
    path('add_to_wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
]
