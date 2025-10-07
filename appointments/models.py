from django.db import models
from services.models import ServicesList
from django.contrib.auth.models import User
import uuid
# Create your models here.


class Appointments(models.Model):

    name = models.ForeignKey(ServicesList, on_delete=models.CASCADE)
    appointment_time = models.TimeField(blank=False, null=False)
    appointment_date = models.DateField(blank=False, null=False)
    booking_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    user_name = models.CharField(max_length=96, blank=False, null=False, default='Guest')
    user_email = models.EmailField(max_length=254, null=False, blank=True)
    user_phone = models.IntegerField(null=False, default=0, blank=False)
    deposit_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
