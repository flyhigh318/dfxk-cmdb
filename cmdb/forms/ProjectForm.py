# -*- coding: utf-8 -*-
# @Time    : 2018/3/28 15:50
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : __init__.py
# @Software: PyCharm


from django import forms
from cmdb.models.Project import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        # widgets = {
        #     'rental_date': forms.DateInput(attrs={'class':'datepicker'}),
        # }
        fields = '__all__'


class ProjectListFilterForm(forms.Form):
    name = forms.CharField(required=False, label='关键字')