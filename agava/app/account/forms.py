from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django import forms
from .models import AccountProjectModel, AccountModel, AccountParameterModel, AccountDevicesModel
from django.shortcuts import get_object_or_404
import logging


class CreateProjectForm(forms.Form):
    name = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': "name project"}))


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
        ('modbus-tcp', "modbus-tcp"),
        ('device-type-2', 'device-type-2')
    )
    type_device = forms.ChoiceField(choices=ch)


class AddParameterOPDForm(forms.Form):
    number = forms.CharField()
    name = forms.CharField()


class AddRegisterModbusForm(forms.Form):
    number_device = forms.CharField()
    number_function_read = forms.CharField(label='')
    number_function_read.required = False
    address_read = forms.CharField(label='')
    address_read.required = False
    number_function_write = forms.CharField(label='')
    number_function_write.required = False
    address_write = forms.CharField(label='')
    address_write.required = False


class AddTagOPCForm(forms.Form):
    type_OPC = forms.CharField()
    address = forms.CharField()


class AddParameterForm(forms.Form):
    name_parameter = forms.CharField()
    type_parameter = forms.CharField()
    ch = (
        ('read', "read"),
        ('write', "write")
    )
    read_or_write = forms.ChoiceField(choices=ch)


class DelParameterForm(forms.Form):
    def __init__(self, id, *args, **kwargs):
        super(DelParameterForm, self).__init__(*args, **kwargs)
        self.fields['parameter'] = forms.ModelChoiceField(AccountParameterModel.objects.filter(
            device=get_object_or_404(AccountDevicesModel, id=id)))

