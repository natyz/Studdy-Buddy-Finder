from django import forms
from django.contrib.auth.decorators import login_required
from django.core.files.images import get_image_dimensions
from django.urls import reverse
from regex import regex
from .models import UserProfile
import json
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserProfileForm, UserZoomForm
from django.views import generic
from django.contrib.auth import get_user_model
from django.shortcuts import render
import re

'''
/***************************************************************************************
*  REFERENCES

*  Title: Django_Blog
*  Author: Corey Schafer
*  Date: 10/26/2020
*  Code version: part 8
*  URL: https://github.com/CoreyMSchafer/code_snippets/tree/master/Django_Blog
*  Software License: N/A

*  Title: How to redirect to a different view after processing a form getting noReverseMatch error
*  Author: Brandon (guy from stackoverflow)
*  Date: 10/27/20
*  Code version: N/A
*  URL: https://stackoverflow.com/questions/8421919/how-to-redirect-to-a-different-view-after-processing-a-form-getting-noreversemat
*  Software License: N/A
***************************************************************************************/
'''

class ProfileView(generic.DetailView):
    model = get_user_model()
    slug_field = "username"
    template_name = 'profile/profile.html'
    fields = '__all__'

    def get_object(self, queryset=None):
        user = super(ProfileView, self).get_object(queryset)
        UserProfile.objects.get_or_create(user=user)
        return user


class UserProfileEdit(generic.UpdateView):
    model = UserProfile
    template_name = 'profile/edit.html'
    form_class = UserProfileForm

    def get_object(self, queryset=None):
        return


class UserProfileZoomEdit(generic.UpdateView):
    model = UserProfile
    template_name = 'profile/zoom.html'
    form_class = UserZoomForm

    def get_object(self, queryset=None):
        return


# https://project-1-08.herokuapp.com/complete/google-oauth2/

'''
/***************************************************************************************
Django_Blog by Corey Schafer
***************************************************************************************/
'''


@login_required
def edit_profile(request):
    # print('am i actually getting here?')  # yes as of now
    pro = request.user.userprofile
    if request.method == 'POST':
        form = UserProfileForm(request.POST or None, request.FILES or None, instance=pro,
                               initial={'nickname': request.user.userprofile.nickname,
                                        'year': request.user.userprofile.year,
                                        'bio': request.user.userprofile.bio,
                                        'major': request.user.userprofile.major,
                                        'zoom_id': request.user.userprofile.zoom_id,
                                        'class_1': request.user.userprofile.class_1,
                                        'class_2': request.user.userprofile.class_2,
                                        'class_3': request.user.userprofile.class_3,
                                        'class_4': request.user.userprofile.class_4,
                                        'class_5': request.user.userprofile.class_5,
                                        'class_6': request.user.userprofile.class_6,
                                        'class_7': request.user.userprofile.class_7})
        if form.is_valid():
            try:
                m = form.cleaned_data['major']
                y = form.cleaned_data['year']
                # rc = form.cleaned_data['relevant_class']
                b = form.cleaned_data['bio']
                i = form.cleaned_data['image']
                u = form.cleaned_data['username']
                n = form.cleaned_data['nickname']
                z = form.cleaned_data['zoom_id']
                c1 = form.cleaned_data['class_1']
                c2 = form.cleaned_data['class_2']
                c3 = form.cleaned_data['class_3']
                c4 = form.cleaned_data['class_4']
                c5 = form.cleaned_data['class_5']
                c6 = form.cleaned_data['class_6']
                c7 = form.cleaned_data['class_7']
                if n and len(n) > 0:
                    pro.nickname = n
                else:
                    pro.nickname = request.user.userprofile.nickname
                if m and len(m) > 0:
                    pro.major = m
                else:
                    pro.major = request.user.userprofile.major
                if y and len(y) > 0:
                    pro.year = y
                else:
                    pro.year = request.user.userprofile.year
                # if rc and len(rc) > 0:
                #     pro.relevant_class = rc
                if b and len(b) > 0:
                    pro.bio = b
                else:
                    pro.bio = request.user.userprofile.bio
                if i:
                    pro.image = i
                if z:
                    z = re.sub(r'-', '', z)
                    if z and (len(z) == 10 or len(z) == 11) and regex.match(r'([0-9]+)?', z):
                        pro.zoom_id = z
                        print('\n\npro.zoomID: ', pro.zoom_id, '\n\n')
                        pro.username = request.user.username

                else:
                    pro.zoom_id = request.user.userprofile.zoom_id
                    pro.username = request.user.username

                if c1 and len(c1) > 0 and regex.match(r'((\s+)?[A-z]{2,4}(\s+)?\d{4}(\s+)?)', c1):
                    pro.class_1 = c1
                else:
                    pro.class_1 = request.user.userprofile.class_1
                if c2 and len(c2) > 0 and regex.match(r'((\s+)?[A-z]{2,4}(\s+)?\d{4}(\s+)?)', c2):
                    pro.class_2 = c2
                else:
                    pro.class_2 = request.user.userprofile.class_2
                if c3 and len(c3) > 0 and regex.match(r'((\s+)?[A-z]{2,4}(\s+)?\d{4}(\s+)?)', c3):
                    pro.class_3 = c3
                else:
                    pro.class_3 = request.user.userprofile.class_3
                if c4 and len(c4) > 0 and regex.match(r'((\s+)?[A-z]{2,4}(\s+)?\d{4}(\s+)?)', c4):
                    pro.class_4 = c4
                else:
                    pro.class_4 = request.user.userprofile.class_4
                if c5 and len(c5) > 0 and regex.match(r'((\s+)?[A-z]{2,4}(\s+)?\d{4}(\s+)?)', c5):
                    pro.class_5 = c5
                else:
                    pro.class_5 = request.user.userprofile.class_5
                if c6 and len(c6) > 0 and regex.match(r'((\s+)?[A-z]{2,4}(\s+)?\d{4}(\s+)?)', c6):
                    pro.class_6 = c6
                else:
                    pro.class_6 = request.user.userprofile.class_6
                if c7 and len(c7) > 0 and regex.match(r'((\s+)?[A-z]{2,4}(\s+)?\d{4}(\s+)?)', c7):
                    pro.class_7 = c7
                else:
                    pro.class_7 = request.user.userprofile.class_7

                pro.username = request.user.username

            except (KeyError, UserProfile.DoesNotExist):
                print('no doeeeeeee')
                return render(request, 'profile/edit.html', {
                    'profile': pro,
                    'error_message': "You didn't select a choice.",
                })
            pro.save()
    # print('but what about here', pro.nick)  # not here yet

    '''
    /***************************************************************************************
    Using HttpResponseRedirect by Brandon
    ***************************************************************************************/
    '''

    return HttpResponseRedirect(reverse('home:profile', kwargs={
        'slug': request.user}))  # render(request, 'profile/profile.html', {'object.userprofile': pro})  )


@login_required
def edit_zoom_profile(request):
    # print('am i actually getting here?')  # yes as of now
    pro = request.user.userprofile
    if request.method == 'POST':
        form = UserZoomForm(request.POST or None, request.FILES or None, instance=pro)
        if form.is_valid():
            try:
                z = form.cleaned_data['zoom_id']
                if z:
                    z = re.sub(r'-', '', z)
                    if z and (len(z) == 10 or len(z) == 11) and regex.match(r'([0-9]+)?', z):
                        pro.zoom_id = z
                        pro.username = request.user.username
                else:
                    pro.zoom_id = request.user.userprofile.zoom_id
            except (KeyError, UserProfile.DoesNotExist):
                print('no doeeeeeee')
                return render(request, 'profile/edit.html', {
                    'profile': pro,
                    'error_message': "Please enter a valid ZoomID.",
                })
            pro.save()
            print('\n\npro.zoomID: ', pro.zoom_id, '\n\n')
            print('\n\npro.username: ', pro.username, '\n\n')
    return HttpResponseRedirect(reverse('listing:create'))  # render(request, 'profile/profile.html', {'object.userprofile': pro})  )
