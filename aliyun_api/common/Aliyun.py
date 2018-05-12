# -*- coding: utf-8 -*-
# @Time    : 2018/3/26 14:23
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : Slb.py
# @Software: PyCharm
from hashlib import sha1
import hmac
import base64
import datetime
import hashlib
import uuid
import requests
import json
from urllib.request import quote
from urllib import parse

class Aliyun(object):

    '''
        经测试适合阿里云的SLB与ECS api 接口请求，其它接口还未测试
        apiParameter 参数为一个字典， 对应接口api参数, 通过传递参数能返回请求接口的url
        请求参数文档规范：https://help.aliyun.com/document_detail/27566.html
    '''

    def __init__(self, apiParameter):
        self.parameter = apiParameter

    '''
    定义公共参数 commonParameter 参数为一个字典。
    '''
    def getCommonParameter(self, commonParameter):
        if isinstance(commonParameter, dict):
            return commonParameter
        else:
            return {"error": "it is not a dict"}


    def percentEncode(self, str):
        res = quote(bytes(str, encoding = "utf8"), '')
        res = res.replace('+', '%20')
        res = res.replace('*', '%2A')
        res = res.replace('%7E', '~')
        return res

    # 所有参数传递完成后，再生成签名
    def getSignnature(self, keySecret):
        D = self.parameter
        sortedD = sorted(D.items(), key=lambda x: x[0])
        canstring = ''
        for k, v in sortedD:
            canstring += '&' + self.percentEncode(k) + '=' + self.percentEncode(v)
        stringToSign = 'GET&%2F&' + self.percentEncode(canstring[1:])
        access_key_secret = keySecret
        h = hmac.new(bytes(str(access_key_secret + "&"), encoding="utf-8"), stringToSign.encode("utf-8"), sha1)
        signature = base64.encodestring(h.digest()).strip()
        signature = str(signature, encoding="utf-8")
        return signature

    def getSignatureNonce(self):
        # # 生成当前时间
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        m = hashlib.md5()
        objstr = str(nowTime) + str(uuid.uuid1())
        m.update(objstr.encode('utf-8'))
        uniqueStr = m.hexdigest()
        return uniqueStr

    def getTimestamp(self):
        timeStampUtc = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        return str(timeStampUtc)

    def getUrl(self, commonParameter):
        keySecret = self.getCommonParameter(commonParameter)['keySecret']
        self.parameter['Format'] = self.getCommonParameter(commonParameter)['Format']
        self.parameter['Version'] = self.getCommonParameter(commonParameter)['Version']
        self.parameter['AccessKeyId'] = self.getCommonParameter(commonParameter)['AccessKeyId']
        self.parameter['SignatureMethod'] = self.getCommonParameter(commonParameter)['SignatureMethod']
        self.parameter['SignatureVersion'] = self.getCommonParameter(commonParameter)['SignatureVersion']
        self.parameter['Timestamp'] = self.getTimestamp()
        self.parameter['SignatureNonce'] = self.getSignatureNonce()
        self.parameter['Signature'] = self.getSignnature(keySecret)
        url = self.getCommonParameter(commonParameter)['url'] + '?' + parse.urlencode(self.parameter)
        return url

class UrlRequest(Aliyun):

    def __init__(self, apiParameter):
        super(UrlRequest,self).__init__(apiParameter)

    def getResult(self, commonParameter):
        result = {}
        try:
            url = self.getUrl(commonParameter)
            # print("url: ",url)
            ret = requests.get(url)
            if ret.status_code == 200:
                r = ret.json()
                result = json.dumps(r, ensure_ascii=False)
                return result
            else:
                result['CodeStatus'] = ret.status_code
                result['message'] = json.dumps(ret.json(), ensure_ascii=False)
                result['error'] = "请求结果错误"
                return result
        except Exception as e:
            result['CodeStatus'] = 400
            result['error'] = e
            return result