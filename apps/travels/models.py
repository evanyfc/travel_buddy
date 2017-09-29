# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ..login_and_reg.models import User
from django.db import models
from datetime import datetime

# Create your models here.
class TravelManager(models.Manager):
    def create_travel(self, form_data, user_id):
        errors = []
        if len(form_data['destination']) < 1:
            errors.append("You did not enter a destination")
        if len(form_data['description']) < 1:
            errors.append("Please enter a description")
        if len(form_data['start_date']) > 0 or len(form_data['end_date']) > 0:
            start_date = datetime.strptime(form_data['start_date'], "%Y-%m-%d")
            end_date = datetime.strptime(form_data['end_date'], "%Y-%m-%d")
            if datetime.today() >= start_date:
                errors.append("Start date must be in the future")
            if start_date > end_date:
                errors.append("Trip cannot end before it starts!")

        if errors:
            return (False, errors)

        user = User.objects.get(id=user_id)
        travel = Travel.objects.create(destination = form_data['destination'], description = form_data['description'], user = user, start_date = start_date, end_date = end_date)
        travel.participants.add(user)
        return (True, travel)

    def join_trip(self, trip_id, user_id):
        user = User.objects.get(id=user_id)
        trip = Travel.objects.get(id=trip_id)
        trip.participants.add(user)
        return True


class Travel(models.Model):
    destination = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(User, related_name="trip_creator")
    participants=models.ManyToManyField(User, related_name="trip_participants")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = TravelManager()
