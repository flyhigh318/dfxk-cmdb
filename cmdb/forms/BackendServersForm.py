# -*- coding: utf-8 -*-
# @Time    : 2018/5/4 11:36
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : BackendServersForm.py
# @Software: PyCharm

from django import forms

from cmdb.models.Slb import Backend_Server


class BackendServersForm(forms.ModelForm):
    class Meta:
        model = Backend_Server
        fields = '__all__'


class BackendServersListFilterForm(forms.Form):
    name = forms.CharField(required=False, label='关键字')