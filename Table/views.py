import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from . import models
from user.models import AccountType
from django.db.models import Q
from django.http import HttpResponse


def main(request):
    if request.method == 'GET' and request.GET.get('search') is not None:
        query = request.GET.get('search')
        restaurants = models.Restaurant.objects.filter(Q(name__contains=query) | Q(cuisines__contains=query))
    else:
        restaurants = models.Restaurant.objects.all()
    if request.user.is_authenticated:
        restaurntAcc = AccountType.objects.filter(user=request.user).first().restaurantAccount
    else:
        restaurntAcc = False
    context = {
        'title': 'REST - easy way to find a restaurant',
        'restaurants': restaurants,
        'restaurantAcc': restaurntAcc
    }
    return render(request, 'table/main.html', context)


def restaurant(request, restaurant_id):
    rt = models.Restaurant.objects.filter(id=restaurant_id).first()  # restaurant
    pics = models.RestaurantPicture.objects.filter(restaurant=rt)
    context = {
        'title': rt.name,
        'restaurant': rt,
        'pics': pics[:5],
        'left': len(pics) - 5
    }
    return render(request, 'table/restaurant.html', context)


@login_required
def reserve(request, restaurant_id):
    rt = models.Restaurant.objects.filter(id=restaurant_id).first()  # restaurant
    date = datetime.datetime.strptime(request.GET.get('date'), "%m/%d/%Y").date()
    context = {
        'title': rt.name + ' | Reservation',
        'date': date,
        'time': request.GET.get('time'),
        'size': request.GET.get('size'),
        'restaurant': rt
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        rq = request.POST.get('rq')
        reservation = models.Reservation(date=date, time=request.GET.get('time'), reserver=request.user,
                                         reserverName=name + ' ' + surname, phone=phone, email=email, request=rq,
                                         restaurant=rt, size=request.GET.get('size'))
        reservation.save()
        messages.success(request, 'You have successfully reserved a table. Please be on time!')
        return redirect('table-main')
    return render(request, 'table/reserve.html', context)


@login_required
def reservations(request):
    context = {
        'title': 'My reservations',
        'reservations': models.Reservation.objects.filter(reserver=request.user),
        # 'today': datetime.date.today()
    }
    return render(request, 'table/reservations.html', context)


@login_required
def admin_restaurants(request):
    acc = AccountType.objects.filter(user=request.user).first()
    restaurants = {}
    rr = models.Restaurant.objects.filter(account=acc)
    for r in models.Restaurant.objects.filter(account=acc):
        restaurants[r] = models.Reservation.objects.filter(restaurant=r)

    context = {
        'restaurants': restaurants
    }
    return render(request, 'table/admin_restaurants.html', context)


@login_required
def admin_reservations(request, restaurant_id):
    restaurant = models.Restaurant.objects.filter(id=restaurant_id).first()
    reservations = models.Reservation.objects.filter(restaurant=restaurant)

    context = {
        'reservations': reservations
    }
    return render(request, 'table/admin_reservations.html', context)


@login_required
def restaurant_add(request):
    if request.method == 'POST':
        data = request.POST

        name = data['name']
        avg_check = data['avg_check']
        cuisines = data['cuisines']
        about = data['about']
        address = data['address']
        phone = data['phone']
        email = data['email']
        preview = request.FILES.get('preview')
        pictures = request.FILES.getlist('pictures')
        acc = AccountType.objects.filter(user=request.user).first()

        r = models.Restaurant.objects.create(
            name=name,
            avg_check=avg_check,
            cuisines=cuisines,
            about=about,
            address=address,
            phone=phone,
            email=email,
            preview_img=preview,
            account=acc
        )

        for pic in pictures:
            p = models.RestaurantPicture.objects.create(restaurant=r, img=pic)

        messages.success(request, 'A new restaurant added successfully!')
        return redirect('admin-restaurants')

    return render(request, 'table/restaurant_add.html')
