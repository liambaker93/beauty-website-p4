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
        max_digits=6, decimal_places=2, null=False)
    booking_id = models.UUIDField(primary_key=True,
                                  default=uuid.uuid4, editable=False,
                                  unique=True)
    final_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0, editable=False)
    stripe_session_id = models.CharField(max_length=250, null=True, blank=True)
    payment_status = models.CharField(
        max_length=20,
        default='PENDING',
        choices=(
            ('PENDING', 'Pending Payment'),
            ('BALANCE', 'Paid'),
            ('FAILED', 'Failed/Expired'),
            ('DEPOSIT', 'Partial Paid'),
        )
    )

    class Meta:
        verbose_name_plural = 'Appointments'
        unique_together = ('service', 'appointment_date', 'appointment_time')
        ordering = ['-appointment_date', '-appointment_time']

    def __str__(self):
        return f"{self.service.name} on {self.appointment_date} at\
        {self.appointment_time}"

    def _calculate_deposit(self, full_price):
        if full_price is None:
            return 0
        
        deposit = round(full_price / 2)
        return deposit
    
    def save(self, *args, **kwargs):
        full_price = self.service.price

        if not self.pk or (self.deposit_cost == 0) and full_price is not None:
            self.deposit_cost = self._calculate_deposit(full_price)

            self.final_cost = full_price - self.deposit_cost

            if self.final_cost < 0:
                self.final_cost = 0

        super().save(*args, **kwargs)
        

