import logging

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import (AccountProjectModel, AccountModel, AccountPermissionsModel, AccountDevicesModel,
                     AccountParameterModel, AccountTagOPCModel, AccountModbusRegisterModel, AccountParameterOPDModel)
from .forms import (CreateProjectForm, EditAdminForm, NewAdminUserForm, CreateDeviceForm, AddRegisterModbusForm,
                    AddParameterOPDForm, AddTagOPCForm, AddParameterForm, DelParameterForm)
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404


def check_own_project(request, project_id):
    user = request.user
    current_account = AccountModel.users.get(user=user)
    prj_id = get_object_or_404(AccountProjectModel, id=project_id)
    if len(prj_id.permissions.filter(account=current_account)) == 0:
        return False
    return True


@login_required
def account(request):
    user = request.user
    account = AccountModel.users.get(user=user)
    list_projects = AccountProjectModel.projects.filter(users=account)
    if request.method == 'POST':
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            account_permissions = AccountPermissionsModel(account=account, admin="Чтение и запись",
                                                          device="Чтение и запись")
            account_permissions.save()
            pr = AccountProjectModel(name_project=cd['name'])
            pr.save()
            pr.permissions.add(account_permissions)
            pr.users.add(account)
            pr.save()
    else:
        form = CreateProjectForm()
    return render(request,
                  'account/account.html',
                  {'account': account,
                   'form': form,
                   'list_projects': list_projects
                   })


@login_required
def project(request, id):
    if not check_own_project(request, id):
        return redirect(account)
    prj_id = get_object_or_404(AccountProjectModel, id=id)
    return render(request,
                  'account/project.html',
                  {'prj_id': prj_id})


@login_required
def admin(request, id):
    if not check_own_project(request, id):
        return redirect(account)
    prj_id = get_object_or_404(AccountProjectModel, id=id)
    perm = prj_id.permissions.all()
    if request.method == 'POST':
        if "use" in request.POST:
            admin_form = EditAdminForm(id, request.POST)
            if admin_form.is_valid():
                cd = admin_form.cleaned_data
                choice_actions = cd['choice_actions']
                user = request.user
                current_account = AccountModel.users.get(user=user)
                if not prj_id.permissions.get(account=current_account) == cd['perm_id'].id:
                    if choice_actions == "admin":
                        permm = AccountPermissionsModel.objects.get(id=cd['perm_id'].id)
                        if permm.admin == "Чтение и запись":
                            permm.admin = "Чтение"
                        elif permm.admin == "Чтение":
                            permm.admin = "Нет прав"
                        else:
                            permm.admin = "Чтение и запись"
                        permm.save()
                    if choice_actions == "device":
                        permm = AccountPermissionsModel.objects.get(id=cd['perm_id'].id)
                        if permm.device == "Чтение и запись":
                            permm.device = "Чтение"
                        elif permm.device == "Чтение":
                            permm.device = "Нет прав"
                        else:
                            permm.device = "Чтение и запись"
                        permm.save()
                    if choice_actions == "del":
                        permm = AccountProjectModel.projects.get(id=id).permissions.get(id=cd['perm_id'].id)
                        AccountProjectModel.projects.get(id=id).permissions.remove(permm)
                        acc = AccountProjectModel.projects.get(id=id).users.get(id=cd['perm_id'].account.id)
                        AccountProjectModel.projects.get(id=id).users.remove(acc)
        else:
            admin_form = EditAdminForm(id)
        if "new" in request.POST:
            new_user = NewAdminUserForm(request.POST)
            if new_user.is_valid():
                cd = new_user.cleaned_data
                acc = AccountModel.users.get(user=get_user_model().objects.get(username=cd['new_user']))
                item = AccountProjectModel.projects.get(id=id)
                if len(item.users.filter(id=acc.id)) == 0:
                    item.users.add(acc)
                    p = AccountPermissionsModel(account=acc)
                    p.save()
                    item.permissions.add(p)
                    item.save()
        else:
            new_user = NewAdminUserForm()
    else:
        new_user = NewAdminUserForm()
        admin_form = EditAdminForm(id)
    return render(request,
                  'account/admin.html',
                  {'prj_id': prj_id, 'admin_form': admin_form, 'perm': perm, 'new_user': new_user})


@login_required
def devices(request, id):
    if not check_own_project(request, id):
        return redirect(account)
    prj_id = get_object_or_404(AccountProjectModel, id=id)
    dvs = AccountDevicesModel.objects.filter(project=prj_id)
    if request.method == 'POST':
        create_form = CreateDeviceForm(request.POST)
        if create_form.is_valid():
            cd = create_form.cleaned_data
            device = AccountDevicesModel(name_device=cd['name'], type_device=cd['type_device'], project=prj_id)
            device.save()
    else:
        create_form = CreateDeviceForm()
    return render(request,
                  'account/devices.html',
                  {'prj_id': prj_id, 'create_form': create_form, "dvs": dvs})


@login_required
def device(request, id):
    device = get_object_or_404(AccountDevicesModel, id=id)
    prj = get_object_or_404(AccountProjectModel, id=device.project.id)
    params = AccountParameterModel.objects.filter(device=device)
    if request.method == 'POST':
        form = AddParameterForm()
        if "del" in request.POST:
            form_del = DelParameterForm(id, request.POST)
            if form_del.is_valid():
                cd = form_del.cleaned_data
                AccountParameterModel.objects.get(id=cd['parameter'].id).delete()
        else:
            form_del = DelParameterForm(id)
        if "modbus" in request.POST:
            form = AddParameterForm(request.POST)
            form_modbus = AddRegisterModbusForm(request.POST)
            if form.is_valid() and form_modbus.is_valid():
                cd = form.cleaned_data
                cd1 = form_modbus.cleaned_data
                param = AccountParameterModel(name_parameter=cd['name_parameter'],
                                              type_parameter=cd['type_parameter'],
                                              read_or_write=cd['read_or_write'],
                                              device=device)
                param.save()
                modbus_reg = AccountModbusRegisterModel(number_device=cd1['number_device'],
                                                        number_function_read=cd1['number_function_read'],
                                                        address_read=cd1['address_read'],
                                                        number_function_write=cd1['number_function_write'],
                                                        address_write=cd1["address_write"])
                modbus_reg.save()
                param.modbus_register = modbus_reg
                param.save()

        else:
            form_modbus = AddRegisterModbusForm()
    else:
        form_modbus = AddRegisterModbusForm()
        form = AddParameterForm()
        form_del = DelParameterForm(id)
    return render(
        request,
        'account/device.html',
        {
            'prj': prj,
            'device': device,
            "form_modbus": form_modbus,
            'form_del': form_del,
            'form': form,
            'params': params
        }
    )
