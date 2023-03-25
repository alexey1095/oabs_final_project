from django.db import models
from users_app.models import Patient
from users_app.models import Doctor
from django.db.models import Q

from django.utils import timezone


class AppointmentStatus(models.Model):
    ''' Store appointment status'''
    
    status = models.CharField(max_length=256, blank=False, unique=True)

    # Data seeding : Requested,Attended, Cancelled_by_patient,
    # DNA, Confirmed, Days_off

    def __str__(self):
        return f'{self.status}'


class Appointment(models.Model):
    '''Store appointment details'''
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField(blank=False)
    symptoms = models.CharField(max_length=256, blank=False)

    # The "timezone.now" has been added to avoid issue during testing as 
    # described here https://github.com/FactoryBoy/factory_boy/issues/102
    request_date = models.DateTimeField(default = timezone.now)
    appointment_status = models.ForeignKey(
        AppointmentStatus, on_delete=models.CASCADE, to_field='status', default='Requested')

    class Meta:

        constraints = [models.UniqueConstraint(
            fields=['doctor', 'appointment_date', 'appointment_status'], 
            condition=Q(appointment_status='Requested') | Q(appointment_status='Confirmed'), 
            name='unique_appointment')]

    def __str__(self):
        return f'{self.appointment_date} {self.doctor}'

class DaysOffStatus(models.Model):
    ''' DaysOff status '''
    status = models.CharField(max_length=256, blank=False, unique=True)

    # Data seeding: Cancelled, Booked

    def __str__(self):
        return f'{self.status}'


class DaysOff(models.Model):
    ''' Store details for daysoff model'''    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date_from = models.DateField(blank=False)
    date_till = models.DateField(blank=False)
    daysoff_status = models.ForeignKey(
        DaysOffStatus, on_delete=models.CASCADE, to_field='status', default='Booked')
    comment = models.CharField(max_length=256, blank=True)

    # The "timezone.now" is added to avoid issues during testing https://github.com/FactoryBoy/factory_boy/issues/102
    request_date = models.DateTimeField(default = timezone.now)
    
    class Meta:

        constraints = [models.UniqueConstraint(
            fields=['doctor', 'date_from', 'date_till'], 
            name='unique_daysoff_record')]

    def __str__(self):
        return f'{self.date_from} - {self.date_till} - {self.doctor}'


class WishListStatus(models.Model):
    ''' Store wishlist status'''
    status = models.CharField(max_length=256, blank=False, unique=True)

    # Data seeding: Booked, Availble, Waiting

    def __str__(self):
        return f'{self.status}'

class WishList(models.Model):
    ''' WishList details'''
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField(blank=False)
    symptoms = models.CharField(max_length=256, blank=False)

    # adopted from here https://github.com/FactoryBoy/factory_boy/issues/102
    request_date = models.DateTimeField(default = timezone.now)
    wishlist_status = models.ForeignKey(
        WishListStatus, on_delete=models.CASCADE, to_field='status', default='Waiting')

    class Meta:

        constraints = [models.UniqueConstraint(
            # patient is also included as the wishlist entry can be added by many patients
            fields=['patient','doctor', 'appointment_date', 'wishlist_status'], 
            condition=Q(wishlist_status='Waiting') | Q(wishlist_status='Available')| Q(wishlist_status='Booked'), 
            name='unique_wishlist_record')]

    def __str__(self):
        return f'{self.appointment_date} {self.doctor}'
