from django.urls import path

from . import views


app_name = 'appointments_app'


urlpatterns = [

    path('doctors/', views.doctor_list_view, name='doctor_list_view'),

    # return week calendar for a given doctor for a given week
    path('<int:doctor_id>/', views.appointment_view, name='appointment_view'),

    # generate and send week calendar --this url is to be accessed via XMLHttpRequest from the week_calendar.html webpage
    path('calendar/<int:doctor_id>/<int:year>/<int:week_number>/',
         views.send_week_calendar,
         name='send_week_calendar'
         ),

    path('book/', views.book_appointment, name='book_appointment'),

    path('cancel/', views.cancel_appointment, name='cancel_appointment'),


]
