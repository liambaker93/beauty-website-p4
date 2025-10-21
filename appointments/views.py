from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import datetime, timedelta
from django.http import JsonResponse
from decimal import Decimal
from .models import Appointments
from .forms import BookingForm
from services.models import ServicesList


# Create your views here.

def appointmentsPage(request):
    """
    View that displays a full calendar to all users.
    Displays to staff a list of bookings made by all users.
    """
    user = request.user
    all_bookings = Appointments.objects.all().order_by(
        'appointment_date', 'appointment_time')
    user_bookings = Appointments.objects.filter(user=user).order_by(
        'appointment_date', 'appointment_time')
    template = 'appointments/appointments.html'

    if user.is_authenticated:
        if user.is_staff:
            context = {
                'bookings': all_bookings,
            }
        else:
            context = {
                'bookings': user_bookings,
            }
        return render(request, template, context)


def fullCalendar(request):

    return render(request, 'appointments/calendar_detail.html')


def viewOrders(request):
    """
    Returns a list of the appointments currently being booked by the user
    """
    return render(request, 'appointments/user_order.html')


def addAppointment(request, service_id):
    """
    Adds a service to the user's order, and then handles payment
    """


def bookingConfirmation(request, booking_id):
    """
    Handles displaying the booking confirmation page generated
    via the new uuid from bookings
    """
    booking = get_object_or_404(Appointments, booking_id=booking_id)

    context = {
        'booking': booking,
        'booking_id': booking_id,
    }

    template = 'appointments/booking_confirmed.html'

    return render(request, template, context)


def calendar_events(request):
    """
    Handles displaying booking info within the calendar detail page.
    The view seperates what users are able to see based
    on their account privilege.
    Users can see their own bookings only, staff users and above
    can see all bookings being made.
    Unauthenticated users (guests) can see no bookings made.
    """
    start_date_str = request.GET.get('start')
    end_date_str = request.GET.get('end')

    if not request.user.is_authenticated:
        return JsonResponse([], safe=False)

    user = request.user
    is_staff = user.is_authenticated and user.is_staff

    try:
        start_date = datetime.fromisoformat(start_date_str.replace
                                            ('Z', '+00:00'))
        end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))
    except (ValueError, TypeError):
        return JsonResponse([], safe=False)

    bookings_queryset = Appointments.objects.filter(
        appointment_date__gte=start_date.date(),
        appointment_date__lt=end_date.date(),
    )

    if not is_staff and user.is_authenticated:
        bookings_queryset = bookings_queryset.filter(user=user)
    elif not user.is_authenticated:
        return JsonResponse([], safe=False)

    events = []
    for booking in bookings_queryset:

        start_datetime = datetime.combine(
            booking.appointment_date, booking.appointment_time)
        end_datetime = start_datetime + timedelta(hours=0.75)

        events.append({
            'title': f"Booked: {booking.service.name}.",
            'start': start_datetime.isoformat(),
            'end': end_datetime.isoformat(),
        })

    return JsonResponse(events, safe=False)
