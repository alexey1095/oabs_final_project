from django import forms
from django.forms import ModelForm
from appointments_app.models import Appointment


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

    # appointment_date=forms.DateTimeField(input_formats=["%d-%m-%Y %H:%M"])

    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'symptoms']