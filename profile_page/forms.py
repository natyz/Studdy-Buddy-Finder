from django import forms
from django.core.files.images import get_image_dimensions
from django.utils import timezone
import datetime
from django.db.models import Count, F, Value
from .models import UserProfile


class UserProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = UserProfile
        exclude = ("user", "url", 'relevant_class')
        widgets = {
            'bio': forms.Textarea(
                attrs={'id': 'bio', 'class': 'bio', 'placeholder': 'Tell us about yourself ...', 'autofocus': 'autofocus'}),
            'zoom_id': forms.Textarea(
                attrs={'id': 'zoomID', 'class': 'form-control', 'placeholder': '555-555-5555',}),
            'class_1': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'CS3240',}),
            'class_2': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'APMA3100',}),
            'class_3': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'STS4500',}),
            'class_4': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'CS2150',}),
            'class_5': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'ECE4120',}),
            'class_6': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'CS1234',}),
            'username': forms.HiddenInput(),
            'zid': forms.HiddenInput(),
        }

    def save(self, commit=True):
        profile = self.instance
        profile.nickname = self.cleaned_data['nickname']
        profile.major = self.cleaned_data['major']
        profile.nick = self.cleaned_data['nick']
        profile.year = self.cleaned_data['year']
        # profile.relevant_class = self.cleaned_data['relevant_class']
        profile.bio = self.cleaned_data['bio']
        profile.zoom_id = self.cleaned_data['zoom_id']

        profile.class_1 = self.cleaned_data['class_1']
        profile.class_2 = self.cleaned_data['class_2']
        profile.class_3 = self.cleaned_data['class_3']
        profile.class_4 = self.cleaned_data['class_4']
        profile.class_5 = self.cleaned_data['class_5']
        profile.class_6 = self.cleaned_data['class_6']
        profile.class_7 = self.cleaned_data['class_7']

        if self.cleaned_data['image']:
            profile.image = self.cleaned_data['image']

        if commit:
            profile.save()
        return profile


class UserZoomForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('zoom_id',)
        widgets = {
            'zoom_id': forms.Textarea(
                attrs={'id': 'zoomID', 'placeholder': '555-555-5555', 'autofocus': 'autofocus',})
        }

    def save(self, commit=True):
        profile = self.instance
        profile.zoom_id = self.cleaned_data['zoom_id']

        if commit:
            profile.save()
        return profile
