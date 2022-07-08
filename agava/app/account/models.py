from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone


class AccountHistoryModel(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    action = models.CharField(default="nothing", max_length=1000)

    def __str__(self):
        tz = timezone.get_default_timezone()
        return '{} '.format(self.date.astimezone(tz).strftime('%H:%M %Y-%m-%d')) + str(self.action)


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
    history_project = models.ManyToManyField(AccountHistoryModel, related_name="history")

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


class AccountParameterValueModel(models.Model):
    value = models.CharField(null=True, max_length=200)


class AccountModbusRegisterModel(models.Model):
    number_device = models.CharField(null=True, max_length=200)
    number_function_read = models.CharField(null=True, max_length=200)
    address_read = models.CharField(null=True, max_length=200)
    number_function_write = models.CharField(null=True, max_length=200)
    address_write = models.CharField(null=True, max_length=200)


class AccountParameterModel(models.Model):
    name_parameter = models.CharField(default="parameter", max_length=200)
    type_parameter = models.CharField(default="type_parameter", max_length=200)
    value = models.ForeignKey(AccountParameterValueModel, on_delete=models.CASCADE, null=True)
    device = models.ForeignKey(AccountDevicesModel, on_delete=models.CASCADE, null=True)
    modbus_register = models.OneToOneField(AccountModbusRegisterModel, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name_parameter


class AccountDashboardModel(models.Model):
    name = models.CharField(default="dashboard", max_length=200)
    project = models.ForeignKey(AccountProjectModel, on_delete=models.CASCADE, null=True)

    def get_absolute_url(self):
        return reverse('dashboard', kwargs={'id': self.id})


class AccountWidgetModel(models.Model):
    name = models.CharField(default="", max_length=200)
    parameters = models.ManyToManyField(AccountParameterModel, on_delete=models.CASCADE, null=True)
    wdth = models.CharField(default="100", max_length=200)
    hght = models.CharField(default="100", max_length=200)
    type = models.CharField(default="last_value", max_length=200)
    dashboard = models.ForeignKey(AccountDashboardModel, on_delete=models.CASCADE, null=True)
