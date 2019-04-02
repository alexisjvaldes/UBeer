from django.shortcuts import render, HttpResponseRedirect
from UBeer.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate, login, logout
from django import *

def log(request):
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
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                request.session.set_expiry(86400)
                login(request, user)

                if user.groups.filter(name='UBeer_riders').exists():
                    return HttpResponseRedirect('/riderHome')
                if user.groups.filter(name='UBeer_Establishment').exists():
                    return HttpResponseRedirect('/establishmentHome')
        else:
            context['errors'].append("The username or password is incorrect.")
        # If a user exists and is valid, we redirect them to the appropriate page based on
        # their role (rider or establishment).  Otherwise, add an error to the page.
        # if user and user.is_valid(username, password):
    return render(request, "login.html", context)


def signup(request):
    context = {
        'data': {},
        'errors': [],
    }
    if request.method == 'POST':
        data = request.POST
        username = data.get('username', '')
        firstName = data.get('firstName', '')
        lastName = data.get('lastName', '')
        password = data.get('password', '')
        email = data.get('email', '')
        userGroup = data.get('group', '')
        user = User.objects.create_user(username, email, password)
        user.last_name = lastName
        user.first_name = firstName
        user.email = email
        user.save()
        if userGroup == '1':
            group = Group.objects.get(name='UBeer_riders')
            group.user_set.add(user)
        else:
            group = Group.objects.get(name='UBeer_Establishment')
            group.user_set.add(user)
        return HttpResponseRedirect('/login')
    return render(request, "signup.html", context)
def riderHome(request):
    context = {
        'data': {},
        'errors': [],
    }
    user = request.user
    if not user.is_authenticated:
        return HttpResponseRedirect('/login')
    if user.groups.filter(name='UBeer_Establishment').exists():
        return HttpResponseRedirect('/establishmentHome')

    return render(request, "rider/rider_home.html", context)

def establishmentHome(request):
    context = {
        'data': {},
        'errors': [],
    }
    user = request.user
    if not user.is_authenticated:
        return HttpResponseRedirect('/login')
    if user.groups.filter(name='UBeer_riders').exists():
        return HttpResponseRedirect('/riderHome')
    return render(request, "establishment/establishment_home.html", context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')