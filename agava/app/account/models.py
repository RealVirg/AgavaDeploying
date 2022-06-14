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
    admin = models.BooleanField(default=True)
    device = models.BooleanField(default=True)
    tables = models.BooleanField(default=True)

    def __str__(self):
        return self.account.user.username


class AccountDevicesModel(models.Model):
    name_device = models.CharField(default='device', max_length=200)

    def __str__(self):
        return self.name_device


class AccountProjectModel(models.Model):
    users = models.ManyToManyField(AccountModel, related_name='accounts')
    name_project = models.CharField(max_length=200, default='Project', help_text="Project")
    projects = models.Manager()
    permissions = models.ManyToManyField(AccountPermissionsModel, related_name='perm')
    devices = models.ManyToManyField(AccountDevicesModel, related_name="devices")

    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'id': self.id})
