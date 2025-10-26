from django.shortcuts import render
from django.utils import timezone
import random
from django.http import JsonResponse
from datetime import datetime, timedelta
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
    start_date_str = request.GET.get('start')
    end_date_str = request.GET.get('end')

    try:
        start_date = datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
        end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))
    except (ValueError, TypeError):
        return JsonResponse([], safe=False)
    
    bookings = Appointments.objects.filter(
        appointment_date__gte=start_date.date(),
        appointment_date__lt=end_date.date(),
    )

    if request.user.is_authenticated and not request.user.is_staff:
        bookings = bookings.filter(user=request.user)
    elif not request.user.is_authenticated:
        return JsonResponse([], safe=False)
    
    events = []
    for booking in bookings:
        start_datetime = datetime.combine(booking.appointment_date, booking.appointment_time)
        end_datetime = start_datetime + timedelta(hours=0.75)

        color = '#07393C' if request.user.is_staff else '#4CAF50'

        events.append({
            'title': f"{booking.service.name}",
            'start': start_datetime.isoformat(),
            'end': end_datetime.isoformat(),
            'color': color,
            'allDay': False,
        })

    return JsonResponse(events, safe=False)


