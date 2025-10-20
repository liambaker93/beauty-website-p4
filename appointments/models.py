from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.


class Appointments(models.Model):

    service = models.ForeignKey(
        'services.ServicesList', on_delete=models.CASCADE)
    appointment_time = models.TimeField(blank=False, null=False)
    appointment_date = models.DateField(blank=False, null=False)
    booking_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=True)
    user_name = models.CharField(
        max_length=96, blank=False, null=False, default='Guest')
    user_email = models.EmailField(max_length=254, null=False, blank=True)
    user_phone = models.CharField(null=True, max_length=20, blank=True)
    deposit_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0)
    booking_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        verbose_name_plural = 'Appointments'
        unique_together = ('service', 'appointment_date', 'appointment_time')
        ordering = ['-appointment_date', '-appointment_time']

    def __str__(self):
        return f"{self.service.name} on {self.appointment_date} at\
        {self.appointment_time}"

    def deposit_cost_calc(self):
        deposit_percentage = 0.10

        return self.service.price * deposit_percentage
    
    def total_service_cost(self):

        return self.service.price
