from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django import forms
from .models import AccountProjectModel, AccountModel
import logging


class CreateProjectForm(forms.Form):
    name = forms.CharField()


class EditAdminForm(forms.Form):
    def __init__(self, id, *args, **kwargs):
        super(EditAdminForm, self).__init__(*args, **kwargs)
        self.fields['perm_id'] = forms.ModelChoiceField(AccountProjectModel.projects.get(id=id).permissions.all())
    ch = (
        ('admin', "admin"),
        ('del', "del"),
        ('device', 'device')
    )
    choice_actions = forms.ChoiceField(choices=ch)


class NewAdminUserForm(forms.Form):
    new_user = forms.CharField()

    def clean_new_user(self):
        cd = self.cleaned_data
        if len(get_user_model().objects.filter(username=cd['new_user'])) == 0:
            raise forms.ValidationError('Wrong username!')
        return cd['new_user']


class CreateDeviceForm(forms.Form):
    name = forms.CharField()
    ch = (
        ('modbus', "modbus"),
        ('OPC', "OPC"),
        ('OPD', 'OPD')
    )
    type_device = forms.ChoiceField(choices=ch)

