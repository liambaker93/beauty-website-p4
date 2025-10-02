from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib import messages
from .models import ServiceCategory, ServicesList
from .forms import ServiceForm, ServiceCategoryForm

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


def addNewService(request):
    """
    Ability for admin user to add a new service to the site from within the webpage
    instead of via the admin page.
    """
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only the store owner can do that!")
        return redirect(reverse('services'))
    
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully added service!")
            return redirect(reverse('home'))
        else:
            messages.error(request, "Adding service failed. Please ensure the form is valid.")
    else:
        form = ServiceForm()
    
    template = 'services/add_service.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


def addNewCategory(request):
    """
    Ability for admin user to add a new category to the site from within the webpage
    instead of via the admin page
    """
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only the store owner can do that!")
        return redirect(reverse('home'))
    
    if request.method == 'POST':
        form = ServiceCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully added category!")
            return redirect(reverse('services'))
        else:
            messages.error(request, "Adding category failed. Please ensure the form is valid.")
    else:
        form = ServiceCategoryForm()
    
    template = 'services/add_category.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
