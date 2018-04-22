from django.conf.urls import include, url

from common import views

urlpatterns = [

    # url(r'bug_list/$', views.BugListView.as_view(), name='bug_list'),
    url(r'^$', views.dashboard, name='dashboard'),
]
