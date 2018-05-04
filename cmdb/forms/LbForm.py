# -*- coding: utf-8 -*-
# @Time    : 2018/5/3 17:21
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : LbForm.py
# @Software: PyCharm

from django import forms

from cmdb.models.Slb import Lb


class LbForm(forms.ModelForm):
    class Meta:
        model = Lb
        fields = '__all__'


class LbListFilterForm(forms.Form):
    name = forms.CharField(required=False, label='关键字')