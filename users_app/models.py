from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(blank=False)
    home_address = models.CharField(max_length=256, blank=False)
    home_phone = models.CharField(max_length=20, blank=False)

class DoctorType(models.Model):
    """ Doctor's specialisation"""
    type = models.CharField(max_length=100, null=False)


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.ForeignKey(DoctorType, on_delete = models.PROTECT)





