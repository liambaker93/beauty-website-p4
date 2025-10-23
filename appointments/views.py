from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.views.decorators.http import require_POST
from datetime import datetime, timedelta
from django.http import JsonResponse
from decimal import Decimal
from .models import Appointments
from .forms import BookingForm
from services.models import ServicesList
import stripe
import json


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
    service = get_object_or_404(ServicesList, pk=service_id)
    deposit_price = service.price / 5

    if request.method == 'POST':
        booking_form = BookingForm(request.POST)

        if booking_form.is_valid():
            pass
    
    deposit_cost = round(deposit_price)

    booking_form = BookingForm(initial={
        'deposit_cost': deposit_cost,
        'service': service,
    })

    context = {
        'booking_form': booking_form,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'deposit_cost': deposit_cost,
        'service': service,
        'service_id': service.id,
    }

    return render(request, 'appointments/add_appointment.html', context)


@require_POST
def test_data_reception(request, service_id):
    service = get_object_or_404(ServicesList, pk=service_id)
    try:
        raw_body = request.body.decode()
        print("Raw Body Received:", raw_body)

        data = json.loads(request.body)
        print("Parsed Data:", data)

        form_data = data.get('form_data')
        print("'Form_data' content:", form_data)

        if form_data:
            return JsonResponse({'message': 'Data received OK', 'data': form_data})
        else:
            return JsonResponse({'error': "Key 'form_data' not found or empty."}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Parsing failed: {str(e)}'}, status=500)


@require_POST
def create_embedded_checkout(request, service_id):
    try:
        data = json.loads(request.body)
        form_data = data.get('form-data')
        print("Received form data:", form_data)

        service = get_object_or_404(ServicesList, pk=service_id)

        booking_form = BookingForm(form_data)

        if not booking_form.is_valid():
            print("Form Errors:", booking_form.errors)
            return JsonResponse({'errors': booking_form.errors}, status=400)

        new_booking = booking_form.save(commit=False)
        new_booking.service = service
        new_booking.deposit_cost = service.price / 5
        new_booking.payment_status = 'PENDING'

        if request.user.is_authenticated:
            new_booking.user = request.user

        new_booking.save()

        stripe_total = round(new_booking.deposit_cost * 100)

        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': settings.STRIPE_CURRENCY,
                    'product_data': {'name': service.name + ' Deposit'},
                    'unit_amount': stripe_total,
                },
                'quantity': 1,
            }],
            mode='payment',
            ui_mode='embedded',
            return_url=request.build_absolute_uri(
                f'/appointments/confirmation/{new_booking.id}/?session_id={{CHECKOUT_SESSION_ID}}'
            ),
            metadata={'booking_id': str(new_booking.id)},
        )

        new_booking.stripe_session_id = session.id
        new_booking.save()

        return JsonResponse({
            'clientSecret': session.client_secret,
            'sessionId': session.id,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)




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
