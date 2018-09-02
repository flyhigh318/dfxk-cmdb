# -*- coding: utf-8 -*-
# @Time    : 18-4-6 下午7:45
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : Asset.py
# @Software: dfxk-cmdb
import paramiko
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
import json
from cmdb.models.Password import Password  as KeyPass

from cmdb.models import Assets

import pymysql
from sshtunnel import SSHTunnelForwarder
listview_template = 'cmdb/zhima_query_list.html'

class ZhimaCreditView(View):

    template_name = listview_template

    def get(self, request):

        beginTime = request.GET.get('beginTime')
        endTime = request.GET.get('endTime')
        print(beginTime, endTime)

        data = []
        ret = self.ssh_connect_and_read_db(beginTime, endTime)
        for i in ret:
            if  not isinstance(i[0], str):
                continue
            a = {}
            a['date'] = i[0]
            a['amountQueryZhima'] = i[1]
            data.append(a)
        # print("data: %s" % data)
        return render(request, 'cmdb/zhima_query_list.html', {'data': data})

    def post(self, request):

        beginTime = request.POST['beginTime']
        endTime = request.POST['endTime']
        print(beginTime, endTime)

        data = []
        ret = self.ssh_connect_and_read_db()
        for i in ret:
            if  not isinstance(i[0], str):
                continue
            a = {}
            a['date'] = i[0]
            a['amountQueryZhima'] = i[1]
            data.append(a)
        # print("data: %s" % data)
        return render(request, 'cmdb/zhima_query_list.html', {'data': data})


    def ssh_connect_and_read_db(self, *args):
        with SSHTunnelForwarder(
                ('172.18.31.48', 22),  # B机器的配置--跳板机
                ssh_username="root",  # B机器的配置--跳板机账号
                ssh_password="fpxOuSFvhIwznZEz7d96pUA7",  # B机器的配置--跳板机账户密码
                remote_bind_address=('rm-wz9b239e8zbuwid66to.mysql.rds.aliyuncs.com', 3306)) as server:  # A机器的配置-MySQL服务器

            conn =  pymysql.connect(host='127.0.0.1',  # 此处必须是必须是127.0.0.1，代表C机器
                                   port=server.local_bind_port,
                                   user='mroot',  # A机器的配置-MySQL服务器账户
                                   passwd='5UE1pFFcRyfH13NejBcMzA',  # A机器的配置-MySQL服务器密码c
                                   charset='utf8', # 和数据库字符编码集合，保持一致，这样能够解决读出数据的中文乱码问题
                                   db='dfxk_history' # 可以限定，只访问特定的数据库,否则需要在mysql的查询或者操作语句中，指定好表名
                                   )
            # print conn
            # 打开数据库
            cursor = conn.cursor()
            # 执行sql操作
            try:
                # test1
                cursor.execute("SELECT VERSION()")
                data = cursor.fetchone()
                print("Database version : %s " % data)
                # test2
                test_sql = '''SELECT
                              	DATE_FORMAT(send_mail_date, '%Y-%m-%d') query_date,
                              	COUNT(send_type) '查询芝麻数(次)'
                              FROM
                              	`t_dm_sendmail_zhima_history`
                              WHERE
                              	send_mail_date BETWEEN \'{0}\'
                              AND    
                                      \'{1}\'
                              AND    
                                      send_type is not null
                              GROUP BY 
                                      query_date
                              ORDER BY 
                                       send_mail_date
                              ;
                            '''.format(
#                    '2018-08-15  00:00:00', '2018-08-29  23:59:59'
                      args[0], args[1]
                )
                cursor.execute(test_sql)
                data = cursor.fetchall()
                print(data)
                data_tupple = data
            except Exception as e:
                data_tupple = str(e)
                print(e)
            # 关闭数据库
            conn.close()
            return data_tupple


