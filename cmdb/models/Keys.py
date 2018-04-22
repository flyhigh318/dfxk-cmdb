# -*- coding: utf-8 -*-
# @Time    : 2018/4/3 13:37
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : Keys.py
# @Software: PyCharm

from django.db import models
from common.models import BaseModel
from cmdb.models.YunAccount import Yun_Account

class Key(BaseModel):
    account = models.ForeignKey(Yun_Account, null=True, blank=True, related_name="account", verbose_name="云账号")
    access_key = models.CharField(max_length=255, null=False, blank=False, verbose_name='密钥ID')
    key_secret = models.CharField(max_length=255, null=False, blank=False,verbose_name='密匙')
    comment = models.CharField(max_length=255, null=True, blank=True, verbose_name='备注')

    def __repr__(self):
        return '<Key(access_key=%s)>' % self.access_key

    # def __str__(self):
    #     return self.access_key

    class Meta:
        verbose_name = "密钥"
        verbose_name_plural = verbose_name
