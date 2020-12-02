from django.contrib import messages

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ContactForm
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from django.views.generic import TemplateView

'''
/***************************************************************************************
*  REFERENCES
*  Title: Django Email/Contact Form Tutorial
*  Author: Will Vincnet
*  Date: 11/10/20
*  Code version: N/A
*  URL: https://learndjango.com/tutorials/django-email-contact-form
*  Software License: N/A
***************************************************************************************/
'''

def contact(request):
    '''
    /***************************************************************************************
    Django Email/Contact Form Tutorial by Will Vincent
    ***************************************************************************************/
    '''
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            sender_name = form.cleaned_data['name']
            sender_email = 'nyz7tc@virginia.edu'
            # form.cleaned_data['message']
            subject = f'Thank you contacting us! This is what you sent to us'
            message = form.cleaned_data['message']
            recipient = [form.cleaned_data['email']]
            try:
                send_mail(subject, message, sender_email, recipient,
                          fail_silently=False)
                self_subject = f'New feedback'
                self_recipient = ['studybuddyservices132@gmail.com']
                message = "Name: " + sender_name + "\n\n" + "From: " + recipient[0] + "\n\n" + message
                send_mail(self_subject, message, sender_email, self_recipient,
                          fail_silently=False)
            except BadHeaderError:
                return HttpResponse("Invalid Header")
            messages.success(request, 'Thank you for reaching out!', extra_tags='submit')
            return HttpResponseRedirect(request.path_info)
    else:
        form = ContactForm()
    return render(request, 'home/contact.html', {'form': form})


