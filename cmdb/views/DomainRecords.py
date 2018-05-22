# -*- coding: utf-8 -*-
# @Time    : 2018/5/8 17:09
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : DomainRecords.py
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
from django.db.models import Q
from django.utils import timezone
import re


listview_lazy_url = 'cmdb:domain_record_list'
listview_template = 'cmdb/domain_record_list.html'
formview_template = 'cmdb/domain_record_form.html'

class DomainRecordsUpdateSql(object):

    def __init__(self, domainName, account):
        self.domainName = domainName
        self.account = account

    def insert_sql(self, **kwargs):
        if Domain_Records.objects.filter(rr=kwargs['rr'],
                                         name__domain_name=kwargs['name'],
                                         type=kwargs['type'],
                                         value=kwargs['value']):
            Domain_Records.objects.filter(rr=kwargs['rr'],
                                          name__domain_name=kwargs['name'],
                                          type=kwargs['type'],
                                          value=kwargs['value']
                                          ).update(**kwargs, update_time=timezone.now())
        else:
             Domain_Records.objects.create(**kwargs)

    def update_sql(self):
        api_parameter = {
            'Action': 'DescribeDomainRecords',
            'DomainName': "",
            'RegionId': 'cn-shenzhen',
            'PageNumber': '1',
            'PageSize': '100'
        }
        print("domainName: ", self.domainName)
        api_parameter['DomainName'] = self.domainName if self.domainName else False
        ret = {}
        if api_parameter['DomainName']:
            common = CommonParameter(self.account).get_dns_parameter()
            result = UrlRequest(api_parameter).getResult(common)
            if isinstance(result, str):
                result = json.loads(result)
                obj = result
            else:
                print("result: ", result)
                ret['code'] = 401
                ret['error'] = "there is no type str"
                return ret
        else:
            ret['code'] = 400
            ret['error'] = "there is no related domainName"
            return ret
        record_list = obj['DomainRecords']['Record']
        if isinstance(record_list, list):
            print("record_list: ", record_list)
            if len(record_list) != 0:
                for record_dict in record_list:
                    info_valid = {}
                    info_valid['name'] = Domain.objects.get(domain_name=record_dict['DomainName'])
                    info_valid['rr'] = record_dict['RR']
                    info_valid['status'] = record_dict['Status']
                    info_valid['value'] = record_dict['Value']
                    info_valid['type'] = record_dict['Type']
                    info_valid['lock'] = record_dict['Locked']
                    info_valid['line'] = record_dict['Line']
                    info_valid['ttl'] = str(record_dict['TTL'])
                    self.insert_sql(**info_valid)
        else:
            print("domain_list is not a list")

    def get_date_time(self):
        dt_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return dt_str

class DomainRecordsSyncView(LoginRequiredMixin, ListView):
    model = Domain_Records
    paginate_by = PER_PAGE
    template_name = listview_template
    context_object_name = 'result_list'
    orderable_columns_default = 'id'
    orderable_columns = ['name', 'create_time', 'update_time']

    def sync_domain_record(self):
        try:
            for obj in Domain.objects.filter(domain_name__isnull=False):
                DomainRecordsUpdateSql(obj.domain_name, obj.account.name).update_sql()
        except Exception as e:
            raise e
            print(e)

    def get_queryset(self):
        result_list = Domain_Records.objects.all()
        action = self.request.GET.get("paginate_by")
        if not action:
           self.sync_domain_record()
        return result_list

    def get_context_data(self, **kwargs):
        context = super(DomainRecordsSyncView, self).get_context_data(**kwargs)
        context['order_by'] = self.request.GET.get('order_by', '')
        context['ordering'] = self.request.GET.get('ordering', 'asc')
        context['filter_form'] = DomainRecordsListFilterForm(self.request.GET)
        return context

class DomainRecordsView(LoginRequiredMixin, OrderableListMixin, ListView):
    model = Domain_Records
    paginate_by = PER_PAGE
    template_name = listview_template
    context_object_name = 'result_list'
    orderable_columns_default = 'id'
    orderable_columns = ['name', 'create_time', 'update_time']


    def get_queryset(self):
        result_list = Domain_Records.objects.all()
        search = self.request.GET.get('name')
        order_by = self.request.GET.get('order_by')
        ordering = self.request.GET.get('ordering')

        if search:
            try:
                k = re.search(r'(.*)\.(.*)', search, re.I|re.M)
                if k:
                    m, n = k.groups()
                    if not re.search('com',m) and re.search('com', n):
                        search_list = re.split(r'\.', search)
                        domain = ".".join(search_list[-2:])
                        num_del_tail_2_args = len(search_list) -2
                        rr = ".".join(search_list[0: num_del_tail_2_args])
                        result_list = Domain_Records.objects.filter(name__domain_name__icontains=domain,
                                                                    rr=rr)

                    else:
                        result_list = Domain_Records.objects.filter(Q(rr__icontains=search) |
                                                                    Q(value__icontains=search) |
                                                                    Q(name__domain_name__icontains=search) |
                                                                    Q(comment__icontains=search))
                else:
                    result_list = Domain_Records.objects.filter(Q(rr__icontains=search)|
                                                Q(status__icontains=search)|
                                                Q(value__icontains=search)|
                                                Q(type__icontains=search)|
                                                Q(lock__icontains=search)|
                                                Q(line__icontains=search)|
                                                Q(ttl__icontains=search)|
                                                Q(name__domain_name__icontains=search)|
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
        context = super(DomainRecordsView, self).get_context_data(**kwargs)
        context['order_by'] = self.request.GET.get('order_by', '')
        context['ordering'] = self.request.GET.get('ordering', 'asc')
        context['filter_form'] = DomainRecordsListFilterForm(self.request.GET)
        return context

class DomainRecordsCreateView(LoginRequiredMixin, CreateView):
    model = Domain_Records
    form_class = DomainRecordsForm
    paginate_by = PER_PAGE
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)

    def get_success_url(self):
        return super(DomainRecordsCreateView, self).get_success_url()

class DomainRecordsUpdateView(LoginRequiredMixin, UpdateView):
    model = Domain_Records
    form_class = DomainRecordsForm
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)
    context_object_name = 'entity'

    def get_context_data(self, **kwargs):
        context = super(DomainRecordsUpdateView, self).get_context_data(**kwargs)
        context['is_add'] = False
        return context

class DomainRecordsDeleteView(LoginRequiredMixin, JSONResponseMixin, AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        ids = request.GET.get('id', '')
        if ids != "":
            Domain_Records.objects.filter(pk__in=map(int, ids.split(','))).delete()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})
