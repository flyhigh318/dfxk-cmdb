# -*- coding: utf-8 -*-
# @Time    : 2018/5/8 9:53
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : Domain.py
# @Software: PyCharm

from django.db import models
from common.models import BaseModel
from cmdb.models.Asset import Assets
from cmdb.models.Slb import Lb
from cmdb.models.YunAccount import Yun_Account

class Domain(BaseModel):
    domain_name = models.CharField(max_length=255, null=False, blank=False, verbose_name='域名名称')
    domain_id = models.CharField(max_length=255, null=True, blank=True, verbose_name='域名ID')
    dns_servers = models.CharField(max_length=255, null=True, blank=True, verbose_name='DNS服务器')
    ali_domain = models.NullBooleanField(null=True, blank=True, default=True, verbose_name='阿里云域名')
    version_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='厂商')
    account = models.ForeignKey(Yun_Account, null=True, blank=True, related_name='domain',verbose_name="云账号")
    comment = models.CharField(max_length=255, null=True, blank=True, default=' ', verbose_name='备注')

    def __str__(self):
        return '%s' % self.domain_name

    class Meta:
        verbose_name = "域名信息"
        verbose_name_plural = verbose_name

class Domain_Records(BaseModel):
    name = models.ForeignKey(Domain,blank=True, null=True, related_name="domain_records1", verbose_name='域名名称')
    rr = models.CharField(max_length=255, null=True, blank=True, verbose_name='记录')
    status = models.CharField(max_length=255, null=True, blank=True, verbose_name='状态')
    value = models.CharField(max_length=255, null=True, blank=True, verbose_name='解析值')
    type = models.CharField(max_length=255, null=True, blank=True, verbose_name='记录类型')
    lock = models.NullBooleanField(null=True, blank=True, default=False, verbose_name="上锁")
    line = models.CharField(max_length=255, null=True, blank=True, verbose_name='解析线路')
    ttl = models.CharField(max_length=255, null=True, blank=True, verbose_name='生存值')
    comment = models.CharField(max_length=255, null=True, blank=True, default=' ', verbose_name='备注')


    def __str__(self):
        return '%s' % self.rr

    class Meta:
        verbose_name = "域名记录"
        verbose_name_plural = verbose_name