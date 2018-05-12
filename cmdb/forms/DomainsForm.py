# -*- coding: utf-8 -*-
# @Time    : 2018/5/8 13:56
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : DomainForm.py
# @Software: PyCharm

from django import forms

from cmdb.models.Domain import Domain


class DomainForm(forms.ModelForm):
    class Meta:
        model = Domain
        fields = '__all__'


class DomainListFilterForm(forms.Form):
    name = forms.CharField(required=False, label='关键字')