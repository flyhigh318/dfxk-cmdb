# -*- coding: utf-8 -*-
"""cobra_main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers

# from deploy_manager.serializer import UserViewSet
from common import views
# from common.views import LoginView
# from deploy_manager.views import *
from cobra_main import settings

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', views.index, name='mainform'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^personal/',views.personal,name='personal'),
    url(r'^mainform/$', views.mainform, name='mainform'),
    url(r'^dashboard/', include('common.urls')),
    url(r'^frontend/common/', include('common.urls')),
    url(r'^frontend/cmdb/', include('cmdb.urls', namespace='cmdb')),
    url(r'^frontend/base_auth/', include('base_auth.urls', namespace='base_auth')),
]



# admin.site.site_header = 'cobra_main'
# admin.site.site_title = 'cobra_main'
