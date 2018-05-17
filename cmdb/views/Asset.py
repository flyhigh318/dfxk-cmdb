# -*- coding: utf-8 -*-
# @Time    : 18-4-6 下午7:45
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : Asset.py
# @Software: dfxk-cmdb
import paramiko
from braces.views import *
from django.contrib.auth.mixins import *
from django.http import HttpResponse
from django.urls import *
from django.views.generic import *

from cmdb.forms.Asset import AssetForm, AssetListFilterForm
from cmdb.models.Asset import Assets
from cmdb.models.Password import Password  as KeyPass
from cmdb.models.YunAccount import Yun_Account
from cobra_main.settings import PER_PAGE
from django.db.models import Q

from django.contrib.auth.models import User

from aliyun_api.common.Aliyun import UrlRequest
from aliyun_api.common.Parameter import CommonParameter
import json
from django.utils import timezone

listview_lazy_url = 'cmdb:asset_list'
listview_template = 'cmdb/asset_list.html'
formview_template = 'cmdb/asset_form.html'


class AssetEcsUpdateSql(object):

    def __init__(self, account):
        self.account = account

    def insert_sql(self, kwargs):
        if Assets.objects.filter(intral_ip=kwargs['intral_ip']):
            Assets.objects.filter(intral_ip=kwargs['intral_ip']).update(
                 vps_id=kwargs['vps_id'],
                 vps_name=kwargs['vps_name'],
                 internet_ip=kwargs['internet_ip'],
                 system_version=kwargs['system_version'],
                 core_cpu=kwargs['core_cpu'],
                 memory=kwargs['memory'],
                 status=kwargs['status'],
                 buy_date=kwargs['buy_date'],
                 deadline=kwargs['deadline'],
                 update_time=timezone.now()
            )
        else:
             Assets.objects.create(
                 intral_ip=kwargs['intral_ip'],
                 intral_net=self.get_net(),
                 vps_id=kwargs['vps_id'],
                 vps_name=kwargs['vps_name'],
                 internet_ip=kwargs['internet_ip'],
                 system_version=kwargs['system_version'],
                 core_cpu=kwargs['core_cpu'],
                 memory=kwargs['memory'],
                 status=kwargs['status'],
                 buy_date=kwargs['buy_date'],
                 deadline=kwargs['deadline'],
                 account=Yun_Account.objects.get(name__icontains=self.account),
                 comment=kwargs['vps_name']
             )

    def update_sql(self):
        api_parameter = {
            'Action': 'DescribeInstances',
            'RegionId': 'cn-shenzhen',
            'PageNumber': '1',
            'PageSize': '50'
        }
        common = CommonParameter(self.account).get_vps_parameter()
        result = UrlRequest(api_parameter).getResult(common)
        result = json.loads(result)
        a_list = result['Instances']['Instance']
        for obj in a_list:
            info_valid = {}
            info_valid['vps_id'] = obj['InstanceId']
            info_valid['memory'] = int(obj['Memory']/1024)
            info_valid['core_cpu'] = int(obj['Cpu'])
            info_valid['buy_date'] = obj['StartTime']
            info_valid['deadline'] = obj['ExpiredTime']
            info_valid['vps_name'] = obj['InstanceName']
            info_valid['system_version'] = obj['OSName']
            info_valid['status'] = 1 if obj['Status'] == 'Running' else 0
            info_valid['intral_ip'] = obj['VpcAttributes']['PrivateIpAddress']['IpAddress'][0]
            info_valid['internet_ip'] = obj['PublicIpAddress']['IpAddress'][0]
            self.insert_sql(info_valid)

    def get_net(self):
        if self.account == 'tiantianqiandai':
            intral_net = '172.18.16.0/20'
        elif self.account == 'tiantianjiekuan':
            intral_net = '172.18.144.0/20'
        return intral_net


class AssetSyncView(LoginRequiredMixin, ListView):
    model = Assets
    paginate_by = PER_PAGE
    template_name = listview_template
    context_object_name = 'result_list'
    orderable_columns_default = 'id'
    orderable_columns = ['name', 'create_time', 'update_time']

    def sync_asset(self):
        try:
            for obj in Yun_Account.objects.filter(name__isnull=False):
                if obj.name != '东方星空':
                    AssetEcsUpdateSql(obj.name).update_sql()
        except Exception as e:
            print(e)

    def get_queryset(self):
        result_list = Assets.objects.all()
        self.sync_asset()
        return result_list

    def get_context_data(self, **kwargs):
        context = super(AssetSyncView, self).get_context_data(**kwargs)
        context['order_by'] = self.request.GET.get('order_by', '')
        context['ordering'] = self.request.GET.get('ordering', 'asc')
        context['filter_form'] = AssetListFilterForm(self.request.GET)
        return context
    
class AssetView(LoginRequiredMixin, OrderableListMixin, ListView):
    model = Assets
    paginate_by = PER_PAGE
    template_name = listview_template
    context_object_name = 'result_list'
    orderable_columns_default = 'id'
    orderable_columns = ['name', 'create_time', 'update_time']

    def get_queryset(self):
        result_list = Assets.objects.all()
        search = self.request.GET.get('name')
        order_by = self.request.GET.get('order_by')
        ordering = self.request.GET.get('ordering')
        if search:
            result_list = Assets.objects.filter(Q(intral_ip__icontains=search)|
                                                Q(vps_id__icontains=search)|
                                                Q(vps_name__icontains=search)|
                                                Q(intral_net__icontains=search)|
                                                Q(internet_ip__icontains=search)|
                                                Q(system_version__icontains=search))
            return  result_list
        if order_by:
            if ordering == 'desc':
                result_list = result_list.order_by('-' + order_by)
            else:
                result_list = result_list.order_by(order_by)
        return result_list

    def get_context_data(self, **kwargs):
        context = super(AssetView, self).get_context_data(**kwargs)
        context['order_by'] = self.request.GET.get('order_by', '')
        context['ordering'] = self.request.GET.get('ordering', 'asc')
        context['filter_form'] = AssetListFilterForm(self.request.GET)
        return context

class AssetCreateView(LoginRequiredMixin, CreateView):
    model = Assets
    form_class = AssetForm
    paginate_by = PER_PAGE
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)

    def get_success_url(self):
        return super(AssetCreateView, self).get_success_url()

class AssetUpdateView(LoginRequiredMixin, UpdateView):
    model = Assets
    form_class = AssetForm
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)
    context_object_name = 'entity'

    def get_context_data(self, **kwargs):
        context = super(AssetUpdateView, self).get_context_data(**kwargs)
        context['is_add'] = False
        return context

class AssetDeleteView(LoginRequiredMixin, JSONResponseMixin,
                     AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        ids = request.GET.get('id', '')
        if ids != "":
            Assets.objects.filter(pk__in=map(int, ids.split(','))).delete()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})

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
        ssh.close()
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
                    ret['code'] = 200
                    kwargs = {"dockerServers": "docker ps",
                              "javaServers": "ps -ef | grep -Ei '(/app|/tm|PPID)' | grep -Ei '(java|PPID)' | grep -v grep",
                              "load": "uptime",
                              "ports": "netstat -tlunp"
                              }
                    ret = AssetServersInfo(id).get_server_info(**kwargs)
                else:
                    ret['code'] = 400
                    ret['message'] = "parames type is wrong"
                return HttpResponse(json.dumps(ret), content_type="application/json")
    except Exception as e:
        ret['code'] = 403
        ret['message'] = e
        return HttpResponse(json.dumps(ret), content_type="application/json")




