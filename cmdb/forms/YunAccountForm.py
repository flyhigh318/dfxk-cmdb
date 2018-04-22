# -*- coding: utf-8 -*-
# @Time    : 2018/4/3 16:35
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : YunAccountForm.py
# @Software: PyCharm

from django import forms

from cmdb.models import YunAccount
from common.constants import FORM_WIDGET_BASE_STYLE


class YunAccountForm(forms.ModelForm):
    class Meta:
        model = YunAccount.Yun_Account
        # widgets = {
        #     'rental_date': forms.DateInput(attrs={'class':'datepicker'}),
        # }
        fields = '__all__'


class YunAccountListFilterForm(forms.Form):
    name = forms.CharField(required=False, label='关键字')