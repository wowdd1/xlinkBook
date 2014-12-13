#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.09

import MySQLdb
import os
import redis
#"""
conn = None
cur = None
r = None
def open_db():
    global conn, cur, r
    try:
        conn=MySQLdb.connect(host='localhost',user='root',passwd='zd19861111',port=3306)
        cur=conn.cursor()
        #cur.execute('drop database course if exists course')
        #conn.commit()
        cur.execute('create database if not exists course')
        conn.select_db('course')
        #conn.commit()
        r = redis.Redis('localhost',  port=6379, db=0)
        return cur
    except MySQLdb.Error,e:
         print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def exec_sql(sql):
    #print sql
    try:
        cur.execute(sql)
        conn.commit()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def exec_sql_with_value(sql, value):
    #print sql
    #print value
    try:
        cur.executemany(sql, value)
        conn.commit()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])


def close_db():
    try:
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])


def import_data_to_db(db_path):
    if os.path.exists(db_path):
        cur_list = os.listdir(db_path)
        for item in cur_list:
            #print item
            if item == ".svn" or item == ".git" or item == ".DS_Store":
                continue

            full_path = os.path.join(db_path, item)
            if os.path.isfile(full_path):
                item = item.replace("-", "_")
                f = open(full_path, "rU")
                try:
                    exec_sql('create table ' + item + ' (id varchar(80), title varchar(200), url varchar(200))')
                except MySQLdb.Error,e:
                    print "Mysql Error %d: %s" % (e.args[0], e.args[1])
                for line in f.readlines():
                    values=[]
                    course_number = line[0 : line.find("|")].strip()
                    course_title = line[line.find("|") + 1 : line.find("|", line.find("|") + 1)].strip()
                    url = line[line.find("|",line.find("|") + 1) + 1 : ]
                    #if r.exists(item) == True:
                    #    print item + "already exists in redis"
                    #else:
                    r.lpush(item, line)
                    values.append((course_number, course_title, url))
                    try:
                        exec_sql_with_value('insert into ' + item + ' values (%s, %s, %s)', values)
                    except MySQLdb.Error,e:
                        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
                f.close()
            else:
                import_data_to_db(full_path) 

open_db()
#exec_sql('create table test_x(id int,info varchar(20))')
#exec_sql('create table test_a(id int,info varchar(20))')
#exec_sql('create table test_c(id int,info varchar(20))')

#exec_sql('drop database course')
import_data_to_db(os.getcwd() + '/../db/')

close_db()


print "print redis"
#"""
"""
r = redis.Redis('localhost',  port=6379, db=0)
for key in r.keys():
    r.delete(key)
    #print r.get(key)
"""

#for key in r.keys():
#    print r.get(key)
