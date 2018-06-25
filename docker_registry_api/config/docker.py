# -*- coding: utf-8 -*-
# @Time    : 2018/6/5 9:31
# @Author  : Abner
# @Email   : tangrongwen@dfxkdata.com
# @File    : docker.py
# @Software: PyCharm

DockerRegistryInfo = {
    "url": "https://registry.docker.dfxkdata.com/",
    "host": '192.168.103.103',
    "user": "admin",
    "password": "admin@dfxkdata.com",
    "config": {
         "auths": {
                 "registry.docker.dfxkdata.com": {
                     "auth": "YWRtaW46YWRtaW5AZGZ4a2RhdGEuY29t"
                 }
         },
         "HttpHeaders": {
                 "User-Agent": "Docker-Client/17.12.0-ce (linux)"
         }
    }
}
