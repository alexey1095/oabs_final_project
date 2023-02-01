from django.urls import path

from . import views


urlpatterns = [

    # return week calendar for a given doctor for a given week
    path('', views.appointment_view, name='appointment_view'),

    # generate and send week calendar --this url is to be accessed via XMLHttpRequest from the week_calendar.html webpage
    path('calendar/<int:doctor_id>/<int:year>/<int:week_number>/',
         views.send_week_calendar,
         name='send_week_calendar'
         ),

    path('book/', views.book_appointment, name='book_appointment'),

]
