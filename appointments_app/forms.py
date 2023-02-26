from django import forms
from django.forms import ModelForm
from appointments_app.models import Appointment
from appointments_app.models import DaysOff


# class AppointmentForm1(ModelForm):
#     class Meta:
#         model = Appointment
#         fields = ['symptoms']


# class AppointmentForm2(ModelForm):
#     class Meta:
#         model = Appointment
#         fields = ['pub_date', 'headline', 'content', 'reporter']


# class SymptomsForm(ModelForm):
#     symptoms = forms.CharField(widget=forms.Textarea(
#         # attrs={
#         #     'hidden': '',
#         # }
#     ))

#     class Meta:
#         model = Appointment
#         fields = ['symptoms']

# class DoctorAndAppointmentDateForm(ModelForm):
#     doctor = forms.IntegerField(
#         widget=forms.HiddenInput(),
#         required = True)

#     appointment_date = forms.DateTimeField(
#         widget=forms.HiddenInput(),
#         required = True)

#     class Meta:
#         model = Appointment
#         fields = ['doctor', 'appointment_date']


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



# class RequestDaysOffForm(forms.Form):
#     ''' Days off form'''
#     date_time_from = forms.DateTimeField()
#     date_time_till = forms.DateTimeField() #(attrs={'type': 'datetime-local'})
    
class RequestDaysOffForm(ModelForm):
    ''' Days off form'''
    # date_time_from = forms.DateTimeField()
    # date_time_till = forms.DateTimeField() #(attrs={'type': 'datetime-local'})

    class Meta:
        model = DaysOff
        fields = ['date_from', 'date_till']

    