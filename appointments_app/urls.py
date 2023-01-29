from django.urls import path

from . import views


urlpatterns = [

    # return week calendar for a given doctor for a given week
    path('', views.appointment_view, name='appointment_view'),

    # this url is to be accessed via XMLHttpRequest from the webpage
    path('calendar/<int:doctor_id>/<int:year>/<int:week_number>/',
        views.calendar_view, 
        name='calendar_view'
        ),

]
