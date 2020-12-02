import datetime
from typing import Optional

from django.db import models
from profile_page.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import FieldDoesNotExist

from django.db.models import F, QuerySet
from django.utils import timezone
from datetime import date

from flask import Markup
from .CHOICES import *
from .uva import *

'''
/***************************************************************************************
*  REFERENCES
*  Title: Django Custom Manager Documentation
*  Author: Django
*  Date: 10/10/20
*  Code version: 3.1
*  URL: https://docs.djangoproject.com/en/3.1/topics/db/managers/
*  Software License:  3-clause BSD 
***************************************************************************************
*  Title: Flask Markup Documentation
*  Author: Flask
*  Date: 10/15/20
*  Code version: 1.1
*  URL: https://flask.palletsprojects.com/en/1.1.x/
*  Software License:  3-clause BSD 
***************************************************************************************/
'''


class CS3240Manager(models.Manager):
    '''
    /***************************************************************************************
    Django Custom Manager Documentation
    ***************************************************************************************/
    '''
    # def get_queryset(self):
    #     return super().get_queryset().filter(course='CS').filter(section=3240)

    def find(self, uid) -> Optional['Order']:
        queryset = self.get_queryset()
        try:
            instance = queryset.get(uid=uid)
        except ObjectDoesNotExist:
            instance = None
        finally:
            return instance

    def find_all_for(self, uid) -> QuerySet:
        queryset = self.get_queryset()
        return queryset.filter(uid=uid).order_by('-pub_date')


class ListingsManager(models.Manager):
    # def get_queryset(self):
    #     return super().get_queryset().filter(course='CS').filter(section=3240)

    def find(self, id) -> Optional['Order']:
        queryset = self.get_queryset()
        try:
            instance = queryset.get(id=id)
        except ObjectDoesNotExist:
            instance = None
        finally:
            return instance

    def find_all_for(self) -> QuerySet:
        queryset = self.get_queryset()
        return queryset.all().order_by('-pub_date')


class Listing(models.Model):
    uid = models.CharField(max_length=60, default="NoOne")
    zid = models.CharField(max_length=60, blank=True)
    course = models.CharField(max_length=60, choices=Course, blank=False, default="undefined")
    section = models.IntegerField(choices=sections, blank=False)
    lecture = models.CharField(max_length=60, choices=Lecture, default="WEB_BASED")
    timezone = models.CharField(max_length=60, choices=Timezone, default="EDT")
    language = models.CharField(max_length=100, choices=languages, default="English")
    professor = models.CharField(max_length=400, choices=professors, blank=True)
    major = models.CharField(max_length=60, choices=majors, blank=True)
    pub_date = models.DateTimeField('date published', auto_now_add=True, null=True)
    study_time = models.DateTimeField(blank=True)
    num_members = models.CharField(max_length=1, choices=group_members, default=3)
    member2 = models.CharField(max_length=60, default="vacant")
    member3 = models.CharField(max_length=60, default="vacant")
    member4 = models.CharField(max_length=60, default="vacant")
    member5 = models.CharField(max_length=60, default="vacant")
    comment = models.TextField(max_length=200, blank=False)
    listings = models.Manager()
    cs_3240_listings = CS3240Manager()
    get_all_listings = ListingsManager()

    def __str__(self):
        '''
        /***************************************************************************************
        Flask Markup Documentation
        ***************************************************************************************/
        '''
        pub_date = self.pub_date
        value = Markup('<strong>' + self.comment + '</strong><br>')
        profile = Markup("<sub> <a style='float:right' href=/users/" + self.uid + ">" + self.uid + '</a></sub>')
        br = Markup('<br/>')
        small = Markup('<small>')
        small_ = Markup('</small>')
        sub = Markup('<sub style="float:right">')
        sub_ = Markup('</sub> <hr/>')
        b = Markup('<b>')
        b_ = Markup('</b>')
        li = Markup('<li>')
        li_ = Markup('</li>')
        # ensp = Markup(' &ensp; &ensp;  &ensp; &ensp; &ensp; &ensp; &ensp; &ensp;  &ensp; &ensp; &ensp;  &ensp; &ensp;  &ensp; &ensp;  &ensp; &ensp;  &ensp; &ensp;  &ensp; &ensp;  &ensp; &ensp; ')
        # return f"User: f"{self.uid}"\nCourse: f"{self.course}"\nSection: f"{self.section}"\nLecture: f"{self.lecture}"\nTimeZone: f"{self.timezone}"\nLanguage: f"{self.language}"\nProfessor: f"{self.professor}"\nSelf: f"{self.major}"\nCreated: f"{self.pub_date}"\nComment: f"{self.comment}""
        return value + small + profile + br + sub + f"{pub_date.strftime('%b %d, %Y %I:%M:%S %p')}" + sub_ + small_ + \
               li + b + "Course: " + b_ + f"{self.course}" + li_ + li + b + "Section: " + b_ + f"{self.section}" + li_ + \
               li + b + "Lecture: " + b_ + f"{self.lecture}" + li_ + li + b + "Timezone: " + b_ + f"{self.timezone}" + li_ + \
               li + b + "Language: " + b_ + f"{self.language}" + li_ + li + b + "Professor: " + b_ + f"{self.professor}" + li_ + \
               li + b + "Major: " + b_ + f"{self.major}" + li_ + li + b + "Ideal Study Time: " + b_ + f"{self.study_time.strftime('%b. %d, %Y   -  %I:%M %p')}" + li_ + \
               li + b + "Ideal Group Size: " + b_ + f"{self.num_members}"

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    class Meta:
        indexes = [
            models.Index(fields=['uid', 'pub_date']),
            models.Index(fields=['uid'], name='uid_idx'),
        ]
        ordering = ['-pub_date', 'course', F('professor').asc(nulls_last=True), F('section').asc(nulls_last=True),
                    F('timezone').asc(nulls_last=True)]


class GroupMember(models.Model):
    zoom_id = UserProfile.zoom_id
    name = UserProfile.nickname

    def __str__(self):
        return self.name


class Group(models.Model):
    name = Listing.uid
    members = models.ManyToManyField(GroupMember, through='Membership')
    join_group = models.BooleanField()

    def __str__(self):
        return self.name


class Membership(models.Model):
    person = models.ForeignKey(GroupMember, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)