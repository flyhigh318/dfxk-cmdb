# -*- coding: utf-8 -*-
# @Time    : 2018/4/25 9:26
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : Parameter.py
# @Software: PyCharm

from cmdb.models.Keys import Key

class CommonParameter(object):
    '''
            经测试适合阿里云的SLB与ECS api 接口请求，其它接口还未测试
            阿里云的api接口参数请求，分为2部份，一部分是api，另一部份是公共的参数为一个字典，
            这个类返回公共接口请求参数。
            请求参数文档规范：https://help.aliyun.com/document_detail/27566.html
    '''

    def __init__(self, account):
        self.account = account


    def set_commmon_parameter(self):
        dd = Key.objects.filter(account__name=self.account)
        AccessKeyId = ''
        keySecret = ''
        for obj in dd:
            if obj:
                AccessKeyId = obj.access_key
                keySecret = obj.key_secret
                break
        else:
            ret = {}
            ret['error'] = "there is no accessKeyId and keySecret"
            ret['code'] = 401
            return ret
        parameter = {
            'Format': 'JSON',
            'Version': '2014-05-26',
            'AccessKeyId': AccessKeyId,
            'SignatureMethod': 'HMAC-SHA1',
            'SignatureVersion': '1.0',
            'keySecret': keySecret,
            'url': ''
        }
        return parameter


    def get_vps_parameter(self):
        parameter = self.set_commmon_parameter()
        parameter['url'] = 'https://ecs.aliyuncs.com/'
        parameter['Version'] = '2014-05-26'
        return parameter

    def get_slb_parameter(self):
        parameter = self.set_commmon_parameter()
        parameter['url'] = 'http://slb.aliyuncs.com/'
        parameter['Version'] = '2014-05-15'
        return parameter

    def get_dns_parameter(self):
        parameter = self.set_commmon_parameter()
        parameter['url'] = 'http://alidns.aliyuncs.com'
        parameter['Version'] = '2015-01-09'
        return parameter