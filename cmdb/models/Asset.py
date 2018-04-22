# -*- coding: utf-8 -*-
# @Time    : 2018/3/28 15:50
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : __init__.py
# @Software: PyCharm

from django.db import models
from common.models import BaseModel
from cmdb.models.YunAccount import Yun_Account

class Assets(BaseModel):
    vps_id = models.CharField(max_length=255, null=True, blank=True, unique=True, default=' ', verbose_name='实例ID')
    vps_name = models.CharField(max_length=255, null=True, blank=True, unique=True, default=' ', verbose_name='实例名称')
    intral_ip = models.GenericIPAddressField(null=True, blank=True, unique=True, verbose_name='内网IP')
    intral_net = models.CharField(max_length=255, null=True, blank=True, unique=False, default=' ', verbose_name='内网网段')
    internet_ip = models.GenericIPAddressField(null=True, blank=True, unique=True, verbose_name='外网IP')
    system_version = models.CharField(max_length=255, null=True, blank=True, default=' ', verbose_name='系统版本')
    core_cpu = models.IntegerField(blank=True, null=True, verbose_name='cpu个数')
    memory = models.IntegerField(blank=True, null=True, verbose_name='内存')
    status = models.IntegerField(blank=True, choices=[(1, '运行'), (2, '停止')], default=1, null=True, verbose_name='状态')
    buy_date = models.DateTimeField(blank=True, null=True, verbose_name='购买日期')
    deadline = models.DateTimeField(blank=True, null=True, verbose_name='过期日期')
    account = models.ForeignKey(Yun_Account, null=True, blank=True, related_name="account_1", verbose_name="所属账号")
    comment = models.CharField(max_length=255, null=True, blank=True,verbose_name='备注')

    # def __repr__(self):
    #     return '<Assets(intral_ip=%s)>' % self.intral_ip

    def __str__(self):
        return self.intral_ip

    class Meta:
        verbose_name = "项目"
        verbose_name_plural = verbose_name