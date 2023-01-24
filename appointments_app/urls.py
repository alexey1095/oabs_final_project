from django.urls import path

from . import views


urlpatterns = [

    # return scedule for a given docotor for a given week
    path('', views.appointment_view, name='appointment_view'),

    path('api/calendar/<int:doctor_id>/<int:year>/<int:week_number>/',
        views.api_calendar, 
        name='api_calendar'
        ),

]
