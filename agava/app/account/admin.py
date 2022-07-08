from django.contrib import admin
from .models import AccountModel, AccountProjectModel, AccountPermissionsModel,\
    AccountParameterModel, AccountModbusRegisterModel, AccountHistoryModel, AccountWidgetModel


admin.site.register(AccountHistoryModel)
admin.site.register(AccountModel)
admin.site.register(AccountProjectModel)
admin.site.register(AccountPermissionsModel)
admin.site.register(AccountParameterModel)
admin.site.register(AccountModbusRegisterModel)
admin.site.register(AccountWidgetModel)
