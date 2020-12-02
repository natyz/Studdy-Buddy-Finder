from django.db import models
import datetime

from django.db.models import TextField
from django.utils import timezone
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Field


class Home(models.Model):
    name = models.TextField(max_length=20)
    home_text = models.TextField(max_length=2000)

    def __str__(self):
        return 'Comment {} by {}'.format(self.home_text, self.name)


class Login(models.Model):
    name: TextField = models.TextField(max_length=20)
    login_text = models.TextField(max_length=2000)

    def __str__(self):
        return 'Comment {} by {}'.format(self.login_text, self.name)


class Listings(models.Model):
    # name = models.TextField(max_length=20)
    # home_text = models.TextField(max_length=2000)
    major = models.TextField(max_length=20000)
