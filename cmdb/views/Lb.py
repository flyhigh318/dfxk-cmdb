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
from cmdb.models.Slb import Lb
from django.db.models import Q
from django.utils import timezone


listview_lazy_url = 'cmdb:lb_list'
listview_template = 'cmdb/lb_list.html'
formview_template = 'cmdb/lb_form.html'

class LbUpdateSql(object):

    def __init__(self, account):
        self.account = account

    def insert_sql(self, kwargs):
        if Lb.objects.filter(ip_address=kwargs['ip_address']):
            Lb.objects.filter(ip_address=kwargs['ip_address']).update(
                 name=kwargs['name'],
                 load_balancer_id=kwargs['load_balancer_id'],
                 resource_group_id=kwargs['resource_group_id'],
                 ip_address=kwargs['ip_address'],
                 status=kwargs['status'],
                 ip_type=kwargs['ip_type'],
                 region_id=kwargs['region_id'],
                 listen_ports=kwargs['listen_ports'],
                 listen_protocal=kwargs['listen_protocal'],
                 buy_date=kwargs['buy_date'],
                 update_time=timezone.now()
            )
        else:
             Lb.objects.create(
                 name=kwargs['name'],
                 load_balancer_id=kwargs['load_balancer_id'],
                 resource_group_id=kwargs['resource_group_id'],
                 ip_address=kwargs['ip_address'],
                 status=kwargs['status'],
                 ip_type=kwargs['ip_type'],
                 region_id=kwargs['region_id'],
                 listen_ports=kwargs['listen_ports'],
                 listen_protocal=kwargs['listen_protocal'],
                 buy_date=kwargs['buy_date'],
                 account=kwargs['account'],
                 comment=kwargs['comment']
             )

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
        info_valid['name'] = obj['LoadBalancerName']
        info_valid['load_balancer_id'] = obj['LoadBalancerId']
        info_valid['resource_group_id'] = obj['ResourceGroupId']
        info_valid['ip_address'] = obj['Address']
        info_valid['status'] =  1 if obj['LoadBalancerStatus'] == 'active' else 0
        info_valid['ip_type'] = obj['AddressType']
        info_valid['region_id'] = obj['RegionId']
        listener_port_list = []
        listener_protocol_list = []

        for i_dict in obj['ListenerPortsAndProtocal']['ListenerPortAndProtocal']:
                listener_port_list.append(str(i_dict['ListenerPort']))
                listener_protocol_list.append(i_dict['ListenerProtocal'])
        if len(listener_port_list) > 1:
               info_valid['listen_ports'] = '|'.join(listener_port_list)
               info_valid['listen_protocal'] = '|'.join(listener_protocol_list)
        elif len(listener_port_list)  == 1:
               info_valid['listen_ports'] = listener_port_list[0]
               info_valid['listen_protocal'] = listener_protocol_list[0]

        info_valid['buy_date'] = obj['CreateTime']
        info_valid['account'] = Yun_Account.objects.get(name=self.account)
        info_valid['comment'] = obj['LoadBalancerName']
        self.insert_sql(info_valid)

    def get_load_balancer_id(self):
        api_parameter = {
            'Action': 'DescribeLoadBalancers',
            'RegionId': 'cn-shenzhen'
        }
        common = CommonParameter(self.account).get_slb_parameter()
        common['Version'] = '2014-05-15'
        result = UrlRequest(api_parameter).getResult(common)
        # print('result: ', result)
        result = json.loads(result)
        a_list = result['LoadBalancers']['LoadBalancer']
        # print('a_list: ', a_list)
        lb_id = []
        for obj in a_list:
            lb_id.append(obj['LoadBalancerId'])
        return lb_id

class LbView(LoginRequiredMixin, OrderableListMixin, ListView):
    model = Lb
    paginate_by = PER_PAGE
    template_name = listview_template
    context_object_name = 'result_list'
    orderable_columns_default = 'id'
    orderable_columns = ['name', 'create_time', 'update_time']

    def sync_lb(self):
        try:
            for obj in Yun_Account.objects.filter(name__isnull=False):
                if obj.name != '东方星空':
                    instance = LbUpdateSql(obj.name)
                    lb_id_list = instance.get_load_balancer_id()
                    for loadBalancerId in lb_id_list:
                        instance.update_sql(loadBalancerId)
        except Exception as e:
            print(e)

    def get_queryset(self):
        result_list = Lb.objects.all()
        search = self.request.GET.get('name')
        order_by = self.request.GET.get('order_by')
        ordering = self.request.GET.get('ordering')
        syncAliyun = self.request.GET.get("onclick")
        if syncAliyun == 'syncAliyun':
            self.sync_lb()

        if search:
            try:
                result_list = Lb.objects.filter(Q(name__icontains=search)|
                                            Q(ip_address__icontains=search)|
                                            Q(load_balancer_id__icontains=search)|
                                            Q(region_id__icontains=search)|
                                            Q(listen_ports__icontains=search)|
                                            Q(listen_protocal__icontains=search)|
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
        context = super(LbView, self).get_context_data(**kwargs)
        context['order_by'] = self.request.GET.get('order_by', '')
        context['ordering'] = self.request.GET.get('ordering', 'asc')
        context['filter_form'] = LbListFilterForm(self.request.GET)
        return context

class LbCreateView(LoginRequiredMixin, CreateView):
    model = Lb
    form_class = LbForm
    paginate_by = PER_PAGE
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)

    def get_success_url(self):
        return super(LbCreateView, self).get_success_url()

class LbUpdateView(LoginRequiredMixin, UpdateView):
    model = Lb
    form_class = LbForm
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)
    context_object_name = 'entity'

    def get_context_data(self, **kwargs):
        context = super(LbUpdateView, self).get_context_data(**kwargs)
        context['is_add'] = False
        return context

class LbDeleteView(LoginRequiredMixin, JSONResponseMixin,
                     AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        ids = request.GET.get('id', '')
        if ids != "":
            Lb.objects.filter(pk__in=map(int, ids.split(','))).delete()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})