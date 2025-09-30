from django.shortcuts import render


# Create your views here.

def appointmentsPage(request):

    return render(request, 'appointments/appointments.html')


def fullCalendar(request):

    return render(request, 'appointments/calendar_detail.html')
