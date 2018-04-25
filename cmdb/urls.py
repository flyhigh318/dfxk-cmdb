from django.conf.urls import include, url
from cmdb.views import *


urlpatterns = [

    # 云账号管理
    url(r'^yun_account/', include([
        url(r'^$', YunAccountView.as_view(), name='yun_account_list'),
        url(r'^yun_account_add/', YunAccountCreateView.as_view(), name='yun_account_add'),
        url(r'^(?P<pk>\d+)/yun_account_edit/', YunAccountUpdateView.as_view(), name='yun_account_edit'),
        url(r'^delete_entity/', YunAccountDeleteView.as_view(), name='yun_account_delete'),
    ])),

    # Ak管理
    url(r'^keys/', include([
        url(r'^$', KeysView.as_view(), name='keys_list'),
        url(r'^keys_add/', KeysCreateView.as_view(), name='keys_add'),
        url(r'^(?P<pk>\d+)/keys_edit/', KeysUpdateView.as_view(), name='keys_edit'),
        url(r'^delete_entity/', KeysDeleteView.as_view(), name='keys_delete'),
    ])),

    # 产品线
    url(r'^product_line/', include([
        url(r'^$', ProductLineView.as_view(), name='product_line_list'),
        url(r'^product_line_add/', ProductLineCreateView.as_view(), name='product_line_add'),
        url(r'^(?P<pk>\d+)/product_line_edit/', ProductLineUpdateView.as_view(), name='product_line_edit'),
        url(r'^delete_entity/', ProductLineDeleteView.as_view(), name='product_line_delete'),
    ])),

    # 项目
    url(r'^project/', include([
        url(r'^$', ProjectView.as_view(), name='project_list'),
        url(r'^project_add/', ProjectCreateView.as_view(), name='project_add'),
        url(r'^(?P<pk>\d+)/project_edit/', ProjectUpdateView.as_view(), name='project_edit'),
        url(r'^delete_entity/', ProjectDeleteView.as_view(), name='project_delete'),
    ])),

    # 资产
    url(r'^asset/', include([
        url(r'^$', AssetView.as_view(), name='asset_list'),
        url(r'^asset_add/', AssetCreateView.as_view(), name='asset_add'),
        url(r'^(?P<pk>\d+)/asset_edit/', AssetUpdateView.as_view(), name='asset_edit'),
        url(r'^delete_entity/', AssetDeleteView.as_view(), name='asset_delete'),
        url(r'^asset_sync/', AssetSyncView.as_view(), name='asset_sync'),
    ])),

    # 密码表
    url(r'^password/', include([
        url(r'^$', PasswordView.as_view(), name='password_list'),
        url(r'^password_add/', PasswordCreateView.as_view(), name='password_add'),
        url(r'^(?P<pk>\d+)/password_edit/', PasswordUpdateView.as_view(), name='password_edit'),
        url(r'^delete_entity/', PasswordDeleteView.as_view(), name='password_delete'),
    ])),

    # 密码表
    url(r'^website/', include([
        url(r'^$', WebsiteView.as_view(), name='website_list'),
        url(r'^website_add/', WebsiteCreateView.as_view(), name='website_add'),
        url(r'^(?P<pk>\d+)/website_edit/', WebsiteUpdateView.as_view(), name='website_edit'),
        url(r'^delete_entity/', WebsiteDeleteView.as_view(), name='website_delete'),
    ])),

]
