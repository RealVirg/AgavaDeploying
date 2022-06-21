from django.contrib import admin
from .models import AccountModel, AccountProjectModel, AccountPermissionsModel,\
    AccountParameterModel, AccountModbusRegisterModel, TestModel


admin.site.register(AccountModel)
admin.site.register(AccountProjectModel)
admin.site.register(AccountPermissionsModel)
admin.site.register(AccountParameterModel)
admin.site.register(AccountModbusRegisterModel)
admin.site.regisete(TestModel)
