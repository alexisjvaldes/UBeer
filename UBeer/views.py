from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login as login_user
from django.contrib.auth.decorators import login_required


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
        # user = Users.objects.filter(username=username, password=password).first()
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login_user(request, user)
            if user.groups.filter(name='UBeer_riders').exists():
                return HttpResponseRedirect('/rider_home')
            if user.groups.filter(name='UBeer_Establishment').exists():
                return HttpResponseRedirect('/establishment_home')
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
        pass
        # data = request.POST
        # username = data.get('username', '')
        # password = data.get('password', '')

    return render(request, "signup.html", context)


@login_required(login_url='/login/')
def rider_home(request):
    context = {
        'data': {},
        'errors': [],
    }

    return render(request, "rider/rider_home.html", context)


@login_required(login_url='/login/')
def rider_home(request):
    context = {
        'data': {},
        'errors': [],
    }

    return render(request, "rider/rider_home.html", context)
