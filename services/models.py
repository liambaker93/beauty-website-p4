from django.db import models
import datetime

# Create your models here.


class ServiceCategory(models.Model):

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=96)

    def __str__(self):
        return self.name


class ServicesList(models.Model):

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    name = models.CharField(primary_key=True, max_length=256, blank=True, default='Treatment')
    category = models.ForeignKey(ServiceCategory, null=True, blank=True, on_delete=models.SET_NULL)
    timeframe = models.DurationField(default=datetime.timedelta(minutes=45))
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    description = models.CharField(max_length=512, blank=True, null=True)

    def __str__(self):
        return self.name
