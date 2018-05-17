# -*- coding: utf-8 -*-
# @Time    : 2018/4/17 9:37
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : Password.py
# @Software: PyCharm

from django.db import models
from common.models import BaseModel
from cmdb.models.Asset import Assets

class Password(BaseModel):
    ip = models.ForeignKey(Assets, null=True, blank=True, related_name="ip", verbose_name="资产ip")
    port = models.CharField(max_length=255, null=True, blank=True,verbose_name='端口')
    user = models.CharField(max_length=255, null=True, blank=True,verbose_name='用户')
    password = models.CharField(max_length=255, null=True, blank=True,verbose_name='密码')
    comment = models.CharField(max_length=255, null=True, blank=True,verbose_name='备注')

    # def __repr__(self):
    #     return '<Project(name=%s)>' % self.port

    def __str__(self):
        return self.port

    class Meta:
        verbose_name = "密码表"
        verbose_name_plural = verbose_name