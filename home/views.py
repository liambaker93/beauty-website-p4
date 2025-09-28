from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from msal import ConfidentialClientApplication
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

    print(f"Final tandom items count: {len(random_items)}")
    for item in random_items:
        print(f"Item title: {item.name}")

    context = {
        'random_services': random_items
    }

    return render(request, 'home/index.html', context)

def outlook_calendar_init(request):
    client_app = ConfidentialClientApplication(
        client_id=settings.MS_CLIENT_ID,
        client_credential=settings.MS_CLIENT_SECRET,
        authority=f'https://login.microsoftonline.com/{settings.MS_TENANT_ID}'
    )

    authorization_url = client_app.get_authorization_request_url(
        scopes=settings.MS_SCOPES,
        redirect_uri=settings.MS_REDIRECT_URI
    )

    return redirect(authorization_url)

def outlook_calendar_callback(request):
    code = request.GET.get('code')

    if not code:
        return HttpResponse('Authorization code not found in callback.', status=400)

    client_app = ConfidentialClientApplication(
        client_id=settings.MS_CLIENT_ID,
        client_credential=settings.MS_CLIENT_SECRET,
        authority=f'https://login.microsoftonline.com/{settings.MS_TENANT_ID}'
    )

    try:
        token_response = client_app.acquire_token_by_authorization_code(
            code=code,
            scopes=settings.MS_SCOPES,
            redirect_uri=settings.MS_REDIRECT_URI
        )

        if 'access_token' in token_response:
            request.session['ms_access_token'] = token_response['access_token']
            return HttpResponse('Outlook Calendar integration complete. You can now use Outlook Calendar with your Django app.')
        else:
            error_msg = token_response.get('error_description', 'Failed to authenticate.')
            return HttpResponse(f'Authentication failed: {error_msg}', status=400)
    except Exception as e:
        return HttpResponse(f'An error occured: {str(e)}', status=500)
    

def list_events(request):
    access_token = request.session.get('ms_access_token')

    if not access_token:
        return HttpResponse('User not authenticated.', status=401)

    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    events_url = 'https://graph.microsoft.com/v1.0/me/events'
    response = requests.get(events_url, headers=headers)

    if response.status_code == 200:
        events = response.json().get('value', [])
        return JsonResponse(events, safe=False)
    else:
        return HttpResponse('Failed to fetch events.', status=response.status_code)
