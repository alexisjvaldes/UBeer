from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login as login_user, logout
from UBeer.models import Trips


def login(request):
    context = {
        'data': {},
        'errors': [],
    }

    if request.method == 'POST':
        data = request.POST
        username = data.get('username', '')
        password = data.get('password', '')

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                request.session.set_expiry(86400)
                login_user(request, user)

                if user.groups.filter(name='UBeer_riders').exists():
                    return HttpResponseRedirect('/riderHome')
                if user.groups.filter(name='UBeer_establishments').exists():
                    return HttpResponseRedirect('/establishmentHome')
        else:
            context['errors'].append("The username or password is incorrect.")

    return render(request, "login.html", context)


def signup(request):
    context = {
        'data': {},
        'errors': [],
    }

    if request.method == 'POST':
        data = request.POST
        username = data.get('username', '')
        first_name = data.get('firstName', '')
        last_name = data.get('lastName', '')
        password = data.get('password', '')
        password_conf = data.get('confirmPassword', '')
        email = data.get('email', '')
        user_group = data.get('group', '')

        if password != password_conf:
            context['errors'].append("Passwords do not match. Please try again.")
            return render(request, "signup.html", context)

        if User.objects.filter(username=username).exists():
            context['errors'].append("Username is already taken.")
            return render(request, "signup.html", context)

        user = User.objects.create_user(username, email, password)
        user.last_name = last_name
        user.first_name = first_name
        user.email = email
        user.save()

        if user_group == '1':
            group, created = Group.objects.get_or_create(name='UBeer_riders')
            user.groups.add(group)
        else:
            group, created = Group.objects.get_or_create(name='UBeer_establishments')
            user.groups.add(group)

        return HttpResponseRedirect('/login')

    return render(request, "signup.html", context)


def rider_home(request):
    user = request.user

    if not user.is_authenticated:
        return HttpResponseRedirect('/login')
    elif user.groups.filter(name='UBeer_Establishment').exists():
        return HttpResponseRedirect('/establishmentHome')

    return render(request, "rider/rider_home.html", {})


def establishment_home(request):
    user = request.user

    if not user.is_authenticated:
        return HttpResponseRedirect('/login')
    elif user.groups.filter(name='UBeer_riders').exists():
        return HttpResponseRedirect('/riderHome')

    trips = Trips.objects.filter(establishment__user=user)

    return render(request, "establishment/establishment_home.html", {'trips': trips})


def logout_view(request):
    logout(request)

    return HttpResponseRedirect('/login')
