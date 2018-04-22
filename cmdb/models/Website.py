# -*- coding: utf-8 -*-
# @Time    : 2018/4/19 14:35
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : website.py
# @Software: PyCharm

from django.db import models
from common.models import BaseModel

class Website(BaseModel):
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name='网址')
    use = models.CharField(max_length=255, null=False, blank=False, verbose_name='用途')
    user = models.CharField(max_length=255, null=True, blank=True,  verbose_name='登录账号')
    password = models.CharField(max_length=255, null=True, blank=True, verbose_name='登录密码')
    comment = models.CharField(max_length=255, null=True, blank=True,verbose_name='备注')

    def __repr__(self):
        return '<Project(name=%s)>' % self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "项目"
        verbose_name_plural = verbose_name