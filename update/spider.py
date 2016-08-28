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
sys.path.append("..")
from record import Category


class Spider:
    google = None
    baidu = None
    bing = None
    yahoo = None
    db_dir = None
    zh_re = None
    shcool = None
    subject = None
    url = None
    count = None
    deep_mind = None
    category = ''
    category_obj = None

    proxies = {
        "http": "http://127.0.0.1:8087",
        "https": "http://127.0.0.1:8087",
    }

    proxies2 = {
        "http": "http://127.0.0.1:8787",
        "https": "http://127.0.0.1:8787",
    }


    def __init__(self):
        self.google = "https://www.google.com.hk/?gws_rd=cr,ssl#safe=strict&q="
        self.baidu = "http://www.baidu.com/s?word="
        self.bing = "http://cn.bing.com/search?q=a+b&go=Submit&qs=n&form=QBLH&pq="
        self.yahoo = "https://search.yahoo.com/search;_ylt=Atkyc2y9pQQo09zbTUWM4CWbvZx4?p="
        self.db_dir = os.path.abspath('.') + "/../" + "db/"
        self.zh_re=re.compile(u"[\u4e00-\u9fa5]+")
        self.school = None
        self.subject = None
        self.url = None
        self.count = 0
        self.deep_mind = False
        self.category_obj = Category()

    def doWork(self):
        return
      
    def requestWithProxy(self, url):
        return requests.get(url, proxies=self.proxies, verify=False)

    def requestWithProxy2(self, url):
        return requests.get(url, proxies=self.proxies2, verify=False)

    def format_subject(self, subject):
        match_list = []
        for (k, v) in subject_dict.items():
            if subject.find('/') != -1 and subject.lower()[0:subject.find('/')].strip().find(k.lower()) != -1:
                match_list.append(k)
            elif subject.find('/') == -1 and subject.lower().strip().find(k.lower()) != -1:
                match_list.append(k)
        result = subject
        if len(match_list) > 1:
            max_len = 0
            for key in match_list:
                if key.lower() == subject[0: subject.find(' ')].lower().strip():
                    result = subject_dict[key]
                    break

                if len(key) > max_len:
                    max_len = len(key)
                    result = subject_dict[key]
        elif len(match_list) == 1:
            #print subject_dict[match_list[0]]
            result = subject_dict[match_list[0]]
        #print subject
        if result != subject and subject.find('/') != -1:
            last_index = 0
            while subject.find('/', last_index + 1) != -1:
                last_index = subject.find('/', last_index + 1)

            return result + subject[subject.find('/') : last_index + 1]
        elif result != subject:
            return result + "/"
        else:
            if subject.strip()[len(subject) - 1 : ] != '/':
                return subject + "/"
            else:
                return subject
    
    def need_update_subject(self, subject):
        subject_converted = self.format_subject(subject)
        if subject_converted[len(subject_converted) - 1 : ] == '/':
            subject_converted = subject_converted[0 : len(subject_converted) - 1]
        for item in need_update_subject_list:
            if subject_converted.find(item) != -1:
                return True
        print subject + " not config in all_subject.py, ignore it"
        return False
    
    def replace_sp_char(self, text):
        while text.find('/') != -1:
            text = text[text.find('/') + 1 : ]

        return text.replace(",","").replace("&","").replace(":","").replace("-"," ").replace("  "," ").replace(" ","-").lower()
    
    def get_file_name(self, subject, school):
        dir_name = self.format_subject(subject)
        return self.db_dir + dir_name + self.replace_sp_char(subject) + "-" + school + time.strftime("%Y")
    
    def create_dir_by_file_name(self, file_name):
        if os.path.exists(file_name) == False:
            index = 0
            for i in range(0, len(file_name)):
                if file_name[i] == "/":
                    index = i
            if index > 0:
                if os.path.exists(file_name[0:index]) == False:
                    print "creating " + file_name[0:index] + " dir"
                    os.makedirs(file_name[0:index])
        
    def open_db(self, file_name, append=False):
        self.create_dir_by_file_name(file_name)
        flag = 'w'
        if append:
            flag = 'a'
        try:
            f = open(file_name, flag)
        except IOError, err:
            print str(err)
        return f
    
    def do_upgrade_db(self, file_name):
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
    def cancel_upgrade(self, file_name):
        if os.path.exists(file_name + ".tmp"):
            os.remove(file_name + ".tmp")
    
    def close_db(self, f):
        f.close()
    
    
    def write_db(self, f, course_num, course_name, url, describe=""):
        #if url == "":
        #    url = self.google + course_num + " " + course_name
        if self.category != '' and describe.find('category:') == -1:
            describe += ' category:' + self.category 

        f.write(course_num.strip() + " | " + course_name.replace("|","") + " | " + url  + " | " + describe + "\n")
    
    def get_storage_format(self,course_num, course_name, url, describe=""):
        if url == "":
            url = self.google + course_num + " " + course_name    
        return course_num.strip() + " | " + course_name.replace("|","") + " | " + url  + " | " + describe

    def countFileLineNum(self, file_name):
        if os.path.exists(file_name):
            line_count = len(open(file_name,'rU').readlines())
            return line_count
        return 0
    
    def truncateUrlData(self, dir_name):
        print "truncateUrlData ...."
        self.create_dir_by_file_name(get_url_file_name(dir_name))
        f = open(get_url_file_name(dir_name), "w+")
        f.truncate()
        f.close
    
    
    def delZh(self, text):
        if isinstance(text, unicode):
            list_u = self.zh_re.findall(text)
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

    def getKeyValue(self, option):
        value_pos = option.find("value=") + 7
        return option[value_pos : option.find('"', value_pos)], option[option.find(">") + 1 : option.find("</", 2)].replace("&amp;", "").replace("\n", "").strip()
    
