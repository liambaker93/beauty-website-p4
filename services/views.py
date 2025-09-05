from django.shortcuts import render

# Create your views here.


def services(request):
    """
    A list of the services offered.
    """
    return render(request, 'services/services.html')
