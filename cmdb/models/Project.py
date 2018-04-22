# -*- coding: utf-8 -*-
# @Time    : 2018/3/28 15:50
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : __init__.py
# @Software: PyCharm

from django.db import models
from common.models import BaseModel
from cmdb.models.ProductLine import Product_line
from cmdb.models.Asset import Assets

class Project(BaseModel):
    product = models.ForeignKey(Product_line, null=True, blank=True, related_name="product", verbose_name="产品")
    env = models.IntegerField(blank=True, choices=[(1, '正式'), (2, '测试')], default=0, null=True, verbose_name='环境')
    domain = models.CharField(max_length=255, null=True, blank=True, verbose_name='域名')
    website = models.CharField(max_length=255, null=True, blank=True, verbose_name='网址')
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name='项目')
    path = models.CharField(max_length=255, null=True, blank=True, default='null', verbose_name='路径')
    # slb = models.ManyToManyField(Slb, blank=False, null=False, related_name="slb", verbose_name='slb')
    asset = models.ManyToManyField(Assets, blank=False, null=False, related_name="asset", verbose_name='内网ip')
    comment = models.CharField(max_length=255, null=True, blank=True,verbose_name='备注')

    def __repr__(self):
        return '<Project(name=%s)>' % self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "项目"
        verbose_name_plural = verbose_name