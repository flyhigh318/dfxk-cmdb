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
import base64

listview_template = 'cmdb/web_ssh.html'


class AssetServerWebSshView(View):
    template_name = listview_template

    def get(self, request):
        id = request.GET.get("id")
        type = request.GET.get("type")
        ret = {}
        retscret = {}
        try:
            if isinstance(id, str):
                if type == 'webssh':
                    ret['code'] = 200
                    ret = AssetServersInfo1(id).get_server_info()
                    retscret['hostname'] = base64.b64encode(str(ret['hostname']).encode('utf-8'))
                    retscret['username'] = base64.b64encode(str(ret['username']).encode('utf-8'))
                    retscret['password'] = base64.b64encode(str(ret['password']).encode('utf-8'))
                    # retscret['port'] = base64.b64encode(str(ret['port']).encode('utf-8'))
                    retscret['hostname'] = str(retscret['hostname'],'utf-8')
                    retscret['username'] = str(retscret['username'],'utf-8')
                    retscret['password'] = str(retscret['password'],'utf-8')
                    retscret['port'] = ret['port']
                    ret = {}
                    ret = retscret
                else:
                    ret['code'] = 400
                    ret['error'] = "parames type is wrong"
        except Exception as e:
            ret['code'] = 405
            ret['error'] = str(e)
        finally:
            print('ret---------->', ret)
            return render(request, 'cmdb/web_ssh.html', ret)

class AssetServersInfo1(object):

    def __init__(self, id):
        self.id = id

    def get_asset_info(self):
        obj = Assets.objects.get(id=self.id)
        ip = obj.intral_ip
        name = obj.vps_name
        return {"ip": ip, "name": name}

    def get_server_info(self):
        info = self.get_asset_info()
        obj = KeyPass.objects.get(ip_id=self.id)
        result = {
            'hostname': info['ip'],
            'username': obj.user,
            'password': obj.password,
            'port': obj.port
        }
        return result



