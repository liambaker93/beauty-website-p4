from django.shortcuts import render
from django.contrib import messages
from .forms import ContactForm
from .models import InformationRequest

# Create your views here.


def contact(request):
    """
    Contact form for users to contact site owner with requests
    """
    template = 'contact/contact.html'

    if request.method == 'POST':
        information_form = ContactForm(data=request.POST)
        if information_form.is_valid():
            information_form.save()
            messages.success(request, "Thanks for getting in contact! \
                             I'll get back in touch as soon as I can.")
# This if statement adds the total submissions into the context
# to then be used by the HTML templating to display them to
# staff users.
    if request.user.is_staff:
        submissions = InformationRequest.objects.all()

        information_form = ContactForm()
        context = {
            'information_form': information_form,
            'submissions': submissions
        }

        return render(request, template, context)

    information_form = ContactForm()

    context = {
        'information_form': information_form
    }

    return render(request, template, context)
