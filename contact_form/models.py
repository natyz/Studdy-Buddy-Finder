from django.db import models
from django import forms


class EmailMessage(models.Model):
    name = models.TextField(max_length=100)
    email = models.TextField(max_length=100)
    message = models.TextField(max_length=200)

    def __str__(self):
        return  self.name
