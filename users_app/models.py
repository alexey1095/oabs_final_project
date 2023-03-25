from django.db import models
from django.contrib.auth.models import User

# Data seeding: two groups of users have to be created namely  doctors and patients

class Patient(models.Model):
    ''' Store the patient details'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(blank=False)
    home_address = models.CharField(max_length=256, blank=False)
    home_phone = models.CharField(max_length=20, blank=False)
    
    # set to false by default as medical staff should confirm registration
    registered_status = models.BooleanField(default=False, blank=False)

    def __str__(self):
        return f'{self.user.username}'


class DoctorType(models.Model):
    """ Doctor's specialisation"""
    type = models.CharField(max_length=100, null=False)

    # Data seeding: GP, paediatrician

    def __str__(self):
        return f'{self.type}'


class Doctor(models.Model):
    '''Store doctor details'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.ForeignKey(DoctorType, on_delete=models.PROTECT)
    licence_valid = models.BooleanField(blank=False)
    dob = models.DateField(blank=False)
    home_address = models.CharField(max_length=256, blank=False)
    home_phone = models.CharField(max_length=20, blank=False)

    def __str__(self):      
        return f'{self.user.username}'



