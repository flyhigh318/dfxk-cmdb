# -*- coding: utf-8 -*-
# @Time    : 2018/4/17 10:08
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : Password.py
# @Software: PyCharm

from braces.views import *
from django.contrib.auth.mixins import *
from django.urls import *
from django.views.generic import *

from cmdb.forms.PasswordForm import PasswordForm, PasswordListFilterForm
from cmdb.models.Password import Password
from cmdb.models.Asset import Assets
from django.db.models import Q
from cobra_main.settings import PER_PAGE
import re


listview_lazy_url = 'cmdb:password_list'
listview_template = 'cmdb/password_list.html'
formview_template = 'cmdb/password_form.html'


class PasswordView(LoginRequiredMixin, OrderableListMixin, ListView):
    model = Password
    paginate_by = PER_PAGE
    template_name = listview_template
    context_object_name = 'result_list'
    orderable_columns_default = 'id'
    orderable_columns = ['name', 'create_time', 'update_time']


    def get_queryset(self):
        result_list = Password.objects.all()
        search = self.request.GET.get('name')
        order_by = self.request.GET.get('order_by')
        ordering = self.request.GET.get('ordering')

        if search:
            if re.search(r'\d+\.\d+.*|\d{1,3}.*', search):
                asset_id = []
                result_asset_list = Assets.objects.filter(Q(intral_ip__icontains=search) |
                                                          Q(internet_ip__icontains=search))
                for obj in result_asset_list:
                    asset_id.append(obj.id)
                result_list = Password.objects.filter(ip_id__in=asset_id)
            else:
                result_list = Password.objects.filter(Q(comment__icontains=search)|
                                                      Q(port__icontains=search)|
                                                      Q(user__icontains=search))

        if order_by:
            if ordering == 'desc':
                result_list = result_list.order_by('-' + order_by)
            else:
                result_list = result_list.order_by(order_by)

        return result_list

    def get_context_data(self, **kwargs):
        context = super(PasswordView, self).get_context_data(**kwargs)
        context['order_by'] = self.request.GET.get('order_by', '')
        context['ordering'] = self.request.GET.get('ordering', 'asc')
        context['filter_form'] = PasswordListFilterForm(self.request.GET)
        return context


class PasswordCreateView(LoginRequiredMixin, CreateView):
    model = Password
    form_class = PasswordForm
    paginate_by = PER_PAGE
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)

    def get_success_url(self):
        return super(PasswordCreateView, self).get_success_url()

class PasswordUpdateView(LoginRequiredMixin, UpdateView):
    model = Password
    form_class = PasswordForm
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)
    context_object_name = 'entity'

    def get_context_data(self, **kwargs):
        context = super(PasswordUpdateView, self).get_context_data(**kwargs)
        context['is_add'] = False
        return context



class PasswordDeleteView(LoginRequiredMixin, JSONResponseMixin,
                     AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        ids = request.GET.get('id', '')
        if ids != "":
            list_id = ids.split(',')
            for id in list_id:
                old_data = []
                pl = Password.objects.filter(id=id)

            Password.objects.filter(pk__in=map(int, ids.split(','))).delete()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})