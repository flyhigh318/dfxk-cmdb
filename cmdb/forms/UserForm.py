# -*- coding: utf-8 -*-
# @Time    : 2018/4/4 17:33
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : UserForm.py
# @Software: PyCharm

from django.contrib.auth.models import User
from django.forms import ModelForm


class UserProfileForm(ModelForm):

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email', 'is_active', 'is_staff', 'date_joined','last_login']