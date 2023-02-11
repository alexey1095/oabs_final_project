import factory

import factory.fuzzy

import django

from datetime import datetime


from django.contrib.auth.models import User
from users_app.models import Patient
from users_app.models import Doctor
from users_app.models import DoctorType

from appointments_app.models import Appointment
from appointments_app.models import AppointmentStatus

# https://factoryboy.readthedocs.io/en/stable/recipes.html

class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'username%d' % n)
    first_name = factory.Sequence(lambda n: 'first_name_%d' % n)
    last_name = factory.Sequence(lambda n: 'last_name_%d' % n)
    password = factory.Sequence(lambda n: 'password%d' % n)


class DoctorTypeFactory(factory.django.DjangoModelFactory):
    
    class Meta:
        model = DoctorType

    type = factory.Sequence(lambda n: 'doctor_type_%d' % n)

    


class DoctorFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Doctor

    user = factory.SubFactory(UserFactory)
    type = factory.SubFactory(DoctorTypeFactory)
    licence_valid = True
    dob = "2020-03-17"
    home_address = factory.Sequence(lambda n: 'home_address_%d' % n)
    home_phone = factory.Sequence(lambda n: 'home_phone_%d' % n)


class PatientFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Patient


    user = factory.SubFactory(UserFactory)
    dob = "2000-01-01"
    home_address = factory.Sequence(lambda n: 'patient_home_address_%d' % n)
    home_phone = factory.Sequence(lambda n: 'patient_home_phone_%d' % n)
    

class AppointmentStatusFactory(factory.django.DjangoModelFactory):
    

    class Meta:
        model = AppointmentStatus
        # https://joequery.me/code/factory-boy-handle-unique-constraints/
        django_get_or_create = ('status',)

    #status = factory.Sequence(lambda n: 'Requested_%d' % n)
    status='Requested'





class AppointmentFactory(factory.django.DjangoModelFactory):
    patient = factory.SubFactory(PatientFactory)
    doctor = factory.SubFactory(DoctorFactory)

    # datetime(year, month, day, hour, minute, second, microsecond)
    # b = datetime(2022, 12, 28, 23, 55, 59, 342380)
    #appointment_date = factory.fuzzy.FuzzyNaiveDateTime(start_dt=datetime(2022, 12, 28, 23, 55, 59))
    
    
    appointment_status = factory.SubFactory(AppointmentStatusFactory)
    request_date = datetime.now() #factory.fuzzy.FuzzyNaiveDateTime(start_dt=datetime(2022, 12, 28, 23, 55, 59))
    symptoms = factory.Sequence(lambda n: 'symptoms_%d' % n)

    class Meta:
        model = Appointment