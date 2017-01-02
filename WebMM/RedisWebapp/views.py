# coding=utf-8
from django.shortcuts import render,render_to_response,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .rediscache.vfication import *
from .mysqlcache.conmysql import *
from .serverstatus.getstat import *

import hashlib
import datetime

setuser = vf()
cmy = cmysql()

def regist(request):
    error = False
    if request.method == 'POST':
#        if request.POST['username'] and request.POST['password'] and request.POST['name']:
        if request.POST['password'] != request.POST['password_1']:
            data = 'The two passwords are inconsistent!'
        else:
            username = request.POST['username']
            password = request.POST['password']
            name = request.POST['name']
            val = setuser.get_cache(username)
            if type(val) == str:
                data = 'Username already exists!'
            else:
                if val['name'] == name.encode('utf-8'):
                    data = 'Name already exists!'
                else:
                    pwd = hashlib.sha1(password.encode('utf-8')).hexdigest()
                    setuser.set_cache(username,name,pwd)
                    return render(request,'RedisWebapp/login.html')
        error = True
        return render(request,'RedisWebapp/sign.html',{'error':error,'data':data})
    return render(request,'RedisWebapp/sign.html')

def login(request):
    error = False
    if 'username' in request.session:
        if 'time' in request.session:
            del request.session['time']
        del request.session['username']
    if request.method == 'POST':
        if 'username' in request.POST and 'password' in request.POST:
#        if request.POST['username'] and request.POST['password']:
                    #response = HttpResponseRedirect('index')
                    #response.set_cookie("username",'admin',3600)
                    #return response
            username = request.POST['username']
            password = request.POST['password']
            val = setuser.get_cache(username)
            if type(val) == dict:
#                return render(request,'RedisWebapp/login.html') 
#            else:
                pwd = hashlib.sha1(password.encode('utf-8')).hexdigest()
                if pwd.encode('utf-8') == val['pwd']:
                    time = val.get('time','')
                    if time == '':
                        request.session['username'] = val['name'].decode('utf-8')
                    else:
                        request.session['username'] = val['name'].decode('utf-8')
                        request.session['time'] = val['time'].decode('utf-8')
                    return HttpResponseRedirect('index')
        error = True
        return render(request,'RedisWebapp/login.html',{'error':error})
#    else:
    return render(request,'RedisWebapp/login.html',{'error':error})

def index(request):
    b = gsta()
    d = b.getmemory()
    idle = cmy.selidletdb()
    tem = int(datetime.datetime.now().strftime("%H"))
    sj = []
    val = []
    for i in range(24):
        if tem > 23:
            tem = 0
        sj.append(str(tem))
        try:
            val.append(int(idle[str(tem)]))
        except:
            val.append(0)
        tem += 1
    #username = request.COOKIES.get('username','')
    if 'username' in request.session:
        if 'time' in request.session:
            time = request.session.get('time')
            username = request.session.get('username')
            return render(request,'RedisWebapp/index.html',{'username':username,'time':time,'d':d,'sj':sj,'val':val})
            #return render(request,'RedisWebapp/index.html',locals())
        else:
            username = request.session.get('username')
            return render(request,'RedisWebapp/index.html',{'username':username,'d':d,'sj':sj,'val':val})
            #return render(request,'RedisWebapp/index.html',locals())
    return render(request,'RedisWebapp/login.html')
#    return HttpResponseRedirect('login.html')

def inset(request):
    error = False
    error_1 = False
    if 'username' in request.session:
        if request.method == 'POST':
            if 'startipaddress' in request.POST and 'endipaddress' in request.POST:
                startip = request.POST['startipaddress']
                endip = request.POST['endipaddress']
                hostname = request.POST['hostname']
                snum = int(startip[6:])
                enum = int(endip[6:])
                gip = startip[:-1]
                gsql = []
                for i in range(snum,enum+1):
                    fip = ''
                    fip = gip + str(i)
                    results = cmy.selmysql(fip)
                    if results:
                        gsql.append(fip)
                    else:
                        data = cmy.inmysql(fip,hostname)
                error_1 = True
            elif 'ipaddress' in request.POST:
                hostname = request.POST['hostname']
                ipaddress = request.POST['ipaddress']
                results = cmy.selmysql(ipaddress)
                if not results:
                    error_1 = cmy.inmysql(ipaddress,hostname)
                else:
                    error = True
        return render(request,'RedisWebapp/inset.html',{'error':error,'error_1':error_1})
    return render(request,'RedisWebapp/login.html')

#def logout(request):
#    if request.session['time']:
#        del request.session['time']
    #response = HttpResponse('logout')
    #response.delete_cookie('username')
    #return response
#    del request.session['username']
#    return render(request,'RedisWebapp/login.html')

