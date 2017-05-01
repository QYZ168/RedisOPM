#!/usr/bin/env python
# -*- coding:utf-8 -*-

import redis

server = {
    'host':'172.17.0.3',
    'port':6379,
    'database':0,
    'password':'',
}

class conredis(object):

    _host = server.get('host','')
    _port = server.get('port','')
    _database = server.get('database','')
    _password = server.get('pwssword','')

    def redis_c(self):
        redis_ctl = redis.StrictRedis(host=self._host,port=self._port,db=self._database,password=self._password)
        #redis_ctl = 'asdasd'
        return redis_ctl
