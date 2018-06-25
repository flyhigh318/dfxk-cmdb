# -*- coding: utf-8 -*-
# @Time    : 2018/6/5 10:37
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : docker.py
# @Software: PyCharm

import requests
from urllib.parse import urlparse
import os

class Registry(object):

    def __init__(self, **kwargs):
        self.url = kwargs['url']
        self.user = kwargs['user']
        self.password = kwargs['password']
        self.headers = kwargs['headers']

    def get_registry(self, url):
        result = {}
        try:
            # url = self.url + "v2/_catalog"
            ret = requests.get(url, data=None, headers=self.headers)
            result['info'] = ret.json()
        except Exception as e:
            result['code'] = 400
            result['error'] = str(e)
        finally:
            return result

    def get_tags(self):
        result = []
        info = self.get_registry(url=self.url+"v2/_catalog")
        # print(info)
        registry = info['info']['repositories']
        o = urlparse(self.url)
        for reg in registry:
            url = self.url + "v2/" + reg + "/tags/list"
            info = self.get_registry(url)
            tags = info['info']
            cmds = []
            for tag in tags['tags']:
                cmds.append("docker pull " + str(o.hostname) + "/"+ tags['name']+ ":" +tag)
                tags['cmds'] = cmds
            result.append(tags)
            # print(tags)
        return result











