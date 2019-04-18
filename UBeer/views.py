from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login as login_user, logout
from UBeer.models import Trips, Establishments, Riders


def login(request):
    context = {
        'data': {},
        'errors': [],
    }

    Group .objects.get_or_create(name='rider')
    Group.objects.get_or_create(name='establishment')

    if request.method == 'POST':
        data = request.POST
        username = data.get('username', '')
        password = data.get('password', '')

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                request.session.set_expiry(86400)
                login_user(request, user)

                if user.groups.filter(name='rider').exists():
                    return HttpResponseRedirect('/riderHome')
                if user.groups.filter(name='establishment').exists():
                    return HttpResponseRedirect('/establishmentHome')
        else:
            context['errors'].append("The username or password is incorrect.")

    return render(request, "login.html", context)


def signup(request):
    context = {
        'data': {},
        'errors': [],
    }

    Group .objects.get_or_create(name='rider')
    Group.objects.get_or_create(name='establishment')

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
            group = Group.objects.get(name='rider')
            user.groups.add(group)
        else:
            group = Group.objects.get(name='establishment')
            user.groups.add(group)

        return HttpResponseRedirect('/login')

    return render(request, "signup.html", context)


def rider_home(request):
    context = {
        'data': {},
        'errors': [],
        'establishments': [
            {'name': 'smoking dog pub', 'id': 'a', 'img': 'https://media-cdn.tripadvisor.com/media/photo-s/02/28/1e/1c/outside-bar.jpg', 'info': 'Cheap and great', 'rating': 8,
             'rideTime': 5, 'minTab': 15},
            {'name': 'bar italia', 'id': 'c', 'img': 'https://coolyourjetsiv.files.wordpress.com/2011/11/bar-italia-outside.jpg', 'info': 'Italian bar', 'rating': 11,
             'rideTime': 12, 'minTab': 30},
            {'name': 'the pumphouse', 'id': 'd', 'img': 'https://www.rumshopryan.com/wp-content/uploads/2011/02/Pumphouse-outside-night.jpg', 'info': 'Rustic bar and grille', 'rating': 2,
             'rideTime': 3.5, 'minTab': 10},
            {'name': 'manzoni', 'id': 'b', 'img': 'https://media-cdn.tripadvisor.com/media/photo-s/06/b3/b1/15/outside-view.jpg', 'info': 'Manzoni', 'rating': 4.5,
             'rideTime': 9, 'minTab': 20},
        ],
    }

    user = request.user

    if not user.is_authenticated:
        return HttpResponseRedirect('/login')
    elif user.groups.filter(name='establishment').exists():
        return HttpResponseRedirect('/establishmentHome')

    return render(request, "rider/rider_home.html", context)


def checkout(request):
    context = {
        'data': {},
        'errors': [],
    }

    # establishments = Establishments.objects.all()
    # context['establishments'] = establishments

    user = request.user

    if not user.is_authenticated:
        return HttpResponseRedirect('/login')

    return render(request, "rider/checkout.html", context)


def confirm(request):
    context = {
        'data': {},
        'errors': [],
    }

    user = request.user

    if not user.is_authenticated:
        return HttpResponseRedirect('/login')

    return render(request, "rider/confirm.html", context)


def establishment_home(request):
    user = request.user

    if not user.is_authenticated:
        return HttpResponseRedirect('/login')
    elif user.groups.filter(name='rider').exists():
        return HttpResponseRedirect('/riderHome')

    trips = Trips.objects.filter(establishment__user=user)

    return render(request, "establishment/establishment_home.html", {'trips': trips})


def logout_view(request):
    logout(request)

    return HttpResponseRedirect('/login')
