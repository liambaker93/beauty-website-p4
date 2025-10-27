from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import ServiceCategory, ServicesList
from appointments.models import Appointments
from .forms import ServiceForm, ServiceCategoryForm

# Create your views here.


def services(request):
    """
    A list of the services offered.
    Includes sorting and search queries
    """
    services = ServicesList.objects.all()
    categories = None

    query = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                services = services.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            services = services.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            services = services.filter(category__name__in=categories)
            categories = ServiceCategory.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error
                (request, "You didn't enter any search criteria!")
                return redirect(reverse('services'))
            queries = Q(name__icontains=query) | Q(
                description__icontains=query)
            services = services.filter(queries)

    current_sort = f"{sort}_{direction}"

    context = {
        'services': services,
        'search_term': query,
        'current_categories': categories,
        'current_sort': current_sort

    }
    return render(request, 'services/services.html', context)


def addNewService(request):
    """
    Ability for admin user to add a new service to the site from
    within the webpage
    instead of via the admin page.
    """
    # add blank space validation
    if not request.user.is_staff:
        messages.error(request, "Sorry, only the store owner can do that!")
        return redirect(reverse('services'))

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully added service!")
            return redirect(reverse('services'))
        else:
            messages.error
            (request, "Adding service failed. "
                "Please ensure the form is valid.")
    else:
        form = ServiceForm()

    template = 'services/add_service.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


def editService(request, service_id):
    """
    Ability for the admin user to edit services on the website
    """
    if not request.user.is_staff:
        messages.error(request, "Sorry, only the store owner can do that!")
        return redirect(reverse('services'))
    service = get_object_or_404(ServicesList, pk=service_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid:
            form.save()
            messages.success(request, "Successfully updated service!")
            return redirect(reverse('services'))
        else:
            messages.error
            (request, f"Failed to update service. \
                Please ensure the form is valid.\
                    {form.errors}")
    else:
        form = ServiceForm(instance=service)
        messages.info(request, f"You are editing {service.name}")

    template = 'services/edit_service.html'
    context = {
        'form': form,
        'service': service,
    }

    return render(request, template, context)


def deleteService(request, service_id):
    """
    Ability for the admin user to edit services on the website
    """
    if not request.user.is_staff:
        messages.error(request, "Sorry, only the store owner can do that!")
        return redirect(reverse('services'))
    service = get_object_or_404(ServicesList, pk=service_id)

    if Appointments.objects.filter(service=service).exists():
        messages.warning(request, f"Sorry, {service.name} \
                         has bookings attached. Please cancel \
                         those before deleting the service.")
        return redirect(reverse('services'))
    else:
        service.delete()
        messages.success(request, f"Service: '{service.name}' has been deleted!")
        
        return redirect(reverse('services'))


def addNewCategory(request):
    """
    Ability for admin user to add a new category
    to the site from within the webpage
    instead of via the admin page
    """
    if not request.user.is_staff:
        messages.error(request, "Sorry, only the store owner can do that!")
        return redirect(reverse('services'))

    if request.method == 'POST':
        form = ServiceCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully added category!")
            return redirect(reverse('add_new_service'))
        else:
            messages.error
            (request, "Adding category failed. "
                "Please ensure the form is valid.")
    else:
        form = ServiceCategoryForm()

    template = 'services/add_category.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
