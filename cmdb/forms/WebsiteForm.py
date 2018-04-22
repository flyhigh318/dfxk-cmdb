# -*- coding: utf-8 -*-
# @Time    : 2018/4/19 14:49
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : WebsiteForm.py
# @Software: PyCharm

from django import forms

from cmdb.models.Website import Website
from common.constants import FORM_WIDGET_BASE_STYLE


class WebsiteForm(forms.ModelForm):
    class Meta:
        model = Website
        # widgets = {
        #     'rental_date': forms.DateInput(attrs={'class':'datepicker'}),
        # }
        fields = '__all__'


class WebsiteListFilterForm(forms.Form):
    search = forms.CharField(required=False, label='关键字')