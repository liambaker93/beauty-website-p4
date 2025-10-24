from django.urls import path
from . import views
from .webhooks import webhook_view

urlpatterns = [
    path('', views.appointmentsPage, name="appointments"),
    path('calendar_detail/', views.fullCalendar, name="calendar_detail"),
    path('view_orders/', views.viewOrders, name="view_orders"),
    path('add_appointment/<int:service_id>/', views.addAppointment,
         name="add_appointment"),
    path('api/calendar/events', views.calendar_events, name="calendar_events"),
    path('checkout/<uuid:booking_id>/', views.create_payment, name="checkout"),
    path('webhook', webhook_view, name="webhook"),
]
