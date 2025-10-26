from django.shortcuts import render
from django.utils import timezone
import random
from django.http import JsonResponse
from datetime import date
from services.models import ServicesList
from appointments.models import Appointments

# Create your views here.


def index(request):
    """
    A view of random services to highlight
    on the homepage
    """
    items = list(ServicesList.objects.all())

    sample_size = min(len(items), 2)

    if sample_size > 0:
        random_items = random.sample(items, sample_size)
    else:
        random_items = []

    context = {
        'random_services': random_items
    }

    return render(request, 'home/index.html', context)


def closest_appointment(request):
    """
    A view to display the closest appointment in time to the user
    """
    user = request.user

    current_date = timezone.localdate()

    future_bookings = Appointments.objects.filter(
        appointment_date__gte=current_date
    )

    closest_appointment = None

    if user.is_authenticated:
        future_bookings = future_bookings.filter(user=user)

        closest_appointment = future_bookings.order_by(
            'appointment_date',
            'appointment_time',
        ).first()
    
    context = {
        'closest_appointment': closest_appointment,
    }

    return render(request, 'home/index.html', context)


def calendar_feed(request):
    appointments = Appointments.objects.all()

    if request.user.is_staff:
        events = []
        for appointment in appointments:
            appointment_date = appointment.appointment_date
            appointment_time = appointment.appointment_time

            events.append({
                'title': f"{appointment.service.name} at {appointment_time}",
                'start': appointment_date.strftime('%Y-%m-%d'),
                'display': 'background',
                'color': '#07393C',
            })

        return JsonResponse(events, safe=False)

    else:
        events = []
        for appointment in appointments:
            appointment_date = appointment.appointment_date
            appointment_time = appointment.appointment_time

            events.append({
                'title': 'Booked',
                'start': appointment_date.strftime('%Y-%m-%d'),
                'time': appointment_time,
                'display': 'background',
                'color': '#07393C',
            })

        return JsonResponse(events, safe=False)


