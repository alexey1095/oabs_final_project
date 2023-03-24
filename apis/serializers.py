from rest_framework import serializers
from django.contrib.auth.models import User
from appointments_app.models import Appointment
from users_app.models import Doctor
from users_app.models import Patient
from users_app.models import DoctorType
from appointments_app.models import DaysOff
from appointments_app.models import WishList
from django.contrib.auth.models import Group

from django.contrib.auth import authenticate


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



class RegisterNewUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password','first_name', 'last_name']

class RegisterNewPatientSerializer(serializers.ModelSerializer):


    user = RegisterNewUserSerializer()

    class Meta:
        model = Patient
        fields= ['user','dob', 'home_address', 'home_phone']


    def create(self, validated_data):
        #user = User(validated_data['user'])
        user = User.objects.create_user(
            username= validated_data['user']['username'],
            password = validated_data['user']['password'],
            first_name = validated_data['user']['first_name'],
            last_name=validated_data['user']['last_name'])
        #user.save()
        
        # adding a new user to a 'patients' group
        patients_group = Group.objects.get(name='patients') 
        user.groups.add(patients_group)
        user.save()

        patient=Patient(
            user=user, 
            dob = validated_data['dob'],
            home_address = validated_data['home_address'],
            home_phone = validated_data['home_phone'])
        patient.save()
        return patient
    


class RequestDaysOffSerializer(serializers.ModelSerializer):
    ''' Days off serialiser'''
    # date_time_from = forms.DateTimeField()
    # date_time_till = forms.DateTimeField() #(attrs={'type': 'datetime-local'})

    class Meta:
        model = DaysOff
        fields = ['doctor','date_from', 'date_till']





class AddToWishListSerializer(serializers.ModelSerializer):
    ''' Add to wishlist serialiser '''

    class Meta:
        model = WishList
        fields = ['patient', 'doctor', 'appointment_date', 'symptoms']


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=150, write_only=True)
    password = serializers.CharField(max_length=150, write_only=True)
    

    class Meta:
        # model = User
        fields = ['username', 'password']
        #read_only_fields = ('username', 'password')


    def validate(self,data):

        cleaned_data = super().validate(data)

        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
           
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:               
                raise serializers.ValidationError('Access denied: not valid username or password.', code='authorization')
        else:
            
            raise serializers.ValidationError("Either username or password is missing", code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        data['user'] = user
        return data


        # username = data.get('username')
        # password = data.get('password')


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

    

