#!/usr/bin/env python
# -*- coding:utf-8 -*-

import MySQLdb

class cmysql(object):

    def cdb(self):
        db = MySQLdb.connect('172.17.0.5','root','root','REDISWEB')
        return db

    def inmysql(self,hostip,hostname):
        db = self.cdb()
        cursor = db.cursor()
        status = True
        try:
            cursor.execute("INSERT INTO hostdb(hostaddress,hostname) VALUES('%s','%s')"%(hostip,hostname))
            db.commit()
        except: 
            db.rollback()
            status = False
        db.close()
        return status

    def selmysql(self,hostip):
        db = self.cdb()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT * FROM hostdb WHERE hostaddress = '%s'"%(hostip))
            results = cursor.fetchall()
        except:
            results = 'no'
        db.close()
        return results

    def inidletdb(self,time,value):
        db = self.cdb()
        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO idletdb(time,numvalue) VALUES('%s','%s')"%(time,value))
            db.commit()
        except:
            db.rollback()
        db.close()

    def selidletdb(self):
        db = self.cdb()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT * FROM idletdb")
            #cursor.execute("SELECT * FROM hostdb")
            results = dict(cursor.fetchall())
        except:
            results = 'no'
        db.close()
        return results

    def delidletdb(self,time):
        db = self.cdb()
        cursor = db.cursor()
        try:
            cursor.execute("DELETE FROM idletdb WHERE time = %s"%(time))
            db.commit()
        except:
            db.rollback()
        db.close()

#a = cmysql()
#print(a.selidletdb())
