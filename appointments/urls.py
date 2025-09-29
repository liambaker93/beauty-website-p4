from django.urls import path
from . import views

urlpatterns = [
    path('', views.appointmentsPage, name="appointments"),
]