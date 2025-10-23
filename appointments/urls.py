from django.urls import path
from . import views

urlpatterns = [
    path('', views.appointmentsPage, name="appointments"),
    path('calendar_detail/', views.fullCalendar, name="calendar_detail"),
    path('view_orders/', views.viewOrders, name="view_orders"),
    path('add_appointment/<int:service_id>/', views.addAppointment,
         name="add_appointment"),
    path('booking_confirmed/<uuid:booking_id>', views.bookingConfirmation,
         name="booking_confirmation"),
    path('api/calendar/events', views.calendar_events, name="calendar_events"),
    path('checkout/create/<int:service_id>/', views.create_embedded_checkout, name="checkout"),
]
