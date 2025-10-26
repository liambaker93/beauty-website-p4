from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('/api/bookings/', views.calendar_feed, name="calendar_feed"),
]
