# -*- coding: utf-8 -*-
# @Time    : 2018/5/8 13:51
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : Domain.py
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


listview_lazy_url = 'cmdb:domain_list'
listview_template = 'cmdb/domain_list.html'
formview_template = 'cmdb/domain_form.html'

class DomainsUpdateSql(object):

    def __init__(self, account):
        self.account = account

    def insert_sql(self, **kwargs):
        if Domain.objects.filter(domain_name=kwargs['domain_name']):
            Domain.objects.filter(domain_name=kwargs['domain_name']).update(
                 # domain_name=kwargs['domain_name'],
                 domain_id=kwargs['domain_id'],
                 dns_servers=kwargs['dns_servers'],
                 ali_domain=kwargs['ali_domain'],
                 version_name=kwargs['version_name'],
                 update_time=self.get_date_time()
            )
        else:
             Domain.objects.create(
                 domain_name=kwargs['domain_name'],
                 domain_id=kwargs['domain_id'],
                 dns_servers=kwargs['dns_servers'],
                 ali_domain=kwargs['ali_domain'],
                 version_name=kwargs['version_name'],
                 account=kwargs['account'],
             )

    def update_sql(self):
        api_parameter = {
            'Action': 'DescribeDomains',
            'RegionId': 'cn-shenzhen',
            'PageNumber': '1',
            'PageSize': '50'
        }
        common = CommonParameter(self.account).get_dns_parameter()
        result = UrlRequest(api_parameter).getResult(common)
        result = json.loads(result)
        obj = result
        print(obj)
        info_valid = {}
        domain_list = obj['Domains']['Domain']
        if isinstance(domain_list, list):
            for domain_dict in domain_list:
                info_valid['domain_name'] = domain_dict['DomainName']
                info_valid['domain_id'] = domain_dict['DomainId']
                if isinstance(domain_dict['DnsServers']['DnsServer'], list):
                    info_valid['dns_servers'] = '|'.join(domain_dict['DnsServers']['DnsServer'])
                info_valid['ali_domain'] = domain_dict['AliDomain']
                info_valid['version_name'] =  domain_dict['VersionName']
                info_valid['account'] = Yun_Account.objects.get(name=self.account)
                self.insert_sql(**info_valid)
        else:
            print("domain_list is not a list")

    def get_date_time(self):
        dt_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return dt_str

class DomainsSyncView(LoginRequiredMixin, ListView):
    model = Domain
    paginate_by = PER_PAGE
    template_name = listview_template
    context_object_name = 'result_list'
    orderable_columns_default = 'id'
    orderable_columns = ['name', 'create_time', 'update_time']

    def sync_domain(self):
        try:
            for obj in Yun_Account.objects.filter(name__isnull=False):
                if obj.name != '东方星空':
                    DomainsUpdateSql(obj.name).update_sql()
        except Exception as e:
            print(e)

    def get_queryset(self):
        result_list = Domain.objects.all()
        self.sync_domain()
        return result_list

    def get_context_data(self, **kwargs):
        context = super(DomainsSyncView, self).get_context_data(**kwargs)
        context['order_by'] = self.request.GET.get('order_by', '')
        context['ordering'] = self.request.GET.get('ordering', 'asc')
        context['filter_form'] = DomainListFilterForm(self.request.GET)
        return context

class DomainsView(LoginRequiredMixin, OrderableListMixin, ListView):
    model = Domain
    paginate_by = PER_PAGE
    template_name = listview_template
    context_object_name = 'result_list'
    orderable_columns_default = 'id'
    orderable_columns = ['name', 'create_time', 'update_time']


    def get_queryset(self):
        result_list = Domain.objects.all()
        search = self.request.GET.get('name')
        order_by = self.request.GET.get('order_by')
        ordering = self.request.GET.get('ordering')

        if search:
            try:
                result_list = Domain.objects.filter(Q(domain_name__icontains=search)|
                                            Q(domain_id__icontains=search)|
                                            Q(dns_servers__icontains=search)|
                                            Q(ali_domain__icontains=search)|
                                            Q(version_name__icontains=search)|
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
        context = super(DomainsView, self).get_context_data(**kwargs)
        context['order_by'] = self.request.GET.get('order_by', '')
        context['ordering'] = self.request.GET.get('ordering', 'asc')
        context['filter_form'] = DomainListFilterForm(self.request.GET)
        return context

class DomainsCreateView(LoginRequiredMixin, CreateView):
    model = Domain
    form_class = DomainForm
    paginate_by = PER_PAGE
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)

    def get_success_url(self):
        return super(DomainsCreateView, self).get_success_url()

class DomainsUpdateView(LoginRequiredMixin, UpdateView):
    model = Domain
    form_class = DomainForm
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)
    context_object_name = 'entity'

    def get_context_data(self, **kwargs):
        context = super(DomainsUpdateView, self).get_context_data(**kwargs)
        context['is_add'] = False
        return context

class DomainsDeleteView(LoginRequiredMixin, JSONResponseMixin,
                     AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        ids = request.GET.get('id', '')
        if ids != "":
            Domain.objects.filter(pk__in=map(int, ids.split(','))).delete()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})