from django.shortcuts import render

# Create your views here.

def account(request):
    """
    Show account info if logged in
    """
    return render(request, 'account/account.html')