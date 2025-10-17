from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import datetime, timedelta
from django.http import JsonResponse
from .models import Appointments
from .forms import BookingForm
from services.models import ServicesList



# Create your views here.

def appointmentsPage(request):

    ## Random code string generated for booking id to feed into HTML template and JS function    

    return render(request, 'appointments/appointments.html')


def fullCalendar(request):

    return render(request, 'appointments/calendar_detail.html')


def viewOrders(request):
    """
    Returns a list of the appointments currently being booked by the user
    """
    return render(request, 'appointments/user_order.html')


def addAppointment(request, service_id):
    """
    Adds a service to the user's order
    """
    service = get_object_or_404(ServicesList, pk=service_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)

        if form.is_valid():
            new_booking = form.save(commit=False)
            new_booking.service = service
            selected_time = form.cleaned_data['appointment_time']
            selected_date = form.cleaned_data['appointment_date']

            is_duplicate = Appointments.objects.filter(
                appointment_date=selected_date,
                appointment_time=selected_time,
            ).exists()

            if is_duplicate:
                error_message = f"Booking failed. The slot on {selected_date} at \
                    {selected_time} is already taken. Please select another."

                context = {
                    'form': form,
                    'service': service,
                    'error': error_message,
                }
                return render(request, 'appointments/add_appointment.html', context)

            confirmation_message = (f"Booking successful! See you for \
                                    {service.name} at \
                                    {selected_time} on {selected_date}.")
            if request.user.is_authenticated:
                new_booking.user = request.user

            new_booking.save()

            new_booking_id = new_booking.booking_id

            context = {
                'message': confirmation_message,
                'booking_id': new_booking_id,
            }
            request.session['basket'] = str(new_booking_id)
            print(['basket'])
            return redirect('booking_confirmation', booking_id=new_booking_id)
    else:
        form = BookingForm(initial={'service': service})

    context = {
        'form': form,
        'service': service,
    }

    return render(request, 'appointments/add_appointment.html', context)


def bookingConfirmation(request, booking_id):
    """
    Handles displaying the booking confirmation page generated via the new uuid from bookings
    """
    booking = get_object_or_404(Appointments, booking_id=booking_id)

    context = {
        'booking': booking,
        'booking_id': booking_id,
    }

    template = 'appointments/booking_confirmed.html'

    return render(request, template, context)

def calendar_events(request):
    start_date_str = request.GET.get('start')
    end_date_str = request.GET.get('end')

    if not request.user.is_authenticated:
        return JsonResponse([], safe=False)
    
    user = request.user

    try:
        start_date = datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
        end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))
    except (ValueError, TypeError):
        return JsonResponse([], safe=False)
    
    bookings = Appointments.objects.filter(
        appointment_date__gte=start_date.date(),
        appointment_date__lt=end_date.date(),
        user=user,
    )

    events = []
    for booking in bookings:
        start_datetime = datetime.combine(booking.appointment_date, booking.appointment_time)

        end_datetime = start_datetime + timedelta(hours=1)

        events.append({
            'title': f"Booked: {booking.service.name}",
            'start': start_datetime.isoformat(),
            'end': end_datetime.isoformat(),
        })

    return JsonResponse(events, safe=False)
