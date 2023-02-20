from rest_framework import serializers
from django.contrib.auth.models import User
from appointments_app.models import Appointment
from users_app.models import Doctor
from users_app.models import DoctorType
from appointments_app.models import AppointmentStatus



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
        fields = ["appointment_date", "doctor", "pk"]


class NewAppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = ["appointment_date", "symptoms", "patient", "doctor"]


class ConfirmAppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields= '__all__'
        #fields = ["appointment_date", "patient"]
        #fields = ["appointment_status"]

    # def update(self, instance, validated_data):
    #     """
    #     Update and return an existing `Snippet` instance, given the validated data.
    #     """

    # instance.email = validated_data.get('email', instance.email)
    #     instance.content = validated_data.get('content', instance.content)
    #     instance.created = validated_data.get('created', instance.created)
    #     instance.save()
    #     return instance


        

        
        
        
    #     instance.appointment_status = AppointmentStatus.objects.get(status='Confirmed')
    #     instance.save()
    #     return instance

    

