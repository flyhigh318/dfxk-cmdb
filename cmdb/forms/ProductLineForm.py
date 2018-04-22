# -*- coding: utf-8 -*-
# @Time    : 2018/3/28 15:50
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : __init__.py
# @Software: PyCharm


from django import forms

from cmdb.models.ProductLine import Product_line
from common.constants import FORM_WIDGET_BASE_STYLE


class ProductLineForm(forms.ModelForm):
    class Meta:
        model = Product_line
        # widgets = {
        #     'rental_date': forms.DateInput(attrs={'class':'datepicker'}),
        # }
        fields = '__all__'


class ProductLineListFilterForm(forms.Form):
    name = forms.CharField(required=False, label='关键字')