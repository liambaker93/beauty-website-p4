from django.contrib import admin
from .models import InformationRequest

# Register your models here.


@admin.register(InformationRequest)
class InformationRequestAdmin(admin.ModelAdmin):
    list_display = ('message',)
