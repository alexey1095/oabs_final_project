from django import forms
from django.forms import ModelForm
from appointments_app.models import Appointment
from appointments_app.models import DaysOff
from appointments_app.models import WishList


class BookNewAppointment(ModelForm):
    ''' This form is for valdation data for booking appointment '''

    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'symptoms']


class CancelAppointment(ModelForm):
    ''' This form is for valdation data for cancelling appointment '''

    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date']


class ConfirmAppointment(ModelForm):
    ''' This form is for data validation for cancelling appointment '''

    class Meta:
        model = Appointment
        fields = ['patient', 'appointment_date']

    
class RequestDaysOffForm(ModelForm):
    ''' Days off form'''
   
    class Meta:
        model = DaysOff
        fields = ['date_from', 'date_till']


class AddToWishList(ModelForm):
    ''' This form is for valdation data for booking appointment '''

    class Meta:
        model = WishList
        fields = ['doctor', 'appointment_date', 'symptoms']
