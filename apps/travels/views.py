# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.urls import reverse
from models import Travel
from ..login_and_reg.views import print_errors
from ..login_and_reg.models import User

# Create your views here.
def check_session(request):
    return 'user' in request.session

def index(request):
    if not check_session(request):
        return redirect(reverse('users:index'))
    id = request.session['user']['id']
    context = {
        'travels': Travel.objects.filter(participants=id),
        'other_travels': Travel.objects.exclude(participants=id)
    }
    return render(request, 'travel/index.html', context)

def add(request):
    if not check_session(request):
        return redirect(reverse('users:index'))

    return render(request, 'travel/new.html')

def create(request):
    if not check_session(request):
        return redirect(reverse('users:index'))

    result = Travel.objects.create_travel(request.POST, request.session['user']['id'])

    if result[0] == True:
        return redirect(reverse('travels:show', kwargs={'id': result[1].id}))
    else:
        print_errors(request, result[1])
        return redirect(reverse('travels:add'))

def show(request, id):
    if not check_session(request):
        return redirect(reverse('users:index'))

    context = {
        'travel': Travel.objects.get(id=id),
    }
    return render(request, 'travel/destination.html', context)

def jointrip(request, id):
    if not check_session(request):
        return redirect(reverse('users:index'))

    Travel.objects.join_trip(id, request.session['user']['id'])
    return redirect(reverse('travels:show', kwargs={'id': id}))
