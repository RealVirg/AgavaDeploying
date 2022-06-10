from django.contrib import admin
from .models import AccountModel, AccountProjectModel, AccountPermissionsModel


admin.site.register(AccountModel)
admin.site.register(AccountProjectModel)
admin.site.register(AccountPermissionsModel)
