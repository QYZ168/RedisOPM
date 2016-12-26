# coding=utf-8
from django.shortcuts import render,render_to_response,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .vfication import *

import hashlib

setuser = vf()

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
    #username = request.COOKIES.get('username','')
    if 'username' in request.session:
        if 'time' in request.session:
            time = request.session.get('time')
            username = request.session.get('username')
            return render(request,'RedisWebapp/index.html',{'username':username,'time':time})
        else:
            username = request.session.get('username')
            return render(request,'RedisWebapp/index.html',{'username':username})
    return render(request,'RedisWebapp/login.html')

#def logout(request):
#    if request.session['time']:
#        del request.session['time']
    #response = HttpResponse('logout')
    #response.delete_cookie('username')
    #return response
#    del request.session['username']
#    return render(request,'RedisWebapp/login.html')
