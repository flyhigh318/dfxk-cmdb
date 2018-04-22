# -*- coding: utf-8 -*-
# @Time    : 2018/3/28 15:50
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : __init__.py
# @Software: PyCharm

from django.db import models
from common.models import BaseModel

class Product_line(BaseModel):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name='产品线')
    comment = models.CharField(max_length=255, null=True, blank=True,verbose_name='备注')

    def __repr__(self):
        return '<Product_line(name=%s)>' % self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "产品线"
        verbose_name_plural = verbose_name