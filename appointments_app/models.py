from django.db import models
from users_app.models import Patient
from users_app.models import Doctor
from django.db.models import Q
# Create your models here.


class AppointmentStatus(models.Model):
    status = models.CharField(max_length=256, blank=False, unique=True)

    def __str__(self):
        return f'{self.status}'


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField(blank=False)
    symptoms = models.CharField(max_length=256, blank=False)
    request_date = models.DateTimeField(blank=False, auto_now_add=True)
    appointment_status = models.ForeignKey(
        AppointmentStatus, on_delete=models.CASCADE, to_field='status', default='Requested')

    class Meta:

        constraints = [models.UniqueConstraint(
            fields=['doctor', 'appointment_date', 'appointment_status'], 
            condition=Q(appointment_status='Requested') | Q(appointment_status='Confirmed'), 
            name='unique_appointment')]

    def __str__(self):
        return f'{self.appointment_date} {self.doctor}'
