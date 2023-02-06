from rest_framework import serializers
from appointments_app.models import Appointment
from users_app.models import Doctor
from users_app.models import DoctorType
from django.contrib.auth.models import User


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):

    #type = serializers.SerializerMethodField(source='doctor.type')

    class Meta:
        model = User
        # fields = ['first_name', 'last_name']
        fields = ['first_name', 'last_name'] #, 'type']


class DoctorTypeSerializer(serializers.ModelSerializer):

    #type = serializers.SerializerMethodField(source='doctor.type')

    class Meta:
        model = DoctorType
        # fields = ['first_name', 'last_name']
        fields = ['type'] #, 'type']



class DoctorSerializer(serializers.ModelSerializer):
    doctor_name= UserSerializer(source='user')
    details= DoctorTypeSerializer(source='type')
    # doctor_name = UserSerializer(source='user')
    #first_name = serializers.SerializerMethodField(source='user.first_name_set')

    #type = serializers.SerializerMethodField(source='doctortype')

    class Meta:
        model = Doctor
        fields = ['pk', 'doctor_name', 'details']
        #fields = ['pk', 'first_name']



class BookedAppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model= Appointment
        fields = "__all__"