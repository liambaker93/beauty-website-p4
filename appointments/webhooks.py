import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Appointments
import stripe

stripe.api_key = settings.STRIPE_PUBLIC_KEY

@csrf_exempt
def webhook_view(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        return HttpResponse(status=400)

    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object
        booking_id = payment_intent.metadata.get('booking_id')
        print("PaymentIntent was successful!")
        try:
            appointment = Appointments.objects.get(pk=booking_id)

            appointment.payment_status = Appointments.DEPOSIT

            amount_paid_pounds = payment_intent.amount / 100

            appointment.final_cost -= amount_paid_pounds

            if appointment.final_cost < 0:
                appointment.final_cost = 0
            
            appointment.save()
        except Appointments.DoesNotExist:
            print(f"Error: Booking ID {booking_id} not found.")
            return HttpResponse(status=200)
    elif event.type == 'payment_method.attached':
        payment_method = event.data.object
        print("PaymentMethod was attached to a customer!")
    else:
        print("Unhandled event type {}".format(event.type))

    return HttpResponse(status=200)
