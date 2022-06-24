from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


class AccountModel(models.Model):
    User = get_user_model()
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    users = models.Manager()

    def __str__(self):
        return self.user.username


class AccountPermissionsModel(models.Model):
    account = models.ForeignKey(AccountModel, on_delete=models.CASCADE, null=True)
    admin = models.CharField(default='Нет прав', max_length=100)  # Чтение и запись, Чтение, Нет прав
    device = models.CharField(default='Нет прав', max_length=100)
    tables = models.CharField(default='Нет прав', max_length=100)

    def __str__(self):
        return self.account.user.username


class AccountProjectModel(models.Model):
    users = models.ManyToManyField(AccountModel, related_name='accounts')
    name_project = models.CharField(max_length=200, default='Project', help_text="Project")
    projects = models.Manager()
    permissions = models.ManyToManyField(AccountPermissionsModel, related_name='perm')

    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'id': self.id})


class AccountDevicesModel(models.Model):
    name_device = models.CharField(default='device', max_length=200)
    type_device = models.CharField(default='type', max_length=200)
    project = models.ForeignKey(AccountProjectModel, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name_device

    def get_absolute_url(self):
        return reverse('device', kwargs={"id": self.id})


class AccountModbusRegisterModel(models.Model):
    number_device = models.CharField(null=True, max_length=200)
    number_function_read = models.CharField(null=True, max_length=200)
    address_read = models.CharField(null=True, max_length=200)
    number_function_write = models.CharField(null=True, max_length=200)
    address_write = models.CharField(null=True, max_length=200)


class AccountTagOPCModel(models.Model):
    type_OPC = models.CharField(null=True, max_length=200)
    address = models.CharField(null=True, max_length=200)


class AccountParameterOPDModel(models.Model):
    number = models.CharField(null=True, max_length=200)
    name = models.CharField(null=True, max_length=200)


class AccountParameterModel(models.Model):
    name_parameter = models.CharField(default="parameter", max_length=200)
    type_parameter = models.CharField(default="type_parameter", max_length=200)
    device = models.ForeignKey(AccountDevicesModel, on_delete=models.CASCADE, null=True)
    modbus_register = models.OneToOneField(AccountModbusRegisterModel, on_delete=models.CASCADE, null=True)

