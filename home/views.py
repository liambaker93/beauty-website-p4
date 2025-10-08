from django.shortcuts import render
from django.conf import settings
import random, requests
from services.models import ServicesList

# Create your views here.


def index(request):
    """
    A view of random services to highlight
    on the homepage
    """
    items = list(ServicesList.objects.all())

    print(f"Total items queried: {len(items)}")

    sample_size = min(len(items), 2)

    if sample_size > 0:
        random_items = random.sample(items, sample_size)
    else:
        random_items = []

    print(f"Final random items count: {len(random_items)}")
    for item in random_items:
        print(f"Item title: {item.name}")

    context = {
        'random_services': random_items
    }

    return render(request, 'home/index.html', context)
