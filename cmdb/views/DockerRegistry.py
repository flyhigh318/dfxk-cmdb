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

from cmdb.forms.DockerRegistryForm import DockerRegistryForm, DockerRegistryListFilterForm
from cmdb.models.DockerRegistry import Docker_Registry
from django.db.models import Q
from cobra_main.settings import PER_PAGE

from docker_registry_api.common import Registry
from docker_registry_api.config import DockerRegistryInfo as Info
from cmdb.models.DockerRegistry import Docker_Tag

listview_lazy_url = 'cmdb:docker_registry_list'
listview_template = 'cmdb/docker_registry_list.html'
formview_template = 'cmdb/docker_registry_form.html'


class DockerRegistryData(object):

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Authorization": "Basic " + Info['config']['auths']['registry.docker.dfxkdata.com']['auth'],
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "registry.docker.dfxkdata.com",
        "Pragma": "no-cache",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36",
    }

    def __init__(self, header=headers):
        self.header = header

    def get_registry_data(self):
        Info['headers'] = self.header
        ret = Registry(**Info).get_tags()
        return ret

    def update_sql(self):
        pass
        try:
            ret = self.get_registry_data()
            for i in ret:
                self.insert_sql(**i)
        except Exception as e:
            print(e)

    def insert_sql(self, **kwargs):
        obj = Docker_Registry.objects.filter(name=kwargs['name'])
        if obj:
            for tag, cmd in zip(kwargs['tags'], kwargs['cmds']):
                if len(tag) != 0:
                    obj2 = Docker_Tag.objects.filter(tag=tag).filter(registry__name=kwargs['name'])
                    if not obj2:
                        print(tag)
                        Docker_Tag.objects.create(
                            registry=Docker_Registry.objects.get(name=kwargs['name']),
                            tag=tag,
                            cmd=cmd
                        )
        else:
            Docker_Registry.objects.create(
                name=kwargs['name']
            )
            if len(kwargs['tags']) != 0 :
                for tag, cmd in zip(kwargs['tags'], kwargs['cmds']):
                    Docker_Tag.objects.create(
                        registry=Docker_Registry.objects.get(name=kwargs['name']),
                        tag=tag,
                        cmd=cmd
                    )

class DockerRegistrySyncView(LoginRequiredMixin, OrderableListMixin, ListView):
    model = Docker_Registry
    paginate_by = PER_PAGE
    template_name = listview_template
    context_object_name = 'result_list'
    orderable_columns_default = 'id'
    orderable_columns = ['name', 'create_time', 'update_time']


    def get_queryset(self):
        result_list = Docker_Registry.objects.all()
        search = self.request.GET.get('name')
        order_by = self.request.GET.get('order_by')
        ordering = self.request.GET.get('ordering')
        sync_data = self.request.GET.get('type')


        if sync_data == 'sync':
            DockerRegistryData().update_sql()

        if search:
            result_list = Docker_Registry.objects.filter(Q(name__icontains=search)|
                                                         Q(comment__icontains=search))
        if order_by:
            if ordering == 'desc':
                result_list = result_list.order_by('-' + order_by)
            else:
                result_list = result_list.order_by(order_by)

        return result_list

    def get_context_data(self, **kwargs):
        context = super(DockerRegistrySyncView, self).get_context_data(**kwargs)
        context['order_by'] = self.request.GET.get('order_by', '')
        context['ordering'] = self.request.GET.get('ordering', 'asc')
        context['filter_form'] = DockerRegistryListFilterForm(self.request.GET)
        return context

class DockerRegistryView(LoginRequiredMixin, OrderableListMixin, ListView):
    model = Docker_Registry
    paginate_by = PER_PAGE
    template_name = listview_template
    context_object_name = 'result_list'
    orderable_columns_default = 'id'
    orderable_columns = ['name', 'create_time', 'update_time']


    def get_queryset(self):
        result_list = Docker_Registry.objects.all()
        search = self.request.GET.get('name')
        order_by = self.request.GET.get('order_by')
        ordering = self.request.GET.get('ordering')

        if search:
            result_list = Docker_Registry.objects.filter(Q(name__icontains=search)|
                                                         Q(comment__icontains=search))
        if order_by:
            if ordering == 'desc':
                result_list = result_list.order_by('-' + order_by)
            else:
                result_list = result_list.order_by(order_by)

        return result_list

    def get_context_data(self, **kwargs):
        context = super(DockerRegistryView, self).get_context_data(**kwargs)
        context['order_by'] = self.request.GET.get('order_by', '')
        context['ordering'] = self.request.GET.get('ordering', 'asc')
        context['filter_form'] = DockerRegistryListFilterForm(self.request.GET)
        return context

class DockerRegistryCreateView(LoginRequiredMixin, CreateView):
    model = Docker_Registry
    form_class = DockerRegistryForm
    paginate_by = PER_PAGE
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)

    def get_success_url(self):
        return super(DockerRegistryCreateView, self).get_success_url()

class DockerRegistryUpdateView(LoginRequiredMixin, UpdateView):
    model = Docker_Registry
    form_class = DockerRegistryForm
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)
    context_object_name = 'entity'

    def get_context_data(self, **kwargs):
        context = super(DockerRegistryUpdateView, self).get_context_data(**kwargs)
        context['is_add'] = False
        return context

class DockerRegistryDeleteView(LoginRequiredMixin, JSONResponseMixin,
                     AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        ids = request.GET.get('id', '')
        if ids != "":
            list_id = ids.split(',')
            for id in list_id:
                old_data = []
                pl = Docker_Registry.objects.filter(id=id)

            Docker_Registry.objects.filter(pk__in=map(int, ids.split(','))).delete()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})