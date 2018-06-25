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

from cmdb.forms.DockerTagForm import DockerTagForm, DockerTagListFilterForm
from cmdb.models.DockerRegistry import Docker_Tag
from django.db.models import Q
from cobra_main.settings import PER_PAGE


listview_lazy_url = 'cmdb:docker_tag_list'
listview_template = 'cmdb/docker_tag_list.html'
formview_template = 'cmdb/docker_tag_form.html'


class DockerTagView(LoginRequiredMixin, OrderableListMixin, ListView):
    model = Docker_Tag
    paginate_by = PER_PAGE
    template_name = listview_template
    context_object_name = 'result_list'
    orderable_columns_default = 'id'
    orderable_columns = ['name', 'create_time', 'update_time']


    def get_queryset(self):
        result_list = Docker_Tag.objects.all()
        search = self.request.GET.get('name')
        order_by = self.request.GET.get('order_by')
        ordering = self.request.GET.get('ordering')

        if search:
            result_list = Docker_Tag.objects.filter(Q(registry__name__icontains=search)|
                                                  Q(tag__icontains=search)|
                                                  Q(comment__icontains=search))
        if order_by:
            if ordering == 'desc':
                result_list = result_list.order_by('-' + order_by)
            else:
                result_list = result_list.order_by(order_by)

        return result_list

    def get_context_data(self, **kwargs):
        context = super(DockerTagView, self).get_context_data(**kwargs)
        context['order_by'] = self.request.GET.get('order_by', '')
        context['ordering'] = self.request.GET.get('ordering', 'asc')
        context['filter_form'] = DockerTagListFilterForm(self.request.GET)
        return context


class DockerTagCreateView(LoginRequiredMixin, CreateView):
    model = Docker_Tag
    form_class = DockerTagForm
    paginate_by = PER_PAGE
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)

    def get_success_url(self):
        return super(DockerTagCreateView, self).get_success_url()

class DockerTagUpdateView(LoginRequiredMixin, UpdateView):
    model = Docker_Tag
    form_class = DockerTagForm
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)
    context_object_name = 'entity'

    def get_context_data(self, **kwargs):
        context = super(DockerTagUpdateView, self).get_context_data(**kwargs)
        context['is_add'] = False
        return context



class DockerTagDeleteView(LoginRequiredMixin, JSONResponseMixin,
                     AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        ids = request.GET.get('id', '')
        if ids != "":
            list_id = ids.split(',')
            for id in list_id:
                old_data = []
                pl = Docker_Tag.objects.filter(id=id)

            Docker_Tag.objects.filter(pk__in=map(int, ids.split(','))).delete()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})