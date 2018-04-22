import json
import platform

import psutil
from braces.views import OrderableListMixin
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Count
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, ListView

from cmdb.forms.UserForm import UserProfileForm

@login_required
def index(request):
    return HttpResponseRedirect("/mainform/")


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            try:
                auth.login(request, user)
                return HttpResponseRedirect(
                    request.GET.get('next') if request.GET.get('next') else "/mainform/")
            except ObjectDoesNotExist:
                return render(request, 'common/login.html',
                              {'login_err': u'账户还未设定,请先登录后台管理界面创建账户!'})
        else:
            return render(request, 'common/login.html',
                          {'login_err': 'Wrong username or password!'})
    else:
        return render(request, 'common/login.html')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


@login_required
def mainform(request):
    """
    系统主窗体
    :param request:
    :return:
    """
    return render(request, 'common/mainform.html', {})


@login_required
def personal(request):
    if request.method == 'POST':
        msg = {}
        old_passwd = request.POST.get('old_passwd')

        new_password = request.POST.get('new_passwd')
        user = auth.authenticate(username=request.user.username,password=old_passwd)
        if user is not None:
            request.user.set_password(new_password)
            request.user.save()
            msg['msg'] = 'Password has been changed!'
            msg['res'] = 'success'
        else:
            msg['msg'] = 'Old password is incorrect!'
            msg['res'] = 'failed'

        return HttpResponse(json.dumps(msg))
    else:
        return render(request,'common/personal.html',{'info_form':UserProfileForm()})



@login_required
def dashboard(request):
    module = {}
    return render(request, 'common/dashboard.html', {
        'module': module
    })



class BugListView(LoginRequiredMixin, OrderableListMixin, ListView):
    pass