# -*- coding: utf-8 -*-
# @Time    : 18-4-6 下午7:45
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : Asset.py
# @Software: dfxk-cmdb

from braces.views import *
from django.contrib.auth.mixins import *
from django.urls import *
from django.views.generic import *

from cmdb.forms.Asset import AssetForm, AssetListFilterForm
from cmdb.models.Asset import Assets
from cobra_main.settings import PER_PAGE
from django.db.models import Q

listview_lazy_url = 'cmdb:asset_list'
listview_template = 'cmdb/asset_list.html'
formview_template = 'cmdb/asset_form.html'


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
            list_id = ids.split(',')
            for id in list_id:
                old_data = []
                pl = Assets.objects.filter(id=id)

            Assets.objects.filter(pk__in=map(int, ids.split(','))).delete()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})