from django.db import models
from home.CHOICES import *
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django.core.validators import MinLengthValidator, MaxLengthValidator


'''
/***************************************************************************************
*  REFERENCES

*  Title: Django_Blog
*  Author: Corey Schafer
*  Date: 10/26/2020
*  Code version: part 8
*  URL: https://github.com/CoreyMSchafer/code_snippets/tree/master/Django_Blog
*  Software License: N/A

*  Title: How can I make a Django form field contain only alphanumeric characters
*  Author: Martijn Pieters
*  Date: 11/14/2020
*  Code version: N/A
*  URL: https://stackoverflow.com/questions/17165147/how-can-i-make-a-django-form-field-contain-only-alphanumeric-characters
*  Software License: N/A


***************************************************************************************/
'''
alphanumeric = RegexValidator(r'^[0-9a-zA-Z_ ]*$', 'Only alphanumeric characters, spaces, and underscores are allowed.')


# Create your models here.
class UserProfile(models.Model):
    '''
    /***************************************************************************************
    *  How can I make a Django form field contain only alphanumeric characters by Martijn Pieters
    ***************************************************************************************/
    '''
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE, null=True, blank=True)
    # slug = models.SlugField(unique=True)
    nickname = models.CharField(max_length=50, default='', blank=True, null=True, validators=[alphanumeric],
                                help_text='<br/>\t*Only alphanumeric characters, spaces, and underscores are allowed.*')
    image = models.ImageField(default='default.jpg')
    url = models.URLField("Website", blank=True)
    major = models.CharField(max_length=69, choices=majors,
                             blank=True)  # https://stackoverflow.com/questions/31130706/dropdown-in-django-model
    year = models.CharField(max_length=69, choices=years, blank=True)
    relevant_class = models.CharField(max_length=69, choices=uva_classes, blank=True)
    bio = models.TextField(max_length=250, default='', blank=True, )
    zoom_id = models.CharField(max_length=12, blank=False, default='',
                               validators=[RegexValidator(regex='^\d{3}-\d{3}-\d{4}$')])
    # zoom_id = models.CharField(max_length=10, blank=True, default='',
    #                            help_text='<br/>\t*Enter enter the zoom id (digits only; e.g. \'7193694208\')*')
    username = models.CharField(max_length=60, blank=True)

    class_1 = models.CharField(max_length=300, default='', blank=True, null=True,
                               help_text='<br/>\t*Enter the class identifier (e.g. CS3240)*')
    class_2 = models.CharField(max_length=300, default='', blank=True, null=True,
                               help_text='<br/>\t*Enter the class identifier (e.g. CS3240)*')
    class_3 = models.CharField(max_length=300, default='', blank=True, null=True,
                               help_text='<br/>\t*Enter the class identifier (e.g. CS3240)*')
    class_4 = models.CharField(max_length=300, default='', blank=True, null=True,
                               help_text='<br/>\t*Enter the class identifier (e.g. CS3240)*')
    class_5 = models.CharField(max_length=300, default='', blank=True, null=True,
                               help_text='<br/>\t*Enter the class identifier (e.g. CS3240)*')
    class_6 = models.CharField(max_length=300, default='', blank=True, null=True,
                               help_text='<br/>\t*Enter the class identifier (e.g. CS3240)*')
    class_7 = models.CharField(max_length=300, default='', blank=True, null=True,
                               help_text='<br/>\t*Enter the class identifier (e.g. CS3240)*')

    def __str__(self):
        return f'{self.user.username} Profile'

    def __str__(self):
        return f'{self.zoom_id}'


    '''
    /***************************************************************************************
    *  Django_Blog by Corey Schafer
    ***************************************************************************************/
    '''


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
