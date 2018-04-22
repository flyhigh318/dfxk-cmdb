# -*- coding: utf-8 -*-
# @Time    : 2018/3/28 15:50
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : __init__.py
# @Software: PyCharm

from braces.views import *
from django.contrib.auth.mixins import *
from django.urls import *
from django.views.generic import *

from cmdb.forms.ProductLineForm import ProductLineForm, ProductLineListFilterForm
from cmdb.models.ProductLine import Product_line
from cobra_main.settings import PER_PAGE


listview_lazy_url = 'cmdb:product_line_list'
listview_template = 'cmdb/product_line_list.html'
formview_template = 'cmdb/product_line_form.html'


class ProductLineView(LoginRequiredMixin, OrderableListMixin, ListView):
    model = Product_line
    paginate_by = PER_PAGE
    template_name = listview_template
    context_object_name = 'result_list'
    orderable_columns_default = 'id'
    orderable_columns = ['name', 'create_time', 'update_time']


    def get_queryset(self):
        result_list = Product_line.objects.all()
        order_by = self.request.GET.get('order_by')
        ordering = self.request.GET.get('ordering')
        if order_by:
            if ordering == 'desc':
                result_list = result_list.order_by('-' + order_by)
            else:
                result_list = result_list.order_by(order_by)

        return result_list

    # def get_context_data(self, **kwargs):
    #     context = super(YunAccountView, self).get_context_data(**kwargs)
    #     context['order_by'] = self.request.GET.get('order_by', '')
    #     context['ordering'] = self.request.GET.get('ordering', 'asc')
    #     context['filter_form'] = YunAccountForm(self.request.GET)
    #     return context


class ProductLineCreateView(LoginRequiredMixin, CreateView):
    model = Product_line
    form_class = ProductLineForm
    paginate_by = PER_PAGE
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)

    def get_success_url(self):
        return super(ProductLineCreateView, self).get_success_url()

class ProductLineUpdateView(LoginRequiredMixin, UpdateView):
    model = Product_line
    form_class = ProductLineForm
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)
    context_object_name = 'entity'

    def get_context_data(self, **kwargs):
        context = super(ProductLineUpdateView, self).get_context_data(**kwargs)
        context['is_add'] = False
        return context



class ProductLineDeleteView(LoginRequiredMixin, JSONResponseMixin,
                     AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        ids = request.GET.get('id', '')
        if ids != "":
            list_id = ids.split(',')
            for id in list_id:
                old_data = []
                pl = Product_line.objects.filter(id=id)

            Product_line.objects.filter(pk__in=map(int, ids.split(','))).delete()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})