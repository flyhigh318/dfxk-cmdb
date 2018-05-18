# -*- coding: utf-8 -*-
# @Time    : 2018/5/18 10:15
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : Api.py
# @Software: PyCharm

import paramiko
import json
import re
import IPy
from django.contrib.auth.models import User
from django.http import HttpResponse

from cmdb.models import Assets
from cmdb.models.Password import Password as KeyPassword
from cmdb.models.Domain import Domain_Records
from cmdb.models.Slb import Backend_Server, Lb


class AssetServersInfo(object):

    def __init__(self, id):
        self.id = id

    def get_asset_info(self):
        obj = Assets.objects.get(id=self.id)
        ip = obj.intral_ip
        name = obj.vps_name
        return {"ip": ip, "name": name}

    def get_server_info(self, **kwargs):
        info = self.get_asset_info()
        obj = KeyPassword.objects.get(ip_id=self.id)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(info['ip'], obj.port, obj.user, obj.password)
        for i,v in kwargs.items():
            ret = ""
            stdin, stdout, stderr = ssh.exec_command(v)
            ret = stdout.readlines()
            if len(ret) > 1:
                info[i] = ret
            elif len(ret) == 1:
                if i == 'load':
                    info[i] = ret
        ssh.close()
        return info

class DomainRecordRelatedAssetsInfo(object):
    def __init__(self, id):
        self.id = id

    def get_domain(self):
        info = {}
        obj = Domain_Records.objects.get(pk=self.id)
        info['domain'] = obj.rr + '.' + obj.name.domain_name
        is_ip = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', obj.value, re.M|re.I)
        if not is_ip:
            return info
        obj_qt = Assets.objects.filter(intral_ip=obj.value)
        if obj_qt:
           info['intral_ip'] = obj.value
        else:
            obj_qt = Lb.objects.filter(ip_address=obj.value)
            if obj_qt:
                info['slb_ip'] = obj.value
            else:
                if obj.value in IPy.IP("14.18.154.96/29"):
                    info['dfxk_ip'] = obj.value
                elif obj.value in IPy.IP("183.6.105.128/26"):
                    info['dfxk_ip'] = obj.value
                elif obj.value in IPy.IP("192.168.102.0/24"):
                    info['dfxk_ip'] = obj.value
                elif obj.value in IPy.IP("192.168.103.0/24"):
                    info['dfxk_ip'] = obj.value
                else:
                    info['unkown_ip'] = obj.value
        return info

    def get_intral_ip(self):
        info = self.get_domain()
        if "slb_ip" in info.keys():
            obj = Backend_Server.objects.get(lb__ip_address=info['slb_ip'])
            intral_ip_list = []
            for i in obj.server_id.all():
                intral_ip_list.append(i.intral_ip)
            info['intral_ip'] = intral_ip_list
        return info

def api_asset_server_info(request):

    id = request.GET.get('id')
    type = request.GET.get('type')
    user = request.GET.get('user')
    ret = {}
    try:
        obj = User.objects.get(username=user)
        if obj:
            if isinstance(id, str):
                if type == 'search':
                    ret = {}
                    ret['code'] = 200
                    kwargs = {"dockerServers": "docker ps",
                              "javaServers": "ps -ef | grep -Ei '(/app|/tm|PPID)' | grep -Ei '(java|PPID)' | grep -v grep",
                              "load": "uptime",
                              "ports": "netstat -tlunp",
                              "disk": "df -lh"
                              }
                    ret = AssetServersInfo(id).get_server_info(**kwargs)
                else:
                    ret['code'] = 400
                    ret['message'] = "parames type is wrong"
                return HttpResponse(json.dumps(ret), content_type="application/json")
    except Exception as e:
        ret['code'] = 403
        ret['error'] = str(e)
        return HttpResponse(json.dumps(ret), content_type="application/json")

def api_get_assets(request):
    pass
    domainRcordId = request.GET.get('id')
    type = request.GET.get('type')
    user = request.GET.get('user')
    ret = {}
    try:
        obj = User.objects.get(username=user)
        if obj:
            if isinstance(domainRcordId, str):
                if type == 'search':
                    ret = {}
                    ret['code'] = 200
                    ret = DomainRecordRelatedAssetsInfo(domainRcordId).get_intral_ip()
                    print("ret: ", ret)
                else:
                    ret['code'] = 400
                    ret['message'] = "parames type is wrong"
                return HttpResponse(json.dumps(ret), content_type="application/json")
    except Exception as e:
        ret['code'] = 403
        ret['error'] = str(e)
        return HttpResponse(json.dumps(ret), content_type="application/json")