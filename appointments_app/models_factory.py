from datetime import datetime
import factory
import factory.fuzzy


from appointments_app.models import Appointment
from appointments_app.models import AppointmentStatus

from users_app.models_factory import PatientFactory
from users_app.models_factory import DoctorFactory


class AppointmentStatusFactory(factory.django.DjangoModelFactory):
    ''' Create model factory for AppointmentStatus model'''

    status = 'Requested'

    class Meta:
        model = AppointmentStatus
        # the django_get_or_create methos is added here to avoid the UNIQUE constraint break
        # as discussed here https://joequery.me/code/factory-boy-handle-unique-constraints/
        django_get_or_create = ('status',)


class AppointmentFactory(factory.django.DjangoModelFactory):
    ''' Create model factory for Appointment model'''

    patient = factory.SubFactory(PatientFactory)
    doctor = factory.SubFactory(DoctorFactory)
    appointment_status = factory.SubFactory(AppointmentStatusFactory)
    request_date = datetime.now()
    symptoms = factory.Sequence(lambda n: 'symptoms_%d' % n)

    class Meta:
        model = Appointment
