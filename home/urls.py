from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('outlook-calendar/init/', views.outlook_calendar_init, name='outlook_calendar_init'),
    path('callback/', views.outlook_calendar_callback, name='outlook_calendar_callback'),
    path('outlook-calendar/events/', views.list_events, name='list_events'),
]
