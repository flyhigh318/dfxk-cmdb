# - *- coding: utf- 8 - *-
from django.contrib.auth.models import User
from django.db import models


class BaseModel(models.Model):
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        abstract = True


BUG_LEVEL = (
    (1,'建议'),
    (2,'待优化'),
    (3,'功能'),
    (4,'高危'),
    (5,'致命')
)
class BugList(BaseModel):
    title = models.CharField(max_length=256, null=True,blank=True,verbose_name="标题名称")
    context = models.TextField(null=True,blank=True,verbose_name="描述内容")
    level = models.IntegerField(choices=BUG_LEVEL, null=True,blank=True,verbose_name="")
    submitter = models.ForeignKey(User,null=True, blank=True,verbose_name="", related_name='sub_user')
    resolver = models.ForeignKey(User,null=True,blank=True,verbose_name="", related_name='solve_user')
