import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
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
        print("PaymentIntent was successful!")
    elif event.type == 'payment_method.attached':
        payment_method = event.data.object
        print("PaymentMethod was attached to a customer!")
    else:
        print("Unhandled event type {}".format(event.type))

    return HttpResponse(status=200)
