from django.contrib import admin
from django.db import models
from django import forms
from .models import *
from .forms import NewListingForm


class ListingAdmin(admin.ModelAdmin):
    form = NewListingForm


admin.site.register(Listing, ListingAdmin)

