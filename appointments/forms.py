from django import forms
from datetime import date
from .models import Appointments


class BookingForm(forms.ModelForm):
    """
    A form used for users to book appointments
    """
    TIME_CHOICES = (
        ('09:00', '9:00 AM'),
        ('10:00', '10:00 AM'),
        ('11:00', '11:00 AM'),
        ('12:00', '12:00 PM'),
        ('13:00', '1:00 PM'),
        ('14:00', '2:00 PM'),
        ('15:00', '3:00 PM'),
        ('16:00', '4:00 PM'),
        ('17:00', '5:00 PM'),
        ('18:00', '6:00 PM'),
    )

    appointment_time = forms.ChoiceField(
        choices=TIME_CHOICES,
        label="Select Appointment Time"
    )

    class Meta:
        model = Appointments
        fields = ('service', 'appointment_time', 'appointment_date',
                  'user_name', 'user_email',
                  'user_phone')
        widgets = {
            'appointment_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control date-input',
                    'min': date.today().isoformat(),
                }
            )
        }
