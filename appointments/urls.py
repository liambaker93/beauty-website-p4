from django.urls import path
from . import views

urlpatterns = [
    path('', views.appointmentsPage, name="appointments"),
    path('calendar_detail/', views.fullCalendar, name="calendar_detail"),
    path('view_orders/', views.viewOrders, name="view_orders"),
    path('add_appointment/<int:service_id>/', views.addAppointment, name="add_appointment"),
    path('booking_confirmed/<uuid:booking_id>', views.bookingConfirmation, name="booking_confirmation"),
]
