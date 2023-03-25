from datetime import datetime
import factory
import factory.fuzzy
from appointments_app.models import Appointment
from appointments_app.models import AppointmentStatus
from appointments_app.models import DaysOffStatus
from appointments_app.models import WishListStatus
from appointments_app.models import WishList
from users_app.models_factory import PatientFactory
from users_app.models_factory import DoctorFactory


class AppointmentStatusFactory(factory.django.DjangoModelFactory):
    ''' Create model factory for AppointmentStatus model'''    

    status = factory.Iterator(['Requested','Confirmed'])

    class Meta:
        model = AppointmentStatus
        # the django_get_or_create methos is added here to avoid the UNIQUE constraint break
        # as discussed here https://joequery.me/code/factory-boy-handle-unique-constraints/
        django_get_or_create = ('status',)


class AppointmentFactory(factory.django.DjangoModelFactory):
    ''' Create model factory for Appointment model'''  

    patient = factory.SubFactory(PatientFactory)
    doctor = factory.SubFactory(DoctorFactory)
    
    appointment_status = factory.SubFactory(AppointmentStatusFactory, status='Requested')
    request_date = datetime.now()
    symptoms = factory.Sequence(lambda n: 'symptoms_%d' % n)

    class Meta:
        model = Appointment



class DaysOffStatusFactory(factory.django.DjangoModelFactory):
    ''' Create model factory for DaysOffStatus model'''    

    class Meta:
        model = DaysOffStatus
        # the django_get_or_create methos is added here to avoid the UNIQUE constraint break
        # as discussed here https://joequery.me/code/factory-boy-handle-unique-constraints/
        django_get_or_create = ('status',)



class WishListStatusFactory(factory.django.DjangoModelFactory):
    ''' Create model factory for WishListStatus model'''   

    class Meta:
        model = WishListStatus
        # the django_get_or_create methos is added here to avoid the UNIQUE constraint break
        # as discussed here https://joequery.me/code/factory-boy-handle-unique-constraints/
        django_get_or_create = ('status',)



class WishListFactory(factory.django.DjangoModelFactory):
    ''' Create model factory for WishList model'''
    
    patient = factory.SubFactory(PatientFactory)
    doctor = factory.SubFactory(DoctorFactory)
    wishlist_status = factory.SubFactory(AppointmentStatusFactory, status='Requested')
    request_date = datetime.now()
    symptoms = factory.Sequence(lambda n: 'symptoms_%d' % n)

    class Meta:
        model = WishList