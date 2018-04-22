# -*- coding: utf-8 -*-
# @Time    : 2018/4/4 11:10
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : Kyes.py
# @Software: PyCharm

from braces.views import *
from django.contrib.auth.mixins import *
from django.urls import *
from django.views.generic import *

from cmdb.forms import *
from cmdb.models import *
from cobra_main.settings import PER_PAGE


listview_lazy_url = 'cmdb:keys_list'
listview_template = 'cmdb/keys_list.html'
formview_template = 'cmdb/keys_form.html'


class KeysView(LoginRequiredMixin, OrderableListMixin, ListView):
    model = Key
    paginate_by = PER_PAGE
    template_name = listview_template
    context_object_name = 'result_list'
    orderable_columns_default = 'id'
    orderable_columns = ['access_key', 'comment', 'create_time', 'update_time']

    def get_queryset(self):
        result_list = Key.objects.all()
        order_by = self.request.GET.get('order_by')
        ordering = self.request.GET.get('ordering')
        if order_by:
            if order_by == 'account':
                account_sr = []
                for i in result_list:
                    account_sr.append(i.account.name)
                account_sr_1 = Yun_Account.objects.filter(name__in=account_sr)
                if account_sr_1:
                    key_id = []
                    for i in account_sr_1:
                        key_id.append(i.id)
                    print(key_id)
                    result_list = Key.objects.filter(account_id__in=key_id)

            if ordering == 'asc':
                result_list = result_list.order_by('-' + order_by)
                print("desc: {0}".format(result_list))
            else:
                result_list = result_list.order_by(order_by)
                print("asc: {0}".format(result_list))
        return result_list


class KeysCreateView(LoginRequiredMixin, CreateView):
    model = Key
    form_class = KeyForm
    paginate_by = PER_PAGE
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)

    def get_success_url(self):
        return super(KeysCreateView, self).get_success_url()

class KeysUpdateView(LoginRequiredMixin, UpdateView):
    model = Key
    form_class = KeyForm
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)
    context_object_name = 'entity'

    def get_context_data(self, **kwargs):
        context = super(KeysUpdateView, self).get_context_data(**kwargs)
        context['is_add'] = False
        return context


class KeysDeleteView(LoginRequiredMixin, JSONResponseMixin, AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        ids = request.GET.get('id', '')
        if ids != "":
            Key.objects.filter(pk__in=map(int, ids.split(','))).delete()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})