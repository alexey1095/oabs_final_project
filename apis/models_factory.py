import factory


from django.contrib.auth.models import User
from users_app.models import Patient
from users_app.models import Doctor
from users_app.models import DoctorType

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
    