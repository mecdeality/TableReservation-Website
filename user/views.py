from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Request, AccountType
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


# Create your views here.
def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully.')
            return redirect('user-login')
    else:
        form = UserCreationForm()
    return render(request, 'user/registration.html', {'form': form})


@login_required
def request_send(request):
    acc = AccountType.objects.filter(user=request.user).first()

    if request.method == 'POST':
        req = Request(account=acc)
        if len(request.POST.get('message')):
            req.sendMsg = request.POST.get('message')
            messages.success(request, 'Your request has been successfully sent to the administrations!')
        req.save()
        return redirect('table-main')

    if Request.objects.filter(account=acc).exists():
        req = Request.objects.filter(account=acc).first()
        exist = True
    else:
        req = None
        exist = False

    context = {
        'exist': exist,
        'req': req
    }
    return render(request, 'user/send_request.html', context)


@login_required
def request_send_again(request):
    acc = AccountType.objects.filter(user=request.user).first()
    req = Request.objects.filter(account=acc).first()
    req.denied = False
    req.accepted = False
    req.delete()
    return redirect('request-send')


@login_required
def check_request(request):
    reqs = Request.objects.filter(accepted=False,denied=False)
    context = {
        'reqs': reqs
    }

    if request.method == 'POST':
        msg = request.POST.get('message')
        acc_id = request.POST.get('acc_id')
        acc = AccountType.objects.filter(id=acc_id).first()
        req = Request.objects.filter(account=acc).first()

    if 'accept' in request.POST:
        req.accepted = True
        req.responseMsg = msg
        acc.restaurantAccount = True
        acc.save()
        req.save()
        return redirect('check-request')

    elif 'reject' in request.POST:
        req.denied = True
        req.responseMsg = msg
        req.save()
        return redirect('check-request')

    return render(request, 'user/check_request.html', context)

