# -*- coding: utf-8 -*-
# @Time    : 2018/5/3 14:02
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : Slb.py
# @Software: PyCharm

from django.db import models
from common.models import BaseModel
from cmdb.models.Asset import Assets
from cmdb.models.YunAccount import Yun_Account

class Docker_Registry(BaseModel):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name='仓库名称')
    comment = models.CharField(max_length=255, null=True, blank=True, default=' ', verbose_name='备注')


    def __str__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = "docker_registry"
        verbose_name_plural = verbose_name

class Docker_Tag(BaseModel):
    registry = models.ForeignKey(Docker_Registry,blank=True, null=True, related_name="dockerid", verbose_name='registry名称')
    tag = models.CharField(max_length=255, null=True, blank=True, verbose_name='版本')
    cmd = models.CharField(max_length=255, null=True, blank=True, verbose_name='cmd')
    comment = models.CharField(max_length=255, null=True, blank=True, default=' ', verbose_name='备注')

    def __str__(self):
        return '%s' % self.tag

    class Meta:
        verbose_name = "docker_tag"
        verbose_name_plural = verbose_name
