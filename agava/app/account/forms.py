from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django import forms
from .models import AccountProjectModel, AccountModel, AccountParameterModel, AccountDevicesModel, AccountDashboardModel
from django.shortcuts import get_object_or_404
import logging


class CreateProjectForm(forms.Form):
    name = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': "name project"}))


class EditAdminForm(forms.Form):
    def __init__(self, id, *args, **kwargs):
        super(EditAdminForm, self).__init__(*args, **kwargs)
        self.fields['perm_id'] = forms.ModelChoiceField(AccountProjectModel.projects.get(id=id).permissions.all(),
                                                        label='Для кого ')
    ch = (
        ('admin', "Администрирование"),
        ('del', "Удалить"),
        ('device', 'Устройства')
    )
    choice_actions = forms.ChoiceField(choices=ch, label="Изменить ")


class NewAdminUserForm(forms.Form):
    new_user = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя, которого нужно добавить'}))

    def clean_new_user(self):
        cd = self.cleaned_data
        if len(get_user_model().objects.filter(username=cd['new_user'])) == 0:
            raise forms.ValidationError('Wrong username!')
        return cd['new_user']


class CreateDeviceForm(forms.Form):
    name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': "Имя устройства"}))
    ch = (
        ('modbus-tcp', "modbus-tcp"),
        ('device-type-2', 'device-type-2')
    )
    type_device = forms.ChoiceField(choices=ch, label='Тип устройства ')


class AddRegisterModbusForm(forms.Form):
    number_device = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': "Номер устройства"}))
    number_function_read = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'placeholder': "Функция чтения"}))
    address_read = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'placeholder': "Адрес чтения"}))
    number_function_write = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'placeholder': "Функция записи"}))
    address_write = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'placeholder': "Адрес записи"}))


class AddParameterForm(forms.Form):
    name_parameter = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': "Имя параметра"}))
    type_parameter = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': "Тип параметра"}))


class DelParameterForm(forms.Form):
    def __init__(self, id, *args, **kwargs):
        super(DelParameterForm, self).__init__(*args, **kwargs)
        self.fields['parameter'] = forms.ModelChoiceField(AccountParameterModel.objects.filter(
            device=get_object_or_404(AccountDevicesModel, id=id)), label='Параметр для удаления')


class CreateDashboardForm(forms.Form):
    name_dashboard = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': "Название Dashboard"}))


class DeleteDashboardForm(forms.Form):
    def __init__(self, id, *args, **kwargs):
        super(DeleteDashboardForm, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.ModelChoiceField(
            AccountDashboardModel.objects.filter(project=get_object_or_404(AccountProjectModel, id=id)), label='')
