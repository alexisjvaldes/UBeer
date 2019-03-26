from django.shortcuts import render, HttpResponseRedirect
from UBeer.models import *
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login

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
        # user = Users.objects.filter(username=username, password=password).first()
        user = authenticate(request, username=username, password=password)
        if user is not None:
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
        passwordConf = data.get('confirmPassword', '')
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
    return render(request, "riderHome.html", context)