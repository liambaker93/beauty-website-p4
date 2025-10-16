from django import forms
from .models import Appointments
from decimal import Decimal


class BookingForm(forms.ModelForm):
    """
    A form used for users to book appointments
    """
    class Meta:
        model = Appointments
        fields = ('service', 'appointment_time', 'appointment_date',
                  'deposit_cost', 'user_name', 'user_email',
                  'user_phone')
