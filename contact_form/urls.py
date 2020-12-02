from django.urls import path, include
from . import views

app_name = 'contact_form'

urlpatterns = [
    path('contact', views.contact, name='contact'),
    #path('listings', views.listings_view(), name='listings'),
]