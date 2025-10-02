from django.urls import path
from . import views

urlpatterns = [
    path('', views.services, name="services"),
    path('add/', views.addNewService, name="add_new_service"),
]
