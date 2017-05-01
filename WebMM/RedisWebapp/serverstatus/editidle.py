#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
sys.path.append('/home/django/webmm/RedisOPM/WebMM/RedisWebapp/')
  
from mysqlcache.conmysql import *
import os
import datetime
 
cmy = cmysql()

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
    getidle()
