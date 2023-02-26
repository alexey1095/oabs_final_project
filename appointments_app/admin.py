from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(AppointmentStatus)
admin.site.register(Appointment)
admin.site.register(DaysOff)
admin.site.register(DaysOffStatus)
