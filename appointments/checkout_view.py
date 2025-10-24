from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.conf import settings
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Appointments
from .forms import BookingForm
from services.models import ServicesList
import stripe
import json

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout_view(request, service_id):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    service = get_object_or_404(ServicesList, pk=service_id)
    deposit = service.price / 2
    deposit_cost = round(deposit)


    template = 'appointments/checkout.html'

    context = {
        'service': service,
        'stripe_public_key': stripe_public_key,
        'deposit_cost': deposit_cost,
    }

    return render(request, template, context)

def calculate_order_amount(service_id)
    service = get_object_or_404(ServicesList, pk=service_id)

    deposit_cost = service.price / 2
    stripe_total = round(deposit_cost)


def create_payment(request, service_id):
    service = get_object_or_404(ServicesList, pk=service_id)

    if request.method == 'POST':
        try:
            data = json.loads(request.data)
            intent = stripe.PaymentIntent.create(
                amount=calculate_order_amount(data[service_id]),
                currency='gbp',
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse(error=str(e)), 403