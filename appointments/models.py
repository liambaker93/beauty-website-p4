from django.db import models
from services.models import ServicesList

# Create your models here.

## Needs migrating when finished, pls delete when migrated 

class Appointments(models.Model):

    name = models.ForeignKey(ServicesList, on_delete=models.PROTECT, related_name='appointments')
    appointment_time = models.DateTimeField()
