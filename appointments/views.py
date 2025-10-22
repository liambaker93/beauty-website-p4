from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from datetime import datetime, timedelta
from django.http import JsonResponse
from decimal import Decimal
from .models import Appointments
from .forms import BookingForm
from services.models import ServicesList

import stripe


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
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    service = get_object_or_404(ServicesList, pk=service_id)
    booking_form = BookingForm()

    deposit_price = service.price / 5 * 100

    stripe_total = round(deposit_price)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    template = 'appointments/add_appointment.html/'
    context = {
        'booking_form': booking_form,
        'service': service,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    if request.method == 'POST':
        booking_form = BookingForm(request.POST)

        if booking_form.is_valid():
            new_booking = booking_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            new_booking.stripe_pid = pid
            new_booking.service = service
            new_booking.deposit_cost = deposit_price

            selected_time = booking_form.cleaned_data['appointment_time']
            selected_date = booking_form.cleaned_data['appointment_date']

            is_duplicate = Appointments.objects.filter(
                appointment_date=selected_date,
                appointment_time=selected_time,
            ).exists()

            if is_duplicate:
                error_message = f"Booking failed. The slot on \
                {selected_date} at {selected_time} is already taken. \
                    Please select another."
                context.update({
                    'error': error_message,
                })
                return render(request, template, context)

            confirmation_message = (f"Booking successful! See you for \
                                    {service.name} at \
                                        {selected_time} on {selected_date}.")
            if request.user.is_authenticated:
                new_booking.user = request.user
            
            new_booking.save()

            new_booking_id = new_booking.booking_id

            return redirect('booking_confirmation', booking_id=new_booking_id)
        else:
            booking_form = BookingForm(initial={'service': service})

    return render(request, template, context)


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
