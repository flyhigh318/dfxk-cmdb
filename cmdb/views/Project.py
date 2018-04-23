## -*- coding: utf-8 -*-
# @Time    : 2018/3/28 15:50
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : __init__.py
# @Software: PyCharm

from braces.views import *
from django.contrib.auth.mixins import *
from django.urls import *
from django.views.generic import *

from cmdb.forms.ProjectForm import ProjectForm, ProjectListFilterForm
from cmdb.models.Project import Project
from cobra_main.settings import PER_PAGE
from django.db.models import Q

listview_lazy_url = 'cmdb:project_list'
listview_template = 'cmdb/project_list.html'
formview_template = 'cmdb/project_form.html'

class ProjectView(LoginRequiredMixin, OrderableListMixin, ListView):
    model = Project
    paginate_by = PER_PAGE
    template_name = listview_template
    context_object_name = 'result_list'
    orderable_columns_default = 'id'
    orderable_columns = ['name', 'create_time', 'update_time']

    def get_queryset(self):
        result_list = Project.objects.all()
        search = self.request.GET.get('name')
        order_by = self.request.GET.get('order_by')
        ordering = self.request.GET.get('ordering')

        if search:
            result_list = Project.objects.filter(Q(name__icontains=search)|
                                                 Q(asset__intral_ip__icontains=search)|
                                                 Q(website__icontains=search)|
                                                 Q(domain__icontains=search)|
                                                 Q(comment__icontains=search))
        if order_by:
            if ordering == 'desc':
                result_list = result_list.order_by('-' + order_by)
            else:
                result_list = result_list.order_by(order_by)

        return result_list

    def get_context_data(self, **kwargs):
        context = super(ProjectView, self).get_context_data(**kwargs)
        context['order_by'] = self.request.GET.get('order_by', '')
        context['ordering'] = self.request.GET.get('ordering', 'asc')
        context['filter_form'] = ProjectListFilterForm(self.request.GET)
        return context

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    paginate_by = PER_PAGE
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)

    def get_success_url(self):
        return super(ProjectCreateView, self).get_success_url()

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = formview_template
    success_url = reverse_lazy(listview_lazy_url)
    context_object_name = 'entity'

    def get_context_data(self, **kwargs):
        context = super(ProjectUpdateView, self).get_context_data(**kwargs)
        context['is_add'] = False
        return context



class ProjectDeleteView(LoginRequiredMixin, JSONResponseMixin,
                     AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        ids = request.GET.get('id', '')
        if ids != "":
            list_id = ids.split(',')
            for id in list_id:
                old_data = []
                pl = Project.objects.filter(id=id)

            Project.objects.filter(pk__in=map(int, ids.split(','))).delete()
            return self.render_json_response({"success": True})
        else:
            return self.render_json_response({"success": False})