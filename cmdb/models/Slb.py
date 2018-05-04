# -*- coding: utf-8 -*-
# @Time    : 2018/5/3 14:02
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : Slb.py
# @Software: PyCharm

from django.db import models
from common.models import BaseModel
from cmdb.models.Asset import Assets

class Lb(BaseModel):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name='LB名称')
    load_balancer_id = models.CharField(max_length=255, null=True, blank=True, verbose_name='LBID')
    resource_group_id = models.CharField(max_length=255, null=True, blank=True, verbose_name='组ID')
    ip_address = models.GenericIPAddressField(null=True, blank=True, unique=True, verbose_name='IP')
    status = models.IntegerField(blank=True, choices=[(1, '激活'), (2, '停止')], default=1, null=True, verbose_name='状态')
    ip_type = models.CharField(max_length=255, null=True, blank=True, verbose_name='IP类型')
    region_id = models.CharField(max_length=255, null=True, blank=True, verbose_name='区域id')
    listen_ports = models.CharField(max_length=255, null=True, blank=True, verbose_name='监听端口')
    listen_protocal = models.CharField(max_length=255, null=True, blank=True, verbose_name='监听协议')
    buy_date = models.DateTimeField(blank=True, null=True, verbose_name='购买日期')
    comment = models.CharField(max_length=255, null=True, blank=True, default=' ', verbose_name='备注')

    def __repr__(self):
        return '<Lb(name=%s)>' % self.name

    class Meta:
        verbose_name = "负载均衡"
        verbose_name_plural = verbose_name

class Backend_Server(BaseModel):
    lb = models.ManyToManyField(Lb,blank=True, null=True, related_name="lbid", verbose_name='LBID')
    server_id = models.ForeignKey(Assets, blank=True, null=True, related_name="assets", verbose_name='Asset')
    weight = models.CharField(max_length=255, null=True, blank=True, verbose_name='权重')
    status = models.IntegerField(blank=True, choices=[(1, '正常'), (2, '异常')], default=0, null=True, verbose_name='状态')
    listen_ports = models.CharField(max_length=255, null=True, blank=True, verbose_name='"监听端口"')
    comment = models.CharField(max_length=255, null=True, blank=True, default=' ', verbose_name='备注')

    def __repr__(self):
        return '<Backend_Server(server_id=%s)>' % self.server_id

    class Meta:
        verbose_name = "后端服务器"
        verbose_name_plural = verbose_name
