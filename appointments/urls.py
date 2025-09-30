from django.urls import path
from . import views

urlpatterns = [
    path('', views.appointmentsPage, name="appointments"),
    path('calendar_detail/', views.fullCalendar, name="calendar_detail"),
]