from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput
from django.forms import CheckboxInput
from django import forms
from django.core.exceptions import FieldDoesNotExist

from .models import Listing, Group


'''
/***************************************************************************************
*  REFERENCES
*  Title: Bootstrap Date/Time Picker Documentation
*  Author: Tempus Dominus
*  Date: 11/11/20
*  Code version: N/A
*  URL: https://getdatepicker.com/4/Options/
*  Software License: N/A
***************************************************************************************
*  Title: Django Widgets Documentation
*  Author: Django
*  Date: 11/01/20
*  Code version: 3.1
*  URL: https://docs.djangoproject.com/en/3.1/ref/forms/widgets/
*  Software License:  3-clause BSD license
***************************************************************************************/
'''


class NewListingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NewListingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        '''
        /***************************************************************************************
        Bootstrap Date/Time Picker Documentation
        ***************************************************************************************
        Django Widgets Documentation
        ***************************************************************************************/
        '''
        model = Listing
        fields = '__all__'
        widgets = {
            # 'section': SearchableSelect(model='listing.Listing', search_field='section', limit=10),
            'study_time': DateTimePickerInput(
                options={
                    # 'format': "dddd - MMMM D, YYYY - h:mm A",
                    'timeZone': '',
                    # 'inline': True,
                    'showClose': True,
                    'showClear': True,
                    'sideBySide': True,
                    'showTodayButton': True,
                    'allowInputToggle': True
                }),
            'comment': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Enter your listing\'s headline', 'autofocus': 'autofocus',}),
            'uid': forms.HiddenInput(),
            'zid': forms.HiddenInput(),
            'pub_date': forms.DateInput(format='%m/%d/%Y %I:%M'),
            'pub_date': forms.HiddenInput(),
            'member2': forms.HiddenInput(),
            'member3': forms.HiddenInput(),
            'member4': forms.HiddenInput(),
            'member5': forms.HiddenInput(),
            'hi': forms.Select(attrs={
                'class': 'form-control bootstrap-switch',
                'data-size': 'mini',
                'data-on-color': 'success',
                'data-on-text': 'Active',
                'data-off-color': 'danger',
                'data-off-text': 'Inactive',
                'name': 'is_active',
            })
        }
        required = (
            'course',
            'section',
            'comment',
            'study_time'
        )


class GroupJoinForm(forms.ModelForm):
    join_group = forms.BooleanField()
    widgets = {
        'join the group': CheckboxInput(attrs={'class': 'required checkbox form-control'}),
    }

    class Meta:
        model = Group
        fields = '__all__'

