from django.shortcuts import render
from .models import ServiceCategory, ServicesList

# Create your views here.


def services(request):
    """
    A list of the services offered.
    """
    services = ServicesList.objects.all()
    categories = ServiceCategory.objects.all()

    context = {
        'services': services,
        'categories': categories,
    }
    return render(request, 'services/services.html', context)
