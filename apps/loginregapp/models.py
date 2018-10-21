# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
import re
import bcrypt
LETTER_REGEX = re.compile(r"^[a-zA-Z]+$")
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")

class UserManager(models.Manager):
    def regvalidator(self, postData):
        errors = {}

        if len(postData['first_name']) < 1:
            errors["first_name"] = "First name cannot be blank"
        elif len(postData['first_name']) < 2:
            errors["first_name"] = "First name must be greater than 2 characters"
        elif not LETTER_REGEX.match(postData["first_name"]):
            errors["first_name"] = "First name must be letters only!"
        if len(postData['last_name']) < 1:
            errors["last_name"] = "last name cannot be blank"
        elif len(postData['last_name']) < 2:
            errors["last_name"] = "last name must be greater than 2 characters"
        elif not LETTER_REGEX.match(postData["last_name"]):
            errors["last_name"] = "last name must be letters only!"

        if len(postData["email"]) < 1:
            errors["email"] = "Email must cannot be blank"
        elif not EMAIL_REGEX.match(postData["email"]):
            errors["email_valid"] = "Email address not valid"
        elif User.objects.filter(email=postData["email"]):
            errors["email_valid"] = "Email is already registered"

        if len(postData["password"]) < 8:
            errors["password"] = "Password must be at least 8 characters!"
        if postData["password"]!=postData["password_confirm"]:
            errors["password_confirm"] = "Password does not match confirmation"

    def pwvalidator(self, postData):
        errors = {}
        user = User.objects.filter(email=postData["email"])
        print user[0].password
        if not user:
            errors["login"] = "Email is not registered"
            return errors
        if not bcrypt.checkpw(postData["password"].encode(), user[0].password.encode()):
            errors["login"] = "Incorrect password"
            return errors
        else:
            return errors


# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()