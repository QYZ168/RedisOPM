from .sqlfile import conredis
import datetime
import redis
import hashlib

class vf(conredis):

    def set_cache(self,key,name,password):
        try:
            time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.redis_c().hset(key,'name',name)
            self.redis_c().hset(key,'password',password)
            self.redis_c().hset(key,'login-count',0)
            self.redis_c().hset(key,'time',time)
        except Exception as e:
            with open('log','a') as f:
                f.write(e)

    def get_cache(self,key):
        if self.redis_c().exists(key):
            timer = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            name,passwd,time,login_count = self.redis_c().hmget(key,'name','password','time','login-count')
            if login_count == 0:
                idict = {'name':name,'pwd':passwd}
            else:
                idict = {'name':name,'pwd':passwd,'time':time}
            self.redis_c().hincrby(key,'login-count',1)
            self.redis_c().hset(key,'time',timer)
            return idict
        else:
            return 'username or password error!'

#    def dsd(self):
#        print('sd')
#        if self.redis_c().exists('admin'):
#            return print('1')
#        else:
#            return print('0')

#lk = vf()
#lk.dsd()
