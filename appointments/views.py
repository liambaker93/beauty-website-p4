from django.shortcuts import render, redirect, get_object_or_404, reverse
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

    template = 'appointments/appointments.html'

    if user.is_authenticated:
        if user.is_staff:
            all_bookings = Appointments.objects.all().order_by(
        'appointment_date', 'appointment_time')
            context = {
                'bookings': all_bookings,
            }
        else:
            user_bookings = Appointments.objects.filter(user=user).order_by(
        'appointment_date', 'appointment_time')
            context = {
                'bookings': user_bookings,
            }
        return render(request, template, context)
    else:
        return render(request, template)


def fullCalendar(request):

    return render(request, 'appointments/calendar_detail.html')


def viewOrders(request):
    """
    Returns a list of the appointments currently being booked by the user
    """
    return render(request, 'appointments/user_order.html')


def addAppointment(request, service_id):
    """
    Adds a service to the user's order, then leads to payment.
    """
    service = get_object_or_404(ServicesList, pk=service_id)
    deposit_cost = service.price / 2
    stripe_cost = int(deposit_cost)

    booking_form = BookingForm()

    if request.method == 'POST':
        booking_form = BookingForm(request.POST)

        if booking_form.is_valid():
            new_booking = booking_form.save(commit=False)
            new_booking.service = service
            new_booking.deposit_cost = stripe_cost

            selected_time = booking_form.cleaned_data['appointment_time']
            selected_date = booking_form.cleaned_data['appointment_date']

            is_duplicate = Appointments.objects.filter(
                appointment_date=selected_date,
                appointment_time=selected_time,
            ).exists()

            if is_duplicate:
                error_message = (f"Booking failed. The slot on \
                                 {selected_date} at {selected_time} \
                                    is already taken. Please select another.")
                context = {
                    'booking_form': booking_form,
                    'service': service,
                    'error': error_message,
                    'service_id': service_id,
                }
                return render(request, 'appointments/add_appointment.html', context)
            
            if request.user.is_authenticated:
                new_booking.user = request.user

            new_booking.save()

            return redirect('checkout_page', booking_id=new_booking.booking_id)
        else:
            print("Form is NOT valid. Errors:", booking_form.errors)
            booking_form = BookingForm(initial={'service': service,
                                                'deposit_cost': stripe_cost})

    context = {
        'booking_form': booking_form,
        'service': service,
        'deposit_cost': stripe_cost,
        'service_id': service_id,
    }

    template = 'appointments/add_appointment.html'

    return render(request, template, context)


def create_payment_intent(request, booking_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    stripe.api_key = settings.STRIPE_SECRET_KEY
    appointment = get_object_or_404(Appointments, pk=booking_id)
    stripe_total = appointment.deposit_cost

    MINIMUM_AMOUNT = 50

    if stripe_total < MINIMUM_AMOUNT:
        messages.warning(request, f"Deposit is below \
                        Stripe minimum ({MINIMUM_AMOUNT / 100})\
                        Amount set to minimum for testing.")
        stripe_total = MINIMUM_AMOUNT
    try:
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency='gbp',
            metadata={'booking_id': booking_id}
        )
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'clientSecret': intent.client_secret})


def checkout_page(request, booking_id):
    
    appointment = get_object_or_404(Appointments, pk=booking_id)
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    context = {
        'stripe_public_key': stripe_public_key,
        'appointment': appointment,
        'booking_id': booking_id,
    }

    return render(request, 'appointments/checkout.html', context)


def booking_confirmation(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    payment_intent_id = request.GET.get('payment_intent')

    if not payment_intent_id:
        return render(request, 'appointments/appointments.html', {'message': 'Invalid payment confirmation link.'})
    
    try:
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)

        if intent.status == 'succeeded':
            print("Payment")
            booking_id = intent.metadata.get('booking_id')

            context = {
                'intent': intent,
                'booking_id': booking_id,
            }

            return render(request, 'appointments/booking_confirmed.html', context)
        
        elif intent.status in ['requires_payment_method', 'requires_confirmation', 'requires_action']:
            return redirect('checkout_page', booking_id=intent.metadata.get('booking_id'))
        else:
            return render(request, 'appointments/appointments.html', {'intent': intent})
    except stripe.error.StripeError as e:
        return render(request, 'appointments/appointments.html', {'message': f"Stripe Error: {e.user_message}"})


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


def edit_appointment(request, booking_id):
    """
    A view for allowing a user to edit a booking they've made
    """
    appointment = get_object_or_404(Appointments, pk=booking_id)

    if request.method == 'POST':
        booking_form = BookingForm(request.POST, instance=appointment)
        if booking_form.is_valid():
            booking_form.save()

            return redirect(reverse('appointments'))

        else:
            (request, "Failed to update Booking. \
                Please ensure the form is valid.")
    else:
        booking_form = BookingForm(instance=appointment)

    template = 'appointments/edit_appointment.html'
    context = {
        'booking_form': booking_form,
        'appointment': appointment,
    }

    return render(request, template, context)


def delete_appointment(request, booking_id):
    """
    Ability for users to delete appointments they've made
    """
    appointment = get_object_or_404(Appointments, pk=booking_id)

    if request.user != appointment.user:
        messages.error(request, "Sorry, you can only delete your own bookings!")
        return redirect(reverse('appointments'))
    else:
        appointment.delete()
        messages.success(request, 'Booking has been cancelled!')
        return redirect(reverse('appointments'))
