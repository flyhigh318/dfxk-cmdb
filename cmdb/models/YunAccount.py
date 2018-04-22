# -*- coding: utf-8 -*-
# @Time    : 2018/4/3 13:37
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : YunAccountForm.py
# @Software: PyCharm

from django.db import models
from common.models import BaseModel

class Yun_Account(BaseModel):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name='云账号')
    comment = models.CharField(max_length=255, null=True, blank=True, default=' ', verbose_name='备注')

    def __repr__(self):
        return '<Yun_Account(name=%s)>' % self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "云账号"
        verbose_name_plural = verbose_name
