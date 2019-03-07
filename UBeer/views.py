from django.shortcuts import render, HttpResponseRedirect
from UBeer.models import *


def login(request):
    context = {
        'data': {},
        'errors': [],
    }

    if request.method == 'POST':
        # Get data coming down from the login form.
        data = request.POST
        username = data.get('username', '')
        password = data.get('password', '')

        # Query the database for users with the provided username / password.
        # filter returns a list of all matching users, first gets the first one from the list.
        # If no user exists, user will contain 'None'.
        user = Users.objects.filter(username=username, password=password).first()

        # If a user exists and is valid, we redirect them to the appropriate page based on
        # their role (rider or establishment).  Otherwise, add an error to the page.
        if user and user.is_valid(username, password):
            if user.is_rider():
                HttpResponseRedirect('/rider_home.html')
            else:
                HttpResponseRedirect('/establishment_home.html')
        else:
            context['errors'].append("The username or password is incorrect.")

    return render(request, "login.html", context)


def sign_up(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get('username', '')
        password = data.get('password', '')
