# -*- coding: utf-8 -*-
# @Time    : 2018/5/8 17:16
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : DomainRecordsForm.py
# @Software: PyCharm

from django import forms

from cmdb.models.Domain import Domain_Records


class DomainRecordsForm(forms.ModelForm):
    class Meta:
        model = Domain_Records
        fields = '__all__'


class DomainRecordsListFilterForm(forms.Form):
    name = forms.CharField(required=False, label='关键字')