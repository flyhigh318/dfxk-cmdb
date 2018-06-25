# -*- coding: utf-8 -*-
# @Time    : 2018/4/4 13:53
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : KeyForm.py
# @Software: PyCharm

from django import forms

from cmdb.models.DockerRegistry import Docker_Tag

class DockerTagForm(forms.ModelForm):
    class Meta:
        model = Docker_Tag
        # widgets = {
        #     'rental_date': forms.DateInput(attrs={'class':'datepicker'}),
        # }
        fields = '__all__'


class DockerTagListFilterForm(forms.Form):
    name = forms.CharField(required=False, label='关键字')