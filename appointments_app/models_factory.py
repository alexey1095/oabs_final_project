import factory

import factory.fuzzy


from datetime import datetime

from appointments_app.models import Appointment
from appointments_app.models import AppointmentStatus

from users_app.models_factory import PatientFactory
from users_app.models_factory import DoctorFactory



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