from django.db import models
from services.models import ServicesList
from django.contrib.auth.models import User

# Create your models here.


class Appointments(models.Model):

    service = models.ForeignKey(ServicesList, on_delete=models.CASCADE, related_name='appointments')
    appointment_time = models.TimeField()
    appointment_date = models.DateField()
    booking_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=96, blank=True, null=True)
 
