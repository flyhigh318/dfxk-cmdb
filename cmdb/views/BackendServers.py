# -*- coding: utf-8 -*-
# @Time    : 2018/5/4 11:21
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : BackendServers.py
# @Software: PyCharm
# -*- coding: utf-8 -*-
# @Time    : 2018/5/3 17:16
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : Lb.py
# @Software: PyCharm

from braces.views import *
from django.contrib.auth.mixins import *
from django.urls import *
from django.views.generic import *

from aliyun_api.common.Aliyun import UrlRequest
from aliyun_api.common.Parameter import CommonParameter
import json, datetime
from cmdb.forms import *
from cmdb.models import *
from cobra_main.settings import PER_PAGE
from cmdb.models.Slb import Backend_Server
from django.db.models import Q


listview_lazy_url = 'cmdb:backend_servers_list'
listview_template = 'cmdb/backend_servers_list.html'
formview_template = 'cmdb/backend_servers_form.html'

class BackendServersUpdateSql(object):

    def __init__(self, account):
        self.account = account

    def insert_sql(self, kwargs):
        if Backend_Server.objects.filter(lb__ip_address=kwargs['ip_address']):
            Backend_Server.objects.filter(lb__ip_address=kwargs['ip_address']).update(
                 lb=Lb.objects.get(load_balancer_id=kwargs['load_balancer_id']),
                 status=kwargs['status'],
                 weight=kwargs['weight'],
                 listen_ports=kwargs['listen_ports'],
                 update_time=self.get_date_time()
            )
            #移除多对多关系对象数据
            bs = Backend_Server.objects.get(lb__ip_address=kwargs['ip_address'])
            a_old = Assets.objects.filter(assets__comment=kwargs['comment'])
            if a_old:
                for obj in a_old:
                    bs.server_id.remove(obj)
            #更新多对多关系对象数据
            if isinstance(kwargs['vps_id_list'], str):
                a = Assets.objects.get(vps_id=kwargs['vps_id_list'])
                bs.server_id.add(a)
            elif isinstance(kwargs['vps_id_list'], list):
                a = Assets.objects.filter(vps_id__in=kwargs['vps_id_list'])
                for obj in a:
                    bs.server_id.add(obj)
        else:
             bs = Backend_Server(
                 lb=Lb.objects.get(load_balancer_id=kwargs['load_balancer_id']),
                 status=kwargs['status'],
                 weight=kwargs['weight'],
                 listen_ports=kwargs['listen_ports'],
                 comment=kwargs['comment']
             )
             bs.save()
             if isinstance(kwargs['vps_id_list'], str):
                 a = Assets.objects.get(vps_id=kwargs['vps_id_list'])
                 bs.server_id.add(a)
             elif isinstance(kwargs['vps_id_list'], list):
                 a = Assets.objects.filter(vps_id__in=kwargs['vps_id_list'])
                 for obj in a:
                     bs.server_id.add(obj)

    def update_sql(self, LoadBalancerId):
        api_parameter = {
            'Action': 'DescribeLoadBalancerAttribute',
            'LoadBalancerId': LoadBalancerId,
            'RegionId': 'cn-shenzhen',
            'PageNumber': '1',
            'PageSize': '50'
        }
        common = CommonParameter(self.account).get_slb_parameter()
        common['Version'] = '2014-05-15'
        result = UrlRequest(api_parameter).getResult(common)
        result = json.loads(result)
        obj = result
        info_valid = {}
        info_valid['load_balancer_id'] = obj['LoadBalancerId']
        info_valid['ip_address'] = obj['Address']

        vps_id_list = []
        weight_list = []
        for i_dict in obj['BackendServers']['BackendServer']:
            vps_id_list.append(i_dict['ServerId'])
            weight_list.append(str(i_dict['Weight']))
        if len(vps_id_list) > 1:
               info_valid['vps_id_list'] = vps_id_list
               info_valid['weight'] = '|'.join(weight_list)
        elif len(vps_id_list)  == 1:
               info_valid['vps_id_list'] = vps_id_list[0]
               info_valid['weight'] = weight_list[0]

        info_valid['status'] =  self.get_backend_server_status(LoadBalancerId)
        info_valid['region_id'] = obj['RegionId']

        listener_port_list = []
        for i in obj['ListenerPorts']['ListenerPort']:
            listener_port_list.append(str(i))
        info_valid['listen_ports'] = '|'.join(listener_port_list)

        info_valid['comment'] = obj['LoadBalancerName']
        print('info_valid:  ', info_valid)
        self.insert_sql(info_valid)

    def get_load_balancer_id(self):
        api_parameter = {
            'Action': 'DescribeLoadBalancers',
            'RegionId': 'cn-shenzhen'
        }
        common = CommonParameter(self.account).get_slb_parameter()
        common['Version'] = '2014-05-15'
        result = UrlRequest(api_parameter).getResult(common)
        result = json.loads(result)
        a_list = result['LoadBalancers']['LoadBalancer']
        lb_id = []
        for obj in a_list:
            lb_id.append(obj['LoadBalancerId'])
        return lb_id

    def get_date_time(self):
        dt_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return dt_str

    def get_backend_server_status(self, LoadBalancerId):
        api_parameter = {
            'Action': 'DescribeHealthStatus',
            'RegionId': 'cn-shenzhen',
            'LoadBalancerId': LoadBalancerId
        }
        common = CommonParameter(self.account).get_slb_parameter()
        common['Version'] = '2014-05-15'
        result = UrlRequest(api_parameter).getResult(common)
        result = json.loads(result)
        for i_dict in result['BackendServers']['BackendServer']:
            if i_dict['ServerHealthStatus'] == 'abnormal':
                statu = u'异常'
                break
        else:
            statu = u'正常'
        return statu


class BackendServersSyncView(LoginRequiredMixin, ListView):
    model = Lb
    paginate_by = PER_PAGE
    template_name = listview_template
    context_object_name = 'result_list'
    orderable_columns_default = 'id'
    orderable_columns = ['name', 'create_time', 'update_time']

    def sync_backend_servers(self):
        try:
            for obj in Yun_Account.objects.filter(name__isnull=False):
                if obj.name != '东方星空':
                    instance = BackendServersUpdateSql(obj.name)
                    lb_id_list = instance.get_load_balancer_id()
                    for loadBalancerId in lb_id_list:
                        instance.update_sql(loadBalancerId)
        except Exception as e:
            raise (e)
            print(e)

    def get_queryset(self):
        result_list = Backend_Server.objects.all()
        self.sync_backend_servers()
        return result_list

    def get_context_data(self, **kwargs):
        context = super(BackendServersSyncView, self).get_context_data(**kwargs)
        context['order_by'] = self.request.GET.get('order_by', '')
        context['ordering'] = self.request.GET.get('ordering', 'asc')
        context['filter_form'] = BackendServersListFilterForm(self.request.GET)
        return context

class BackendServersView(LoginRequiredMixin, OrderableListMixin, ListView):
    model = Backend_Server
    paginate_by = PER_PAGE
    template_name = listview_template
    context_object_name = 'result_list'
    orderable_columns_default = 'id'
    orderable_columns = ['name', 'create_time', 'update_time']


    def get_queryset(self):
        result_list = Backend_Server.objects.all()
        search = self.request.GET.get('name')
        order_by = self.request.GET.get('order_by')
        ordering = self.request.GET.get('ordering')

        if search:
            try:
                result_list = Backend_Server.objects.filter(Q(lb__name__icontains=search)|
                                                            Q(lb__ip_address__icontains=search)|
                                                            Q(server_id__vps_name__icontains=search)|
                                                            Q(server_id__intral_ip__icontains=search)|
                                                            Q(listen_ports__icontains=search)|
                                                            Q(weight__icontains=search)|
                                                            Q(status__icontains=search)|
                                                            Q(comment__icontains=search))
                return result_list
            except Exception as e:
                print(e)


        if order_by:
            if ordering == 'desc':
                result_list = result_list.order_by('-' + order_by)
            else:
                result_list = result_list.order_by(order_by)

        return result_list

    def get_context_data(self, **kwargs):
        context = super(BackendServersView, self).get_context_data(**kwargs)
        context['order_by'] = self.request.GET.get('order_by', '')
        context['ordering'] = self.request.GET.get('ordering', 'asc')
        context['filter_form'] = LbListFilterForm(self.request.GET)
        return context

class BackendServersCreateView(LoginRequiredMixin, CreateView):
    model = Backend_Server
    form_class = BackendServersForm
    paginate_by = PER_PAGE
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)

    def get_success_url(self):
        return super(BackendServersCreateView, self).get_success_url()

class BackendServersUpdateView(LoginRequiredMixin, UpdateView):
    model = Backend_Server
    form_class = BackendServersForm
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)
    context_object_name = 'entity'

    def get_context_data(self, **kwargs):
        context = super(BackendServersUpdateView, self).get_context_data(**kwargs)
        context['is_add'] = False
        return context

class BackendServersDeleteView(LoginRequiredMixin, JSONResponseMixin,
                     AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        ids = request.GET.get('id', '')
        if ids != "":
            Backend_Server.objects.filter(pk__in=map(int, ids.split(','))).delete()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})