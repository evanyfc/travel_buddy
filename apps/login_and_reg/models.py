# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import datetime
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def validateLogin(self, form_data):
        errors = []
        try:
            user = User.objects.get(username=form_data['username'])
            password = form_data['password'].encode()
            if bcrypt.hashpw(password, user.pw_hash.encode()) == user.pw_hash.encode():
                return (True, user)
            else:
                errors.append("Incorrect password!")
                return (False, errors)
        except ObjectDoesNotExist:
            errors.append("Username does not exist")
            return (False, errors)

    def register(self, form_data):
        errors = []
        name = form_data['name'].title()
        username = form_data['username']
        if not name or name.isspace():
            errors.append("Please enter a name")
        elif len(name) < 3:
            errors.append("Your name must be at least three characters")
        if not username or username.isspace():
            errors.append("Please enter a username")
        elif len(username) < 3:
            errors.append("Your username must be at least three characters")
        elif self.filter(username=username).exists():
            errors.append(("Username already exists!"))
        if len(form_data['password']) < 8:
            errors.append("Password must be at least 8 characters")
        elif not form_data['password'] == form_data['confirm_password']:
            errors.append("Passwords do not match")

        if errors:
            return (False, errors)

        pw_hash = bcrypt.hashpw(form_data['password'].encode(), bcrypt.gensalt())
        user = self.create(name = name, username = username, pw_hash = pw_hash)
        return (True, user)

class User(models.Model):
    name = models.CharField(max_length=45)
    username = models.CharField(max_length=45)
    pw_hash = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
