from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
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
            selected_service = form.cleaned_data['service']

            confirmation_message = (f"Booking successful! See you for \
                                    {selected_service} at \
                                    {selected_time} on {selected_date}.")
            
            new_booking.save()

            new_booking_id = new_booking.booking_id
            
            template = 'appointments/booking_confirmed.html'

            context = {
                'message': confirmation_message,
                'booking_id': new_booking_id,
            }

            return redirect('booking_confirmation', booking_uuid=new_booking_id)
    else:
        form = BookingForm(initial={'service': service})
    
    context = {
        'form': form,
        'service': service,
    }
    
    return render(request, 'appointments/add_appointment.html', context)
