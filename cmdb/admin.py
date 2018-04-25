# -*- coding: utf-8 -*-
# Author: Maksim.G
from django.contrib.admin import forms

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group
from cmdb.models.YunAccount import Yun_Account




class CobraAdmin(UserAdmin):# 显示在管理页面的字段
    list_display = ('username','email', 'first_name', 'last_name', 'is_active','is_superuser','is_staff', 'last_login')
    list_filter = ('is_staff','is_superuser')
    search_fields = ('username','last_name','first_name', 'last_name')

class CobraGroupAdmin(GroupAdmin):# 显示在管理页面的字段
    list_display = ('name')
    # list_filter = ('is_staff','is_superuser')
    # search_fields = ('username','last_name','first_name', 'last_name')


class YunAccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'comment')






admin.site.unregister(User)
admin.site.register(User, CobraAdmin)
admin.site.register(Yun_Account, YunAccountAdmin)
# admin.site.register(IDC, IDCAdmin)
# admin.site.register(Asset, AssetAdmin)
# admin.site.register(IpAddressNew, IpAddressAdmin)
# admin.site.register(SaltMaster, SaltMasterAdmin)

