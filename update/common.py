#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.09


import requests
import json
from bs4 import BeautifulSoup;
import os,sys
import time
import re
reload(sys)
sys.setdefaultencoding("utf-8")

google = "https://www.google.com.hk/?gws_rd=cr,ssl#safe=strict&q="
baidu = "http://www.baidu.com/s?word="
bing = "http://cn.bing.com/search?q=a+b&go=Submit&qs=n&form=QBLH&pq="
yahoo = "https://search.yahoo.com/search;_ylt=Atkyc2y9pQQo09zbTUWM4CWbvZx4?p="
db_dir = os.path.abspath('.') + "/../" + "db/"
local_url_file = db_dir + ".urls"
zh_re=re.compile(u"[\u4e00-\u9fa5]+")

def get_file_name(arg):
    return db_dir + arg + time.strftime("%Y")

def open_url_file(arg):
    return open(get_url_file_name(arg), "a")

def get_url_file_name(arg):
    return db_dir + arg + ".urls"

def close_url_file(f):
    f.close()


def create_dir_by_file_name(file_name):
    if os.path.exists(file_name) == False:
        index = 0
        for i in range(0, len(file_name)):
            if file_name[i] == "/":
                index = i
        if index > 0:
            if os.path.exists(file_name[0:index]) == False:
                print "creating " + file_name[0:index] + " dir"
                os.makedirs(file_name[0:index])
    
def open_db(file_name):
    create_dir_by_file_name(file_name)

    try:
        f = open(file_name, "a")
    except IOError, err:
        print str(err)
    return f

def do_upgrade_db(file_name):
    tmp_file = file_name + ".tmp"
    if os.path.exists(file_name) and os.path.exists(tmp_file):
        print "upgrading..."
        #os.system("diff -y --suppress-common-lines -EbwBi " + file_name + " " + file_name + ".tmp " + "| colordiff")
        print "remove " + file_name[file_name.find("db"):]
        os.remove(file_name)
        print "rename " + file_name[file_name.find("db"):] + ".tmp"
        os.rename(tmp_file, file_name)
        print "upgrade done"
    elif os.path.exists(tmp_file):
        print "upgrading..."
        print "rename " + file_name[file_name.find("db"):] + ".tmp"
        os.rename(tmp_file, file_name)
        print "upgrade done"
    else:
        print "upgrade error"
def cancel_upgrade(file_name):
    if os.path.exists(file_name + ".tmp"):
        os.remove(file_name + ".tmp")

def close_db(f):
    f.close()


def write_db(f, data):
    f.write(data +  "\n")

def write_db_url(url_f, course_num, url, course_name):
    if url == "":
        url = google + course_num + " " + course_name

    url_f.write(course_num + " | " + url.strip() + " | " + course_name +  "\n")


def countFileLineNum(file_name):
    if os.path.exists(file_name):
        line_count = len(open(file_name,'rU').readlines())
        return line_count
    return 0

def truncateUrlData(dir_name):
    print "truncateUrlData ...."
    create_dir_by_file_name(get_url_file_name(dir_name))
    f = open(get_url_file_name(dir_name), "w+")
    f.truncate()
    f.close


def delZh(text):
    if isinstance(text, unicode):
        list_u = zh_re.findall(text)
        if len(list_u) > 0 :
            last_ele = list_u[len(list_u) - 1]
            last_pos = text.find(last_ele)
            first_pos = text.find(list_u[0])
            title = ""
            if first_pos == 0:
                title = text[last_pos + len(last_ele):]
            else:
                title = text[0:first_pos] + text[last_pos + len(last_ele):].strip()

            if title.find("|") != -1:
                title = title.replace("|", "").strip()
            return title
    return text

