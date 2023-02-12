from rest_framework import serializers
from django.contrib.auth.models import User
from appointments_app.models import Appointment
from users_app.models import Doctor
from users_app.models import DoctorType


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class DoctorTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DoctorType
        fields = ['type']


class DoctorSerializer(serializers.ModelSerializer):
    doctor_name = UserSerializer(source='user')
    details = DoctorTypeSerializer(source='type')

    class Meta:
        model = Doctor
        fields = ['pk', 'doctor_name', 'details']


class BookedAppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = ["appointment_date", "doctor"]


class NewAppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = ["appointment_date", "symptoms", "patient", "doctor"]
