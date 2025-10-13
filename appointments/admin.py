from django.contrib import admin
from .models import Appointments

# Register your models here.


class AppointmentsAdmin(admin.ModelAdmin):
    appointments_display = (
        'service',
        'appointment_time',
        'appointment_date',
        'booking_time',
        'user_name',
        'user_email',
        'deposit_cost',
        'booking_id',
        'id',
    )

    ordering = ('service',)

    readonly_fields = ('booking_id',)


admin.site.register(Appointments, AppointmentsAdmin)
