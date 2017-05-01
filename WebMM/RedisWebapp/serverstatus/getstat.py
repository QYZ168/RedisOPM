#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

class gsta(object):

    def getmemory(self):
        a = os.popen('free')
        m = a.read().split()
        d = {m[0]:m[7],m[1]:m[8],m[2]:m[9],'buff':m[11]}
        d['buff'] = round(int(d['buff']) * 100 / int(d['total']),1)
        d['free'] = round(int(d['free']) * 100 / int(d['total']),1)
        d['used'] = round(int(d['used']) * 100 / int(d['total']),1)
        return d
