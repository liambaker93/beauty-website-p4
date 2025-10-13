from django.shortcuts import render, redirect
from appointments.models import Appointments

# Create your views here.

def index(request):
    """
    This view generates the orders made by a user ready to display on the account page.
    """
    template = 'useraccount/account.html'
    if request.user.is_authenticated:
        user_appointments = Appointments.objects.filter(
            user=request.user
        ).select_related('service').order_by('appointment_date', 'appointment_time')

        context = {
            'appointments': user_appointments,
        }
        return render(request, template, context)
    else:
        return render(request, template)
