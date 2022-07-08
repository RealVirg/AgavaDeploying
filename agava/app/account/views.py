import logging

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import (AccountProjectModel, AccountModel, AccountPermissionsModel, AccountDevicesModel,
                     AccountParameterModel, AccountModbusRegisterModel,
                     AccountHistoryModel, AccountDashboardModel, AccountWidgetModel)
from .forms import (CreateProjectForm, EditAdminForm, NewAdminUserForm, CreateDeviceForm, AddRegisterModbusForm,
                    AddParameterForm, DelParameterForm, CreateDashboardForm, DeleteDashboardForm, CreateWidgetForm)
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
import random, math


def check_own_project(request, project_id):
    user = request.user
    current_account = AccountModel.users.get(user=user)
    prj_id = get_object_or_404(AccountProjectModel, id=project_id)
    if len(prj_id.permissions.filter(account=current_account)) == 0:
        return False
    return True


def write_history_str(pr, strin, acc):
    history_str = AccountHistoryModel(action=acc.user.username + ": " + strin)
    history_str.save()
    pr.history_project.add(history_str)
    pr.save()


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
            write_history_str(pr, "Создан проект " + cd['name'], account)
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
    history = prj_id.history_project.all()
    return render(request,
                  'account/project.html',
                  {'prj_id': prj_id,
                   'history': history})


@login_required
def admin(request, id):
    if not check_own_project(request, id):
        return redirect(account)
    prj_id = get_object_or_404(AccountProjectModel, id=id)
    perm = prj_id.permissions.all()
    user = request.user
    current_account = AccountModel.users.get(user=user)
    current_account_perm = prj_id.permissions.get(account=current_account)
    if current_account_perm.admin == "Нет прав":
        return redirect(project, id=prj_id.id)
    if request.method == 'POST':
        if "use" in request.POST:
            admin_form = EditAdminForm(id, request.POST)
            if admin_form.is_valid():
                cd = admin_form.cleaned_data
                choice_actions = cd['choice_actions']
                if not current_account_perm.id == cd['perm_id'].id and current_account_perm.admin == "Чтение и запись":
                    if choice_actions == "admin":
                        permm = AccountPermissionsModel.objects.get(id=cd['perm_id'].id)
                        if permm.admin == "Чтение и запись":
                            permm.admin = "Чтение"
                            write_history_str(prj_id, "Права администрации " + permm.account.user.username + " изменены на Чтение", current_account)
                        elif permm.admin == "Чтение":
                            permm.admin = "Нет прав"
                            write_history_str(prj_id, "Права администрации " + permm.account.user.username + " изменены на Нет прав",
                                              current_account)
                        else:
                            permm.admin = "Чтение и запись"
                            write_history_str(prj_id, "Права администрации " + permm.account.user.username + " изменены на Чтение и запись",
                                              current_account)
                        permm.save()
                    if choice_actions == "device":
                        permm = AccountPermissionsModel.objects.get(id=cd['perm_id'].id)
                        if permm.device == "Чтение и запись":
                            permm.device = "Чтение"
                            write_history_str(prj_id,
                                              "Права на управление устройствами " + permm.account.user.username + " изменены на Чтение",
                                              current_account)
                        elif permm.device == "Чтение":
                            permm.device = "Нет прав"
                            write_history_str(prj_id,
                                              "Права на управление устройствами " + permm.account.user.username + " изменены на Нет прав",
                                              current_account)
                        else:
                            permm.device = "Чтение и запись"
                            write_history_str(prj_id,
                                              "Права на управление устройствами " + permm.account.user.username + " изменены на Чтение и запись",
                                              current_account)
                        permm.save()
                    if choice_actions == "del":
                        permm = AccountProjectModel.projects.get(id=id).permissions.get(id=cd['perm_id'].id)
                        AccountProjectModel.projects.get(id=id).permissions.remove(permm)
                        acc = AccountProjectModel.projects.get(id=id).users.get(id=cd['perm_id'].account.id)
                        AccountProjectModel.projects.get(id=id).users.remove(acc)
                        write_history_str(prj_id, permm.account.user.username + " удален из проекта",
                                          current_account)
        else:
            admin_form = EditAdminForm(id)
        if "new" in request.POST:
            new_user = NewAdminUserForm(request.POST)
            if new_user.is_valid() and current_account_perm.admin == "Чтение и запись":
                cd = new_user.cleaned_data
                acc = AccountModel.users.get(user=get_user_model().objects.get(username=cd['new_user']))
                item = AccountProjectModel.projects.get(id=id)
                if len(item.users.filter(id=acc.id)) == 0:
                    item.users.add(acc)
                    write_history_str(prj_id,
                                      "Добавлен " + acc.user.username + " в проект.",
                                      current_account)
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
    user = request.user
    current_account = AccountModel.users.get(user=user)
    current_account_perm = prj_id.permissions.get(account=current_account)
    if current_account_perm.device == "Нет прав":
        return redirect(project, id=prj_id.id)
    dvs = AccountDevicesModel.objects.filter(project=prj_id)
    if request.method == 'POST':
        create_form = CreateDeviceForm(request.POST)
        if create_form.is_valid() and current_account_perm.device == "Чтение и запись":
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

    user = request.user
    current_account = AccountModel.users.get(user=user)
    current_account_perm = prj.permissions.get(account=current_account)

    if current_account_perm.device == "Нет прав":
        return redirect(project, id=prj.id)

    if request.method == 'POST':
        form = AddParameterForm()
        if "del" in request.POST:
            form_del = DelParameterForm(id, request.POST)
            if form_del.is_valid() and current_account_perm.device == "Чтение и запись":
                cd = form_del.cleaned_data
                AccountParameterModel.objects.get(id=cd['parameter'].id).delete()
        else:
            form_del = DelParameterForm(id)
        if "modbus" in request.POST:
            form = AddParameterForm(request.POST)
            form_modbus = AddRegisterModbusForm(request.POST)
            if form.is_valid() and form_modbus.is_valid() and current_account_perm.device == "Чтение и запись":
                cd = form.cleaned_data
                cd1 = form_modbus.cleaned_data
                param = AccountParameterModel(name_parameter=cd['name_parameter'],
                                              type_parameter=cd['type_parameter'],
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


@login_required
def dashboards(request, id):
    prj = get_object_or_404(AccountProjectModel, id=id)
    dboards = AccountDashboardModel.objects.filter(project=prj)
    if request.method == "POST":
        form = CreateDashboardForm()
        del_form = DeleteDashboardForm(prj.id)
        if "create" in request.POST:
            form = CreateDashboardForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                new_db = AccountDashboardModel(name=cd["name_dashboard"], project=prj)
                new_db.save()
        elif "del" in request.POST:
            del_form = DeleteDashboardForm(prj.id, request.POST)
            if del_form.is_valid():
                cd = del_form.cleaned_data
                AccountDashboardModel.objects.get(id=cd['name'].id).delete()
    else:
        form = CreateDashboardForm()
        del_form = DeleteDashboardForm(prj.id)

    return render(request,
                  'account/dashboards.html',
                  {"dboards": dboards,
                   "form": form,
                   "del_form": del_form,
                   "prj": prj
                   })


@login_required
def dashboard(request, id):
    current_dashboard = get_object_or_404(AccountDashboardModel, id=id)
    prj = current_dashboard.project
    widgets = AccountWidgetModel.objects.filter(dashboard=current_dashboard)
    for wg in widgets:
        if wg.type == "last_value":
            params = wg.parameters.all()
            wg.value = str([random.randint(1, 200) for i in range(len(params))])[1:-1]
        if wg.type == "line_chart":
            y = 2013

            result = "date,value\n"

            for i in range(10000):
                _y = math.floor(i / 365)
                _m = math.floor((i - (_y * 365)) / 30)
                _d = i - _y * 365 - _m * 30
                if len(str(_m)) == 1:
                    _m = "0" + str(_m)
                else:
                    _m = str(_m)
                if _d > 28:
                    continue
                if len(str(_d)) == 1:
                    _d = "0" + str(_d)
                else:
                    _d = str(_d)
                s = str(_y + y) + "-" + _m + "-" + _d + "," + str(random.randint(-2000, 2000)) + "\n"
                result += s
            with open("static/mainpage/csv/test.csv", "w") as f:
                f.write(result)
            wg.value = 'http://172.16.0.88:1337/static/mainpage/csv/test.csv'
    if request.method == "POST":
        form = CreateWidgetForm(prj.id, request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            widget = AccountWidgetModel(name=cd["name"], type=cd["type"],
                                        wdth=cd["wdth"], hght=cd["hght"], dashboard=current_dashboard)
            widget.save()
            for param in cd["parameters"]:
                widget.parameters.add(param)
            widget.save()
            return redirect(dashboard, id=id)
    else:
        form = CreateWidgetForm(prj.id)

    return render(request,
                  'account/dashboard.html',
                  {"current_dashboard": current_dashboard,
                   "prj": prj,
                   "form": form,
                   "widgets": widgets
                   })
