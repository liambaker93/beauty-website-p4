from django.urls import path
from . import views

urlpatterns = [
    path('', views.services, name="services"),
    path('add_service/', views.addNewService, name="add_new_service"),
    path('add_category/', views.addNewCategory, name="add_new_category"),
    path('edit_service/<int:service_id>/', views.editService, name="edit_service"),
    path('delete_service/<int:service_id>', views.deleteService, name="delete_service"),
]
