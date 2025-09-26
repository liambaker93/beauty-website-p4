from django.contrib import admin
from .models import ServiceCategory, ServicesList

# Register your models here.


class ServiceListAdmin(admin.ModelAdmin):
    services_display = (
        'name',
        'category',
        'timeframe',
        'price',
        'description'
    )

    ordering = ('name',)


class ServiceCategoryAdmin(admin.ModelAdmin):
    category_display = (
        'name',
    )


admin.site.register(ServicesList, ServiceListAdmin)
admin.site.register(ServiceCategory, ServiceCategoryAdmin)