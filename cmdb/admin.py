# -*- coding: utf-8 -*-
# Author: Maksim.G
from django.contrib.admin import forms

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin



class CobraAdmin(UserAdmin):# 显示在管理页面的字段
    list_display = ('username','email', 'first_name', 'last_name', 'is_active','is_superuser','is_staff', 'last_login')
    list_filter = ('is_staff','is_superuser')
    search_fields = ('username','last_name','first_name', 'last_name')

class CobraGroupAdmin(GroupAdmin):# 显示在管理页面的字段
    list_display = ('name')
    # list_filter = ('is_staff','is_superuser')
    # search_fields = ('username','last_name','first_name', 'last_name')

class AssetAdmin(admin.ModelAdmin):
    list_display = (
        'hostname', 'asset_type','idc', 'number', 'rack', 'position', 'registrant', 'date_put',
        'status', 'system_type',)
    search_fields = ['hostname', 'idc__name', 'asset_type']
    list_filter = ('brand', 'idc', 'asset_type')

class IDCAdmin(admin.ModelAdmin):
    list_display = ('name','linkman', 'phone', 'comment')

class IpAddressAdmin(admin.ModelAdmin):
    list_display = ('address', 'status', 'alive', 'subnet', 'asset', 'vm',)
    search_fields = ['subnet__address','address']

class SaltMasterAdmin(admin.ModelAdmin):
    list_display = ('name', 'idc', 'asset', 'vm', 'salt_user','salt_url', 'description')
    def has_delete_permission(self, request, obj=None):
        return False



# admin.site.unregister(User)
# admin.site.register(User, CobraAdmin)
# admin.site.register(IDC, IDCAdmin)
# admin.site.register(Asset, AssetAdmin)
# admin.site.register(IpAddressNew, IpAddressAdmin)
# admin.site.register(SaltMaster, SaltMasterAdmin)

