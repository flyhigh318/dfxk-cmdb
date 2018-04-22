# -*- coding: utf-8 -*-
# Author: Maksim.G
import json

from django.http import HttpResponse
from cmdb.common import sqlquery_dict, __default
from cmdb.models import ProductLine, Module, App


def import_product(product):
    for p in product:
        print(p)
        p_obj = ProductLine.objects.filter(name=p['prod_code'])
        if len(p_obj) == 0:
            p_obj = ProductLine(name=p['prod_code'],state=p['prod_code'],create_time=p['createtime'],pro_abbreviation='',domain='',status=1)
            p_obj.save()
        else:
            p_obj=p_obj[0]
            p_obj.name = p['prod_code']
            p_obj.state = p['prod_code']
            # p_obj.create_time = p['createtime']
            p_obj.pro_abbreviation = ''
            p_obj.domain = ''
            p_obj.status = 1
            p_obj.save()

def import_app(app):
    for a in app:
        module_name = a['app_code']
        m_obj = Module.objects.filter(module_name=module_name)
        if len(m_obj) == 0:
            m_obj = Module(module_name=module_name,comment=module_name)
            m_obj.save()
        else:
            m_obj = m_obj[0]
            m_obj.module_name = module_name
            m_obj.comment = module_name
            m_obj.save()

        product_name = a['prod_code']
        p_obj = ProductLine.objects.filter(name=product_name)
        if len(p_obj) == 0:
            p_obj = ProductLine(name=a['prod_code'],state=a['prod_code'],create_time=a['createtime'], pro_abbreviation='',domain='',status=0)
            p_obj.save()
        else:
            p_obj=p_obj[0]
            p_obj.name = a['prod_code']
            p_obj.state = a['prod_code']
            p_obj.pro_abbreviation = ''
            p_obj.domain = 'None'
            p_obj.status = 0
            p_obj.save()

        app_alias = a['prod_code'] + '_' + a['app_code']
        a_obj = App.objects.filter(pk=a['app_id'], alias=app_alias)
        if len(a_obj) == 0:
            a = App(pk=a['app_id'],product_line=p_obj,name=m_obj,alias=app_alias,default_host=a['default_host'], comment=app_alias)
            a.save()

def test_tmp(request):
    pro = sqlquery_dict("select * from t_product;")
    import_product(pro)
    app = sqlquery_dict("SELECT * from t_app as a ,t_product as p WHERE a.prod_code=p.prod_code;;")
    import_app(app)

    return HttpResponse(json.dumps(app, default=__default))

