from django.shortcuts import render
from django.views import generic
from .models import MainPageDocumentationModel
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.forms import formset_factory
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect
from account.models import AccountModel
from django.contrib.auth import get_user_model


def mainpage(request):
    return render(request,
                  'mainpage/mainpage.html',
                  context={})


def doc(request):
    docum = MainPageDocumentationModel.objects.all()
    return render(request,
                  'mainpage/doc.html',
                  context={'docum': docum})


def doc_detail(request, id):
    doc_id = get_object_or_404(MainPageDocumentationModel, id=id)
    docum = MainPageDocumentationModel.objects.all()
    return render(request,
                  'mainpage/doc_detail.html',
                  context={'doc_id': doc_id,
                           'docum': docum})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(mainpage)
                else:
                    return HttpResponse('Disabled account')
            else:
                return redirect(user_login)
    else:
        form = LoginForm()
    return render(request, 'mainpage/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect(mainpage)


def reg(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            new_account = AccountModel(user=get_object_or_404(get_user_model(), id=new_user.id))
            new_account.save()
            return render(request, 'mainpage/reg_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'mainpage/reg.html', {'user_form': user_form})
