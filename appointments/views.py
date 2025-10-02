from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Appointments


# Create your views here.

def appointmentsPage(request):

    return render(request, 'appointments/appointments.html')


def fullCalendar(request):

    return render(request, 'appointments/calendar_detail.html')


def viewOrders(request):
    """
    Returns a list of the appointments currently being booked by the user
    """
    return render(request, 'appointments/user_order.html')


def addService(request, service_id):
    """
    Adds a service to the user's order
    """
    service = get_object_or_404(Appointments, pk=service_id)
    redirect_url = request.POST.get('redirect_url')
    orders = request.session.get('orders', {})

    if service_id not in list(orders.keys()):
        orders[service_id] = {
            'service': service.name,
            'price': service.deposit_cost,
            'date': service.appointment_date,
            'time': service.appointment_time,
        }
        messages.success(request, f"Added {service.name}")
    else:
        messages.info(request, f"{service.name} is already in your order.")

    request.session['orders'] = orders
    request.session.modified = True

    return redirect(redirect_url)
