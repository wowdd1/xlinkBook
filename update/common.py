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
from all_subject import subject_dict, need_update_subject_list
reload(sys)
sys.setdefaultencoding("utf-8")

google = "https://www.google.com.hk/?gws_rd=cr,ssl#safe=strict&q="
baidu = "http://www.baidu.com/s?word="
bing = "http://cn.bing.com/search?q=a+b&go=Submit&qs=n&form=QBLH&pq="
yahoo = "https://search.yahoo.com/search;_ylt=Atkyc2y9pQQo09zbTUWM4CWbvZx4?p="
db_dir = os.path.abspath('.') + "/../" + "db/"
local_url_file = db_dir + ".urls"
zh_re=re.compile(u"[\u4e00-\u9fa5]+")


def format_subject(subject):
    match_list = []
    for (k, v) in subject_dict.items():
        if subject.lower().strip().find(k.lower()) != -1:
            match_list.append(k)

    if len(match_list) > 1:
        result = subject
        max_len = 0
        for key in match_list:
            if len(key) > max_len:
                max_len = len(key)
                result = subject_dict[key]
        return result
    elif len(match_list) == 1:
        #print subject_dict[match_list[0]]
        return subject_dict[match_list[0]]
    #print subject 
    return subject

def need_update_subject(subject):
    subject_converted = format_subject(subject)
    for item in need_update_subject_list:
        if subject_converted == item:
            return True
    print subject + " not config in all_subject.py, ignore it"
    return False

def replace_sp_char(text):
    return text.replace(",","").replace("&","").replace(":","").replace("-"," ").replace("  "," ").replace(" ","-").lower()

def get_file_name(subject, school):
    return db_dir + format_subject(subject) + "/" + replace_sp_char(subject) + "-" + school + time.strftime("%Y")

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
        #print "remove " + file_name[file_name.find("db"):]
        os.remove(file_name)
        #print "rename " + file_name[file_name.find("db"):] + ".tmp"
        os.rename(tmp_file, file_name)
        print "upgrade done"
    elif os.path.exists(tmp_file):
        print "upgrading..."
        #print "rename " + file_name[file_name.find("db"):] + ".tmp"
        os.rename(tmp_file, file_name)
        print "upgrade done"
    else:
        print "upgrade error"
def cancel_upgrade(file_name):
    if os.path.exists(file_name + ".tmp"):
        os.remove(file_name + ".tmp")

def close_db(f):
    f.close()


def write_db(f, course_num, course_name, url):
    if url == "":
        url = google + course_num + " " + course_name

    f.write(course_num.strip() + " | " + course_name.replace("|","") + " | " + url  +  "\n")


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

