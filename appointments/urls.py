from django.urls import path
from . import views
from .webhooks import webhook_view

urlpatterns = [
    path('', views.appointmentsPage, name="appointments"),
    path('calendar_detail/', views.fullCalendar, name="calendar_detail"),
    path('view_orders/', views.viewOrders, name="view_orders"),
    path('add_appointment/<int:service_id>/', views.addAppointment,
         name="add_appointment"),
    path('edit_appointment/<uuid:booking_id>/', views.edit_appointment, name="edit_appointment"),
    path('api/calendar/events', views.calendar_events, name="calendar_events"),
    path('checkout/<uuid:booking_id>/', views.checkout_page, name="checkout_page"),
    path('checkout_intent/<uuid:booking_id>/', views.create_payment_intent, name="create_payment_intent"),
    path('booking_confirmed/', views.booking_confirmation, name="booking_confirmed"),
    path('webhook', webhook_view, name="webhook"),
]
