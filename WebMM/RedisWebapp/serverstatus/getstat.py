#!/usr/bin/env python
# -*- coding:utf-8 -*-

from ..mysqlcache.conmysql import *
import os
import datetime

cmy = cmysql()

class gsta(object):

    def getmemory(self):
        a = os.popen('free')
        m = a.read().split()
        d = {m[0]:m[7],m[1]:m[8],m[2]:m[9],'buff':m[11]}
        d['buff'] = round(int(d['buff']) * 100 / int(d['total']),1)
        d['free'] = round(int(d['free']) * 100 / int(d['total']),1)
        d['used'] = round(int(d['used']) * 100 / int(d['total']),1)
        return d

    def getidle(self):
        idle = os.popen('vmstat')
        idledata = idle.read().split()
        idledata = idledata[-3]
        time = datetime.datetime.now().strftime("%H")
        results = cmy.selidletdb()
        if time in results:
            cmy.delidletdb(time)
        cmy.inidletdb(time,idledata)

if __name__=='__main__':
    b = gsta()
    b.getidle()
