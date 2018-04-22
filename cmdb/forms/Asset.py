# -*- coding: utf-8 -*-
# @Time    : 18-4-6 下午8:01
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : Asset.py
# @Software: dfxk-cmdb


from django import forms
from cmdb.models.Asset import Assets


class AssetForm(forms.ModelForm):
    class Meta:
        model = Assets
        # widgets = {
        #     'rental_date': forms.DateInput(attrs={'class':'datepicker'}),
        # }
        fields = '__all__'


class AssetListFilterForm(forms.Form):
    name = forms.CharField(required=False, label='关键字')