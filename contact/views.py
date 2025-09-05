from django.shortcuts import render

# Create your views here.

def contact(request):
    """
    Contact form for users to contact site owner with requests
    """
    return render(request, 'contact/contact.html')