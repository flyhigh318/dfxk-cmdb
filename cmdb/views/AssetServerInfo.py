# -*- coding: utf-8 -*-
# @Time    : 18-4-6 下午7:45
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : Asset.py
# @Software: dfxk-cmdb
import paramiko
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
import json
from cmdb.models.Password import Password  as KeyPass

from cmdb.models import Assets

listview_template = 'cmdb/asset_server_list.html'


class AssetServerInfoView(View):
    template_name = listview_template

    def get(self, request):
        id = request.GET.get("id")
        type = request.GET.get("type")
        ret = {}
        try:
            if isinstance(id, str):
                if type == 'search':
                    ret['code'] = 200
                    cmd_dict = { "dockerServers": "docker ps",
                                 "javaServers": "ps -ef | grep -Ei '(java|PPID)' |  grep -v grep",
                                 "load": "uptime",
                                 "ports": "netstat -tlunp",
                                 "disk": "df -lh"
                              }
                    ret = AssetServersInfo(id).get_server_info(**cmd_dict)
                else:
                    ret['code'] = 400
                    ret['error'] = "parames type is wrong"
        except Exception as e:
            ret['code'] = 405
            ret['error'] = str(e)
        finally:
            return render(request, 'cmdb/asset_server_list.html', {'ret': json.dumps(ret)})

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
        obj = KeyPass.objects.get(ip_id=self.id)
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



