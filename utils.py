#!/usr/bin/env python
# -*- coding: utf-8-*-    
#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.08

import os
import sys
import re, mmap
import itertools
import unicodedata
from update.all_subject import default_subject
import requests
import json
import sys
from bs4 import BeautifulSoup;
from record import Record
from record import PriorityRecord
from record import CourseRecord
from record import ReferenceRecord
from record import PaperRecord
from record import ContentRecord
from record import EnginRecord
from record import Tag
import time, datetime
import feedparser
import subprocess
from config import Config
from private_config import PrivateConfig
from extension_manager import ExtensionManager
reload(sys)
sys.setdefaultencoding('utf8')
from record import Tag
from slackclient import SlackClient
import urllib

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from random import choice

from github import Github
import base64
import uuid

regex = re.compile("\033\[[0-9;]*m")
py3k = sys.version_info[0] >= 3
if py3k:
    unicode = str
    basestring = str
    itermap = map
    uni_chr = chr
else:
    itermap = itertools.imap
    uni_chr = unichr

class Utils:    
    cc_map = {
        'black': '30',
        'darkred': '31',
        'darkgreen': '32',
        'brown': '33', #dark yellow  
        'darkblue': '34',
        'darkmagenta': '35',
        'darkcyan': '36',
        'darkwhite': '37',
        'red': '1;31',
        'green': '1;32',
        'yellow': '1;33',
        'blue': '1;34',
        'magenta': '1;35',
        'cyan': '1;36',
        'white': '1;37',
    }
    search_engin_dict = {}
    search_engin_type_engin_dict = {}
    search_engin_type_2_engin_title_dict = {}
    search_engin_type = []
    engin_extension = []
    search_engin_url_dict = {}

    ddg_search_engin_dict = {}
    ddg_search_engin_type = []
    ddg_search_engin_url_dict = {}

    ddg_mode = False

    alexa_dict = {}

    def __init__(self):
        self.loadEngins()
        self.tag = Tag()
        self.suportFrameCache = {}
        self.extensionManager = ExtensionManager()

    def setEnginMode(self, engin):
        if engin.find(':duckduckgo') != -1:
            self.ddg_mode = True 
            return True
        return False

    def getExtensions(self):
        extensions = []
        if os.path.exists(Config.engin_extension_file):
            f = open(Config.engin_extension_file, 'rU')
            for line in f.readlines():
                if line.strip() != '':
                    extensions.append(line.strip())
        return extensions

    def getExtensionCommandArgs(self, rID, rTitle, url, client, module, command, fileName):

        form = {}
        form['check'] = 'false'
        form['rID'] = rID
        form['rTitle'] = rTitle
        form['url'] = url
        form['name'] = module
        form['command'] = command
        form['fileName'] = fileName
        form['originFileName'] = fileName
        form['client'] = client;
        form['divID'] = module + '-div'
        form['objID'] = module + '-div'
        form['column'] = '3'
        form['extension_count'] = '6'
        form['page'] = '1'
        form['defaultLinks'] = ''
        form['nopage'] = ''
        return form


    def toExtension(self, sourceExtension, targetExtension, form_dict):
        form_dict['name'] = targetExtension
        form_dict['targetDataId'] = form_dict['targetDataId'].replace(sourceExtension, targetExtension)
        form_dict['divID'] = form_dict['divID'].replace(sourceExtension, targetExtension)
        form_dict['targetid'] = form_dict['targetid'].replace(sourceExtension, targetExtension)
        form_dict['objID'] = form_dict['objID'].replace(sourceExtension, targetExtension)

        return self.handleExtension(form_dict)

    def newExtensionObj(self, module, className):
        obj = self.extensionManager.loadExtensionEx(module, className)

        return obj

    def handleExtension(self, form):

        if form['rID'] == "":
            return ""
        return self.extensionManager.doWork(form, self)

    def write2File(self, fileName, lines):
        if os.path.exists(fileName):
            f = open(fileName, 'w')
            if len(lines) > 0:
                for line in lines:
                    #print line
                    f.write(line)
            else:
                f.write('')
                f.close() 

    def loadFiles(self, folder, fileType):
        cur_list = os.listdir(folder + '/')
        result = ''
        f_list = []
        f_list_2 = []
        for f in cur_list:
            if f.startswith('jquery'):
                f_list.append(f)
            else:
                f_list_2.append(f)
        cur_list = f_list + f_list_2
        for f in cur_list:
            if f.endswith(fileType):
                result += ''.join(open(folder + '/' + f, 'rU').readlines())
        return result

    def loadAlexa(self):
        if os.path.exists('db/rank/top500web-alexa2016'):
            f = open('db/rank/top500web-alexa2016', 'rU')
            for line in f.readlines():
                record = Record(line)
                title = record.get_title().strip()
                key = title[0 : 1]
                if self.alexa_dict.has_key(key):
                    self.alexa_dict[key].append(record)
                else:
                    self.alexa_dict[key] = [record]
        #print self.alexa_dict

    def loadEngins(self):
        if len(self.search_engin_dict) == 0 and os.path.exists(Config.engin_list_file):
            f = open(Config.engin_list_file,'rU')
            all_lines = f.readlines()
            for line in all_lines:
                record = EnginRecord(line)
                if record.get_title() != '':
                    url = record.get_url().strip()
                    self.search_engin_url_dict[record.get_title().strip()] = url
                    self.search_engin_dict[record.get_title().strip()] = record
                    desc = record.get_description().strip()
                    categorys = desc.split(' ')
                    for category in categorys:
                        if self.search_engin_type_engin_dict.has_key(category):
                            self.search_engin_type_engin_dict[category].append(url)
                        else:
                            self.search_engin_type_engin_dict[category] = [url]

                        if self.search_engin_type_2_engin_title_dict.has_key(category):
                            self.search_engin_type_2_engin_title_dict[category].append(record.get_title().strip())
                        else:
                            self.search_engin_type_2_engin_title_dict[category] = [record.get_title().strip()]
                        
            
            self.search_engin_type_2_engin_title_dict['star'] = self.sortEnginList(self.search_engin_type_2_engin_title_dict['star'])
        if len(self.search_engin_type) == 0 and os.path.exists(Config.engin_type_file):
            f = open(Config.engin_type_file,'rU')
            all_lines = f.readlines()
            for line in all_lines:
                if line.startswith('#'):
                    continue
                if line.strip() != '':
                    self.search_engin_type.append(line.strip().strip())
        if len(self.engin_extension) == 0 and os.path.exists(Config.engin_extension_file):
            f = open(Config.engin_extension_file,'rU')
            all_lines = f.readlines()
            for line in all_lines:
                if line.startswith('#'):
                    continue
                if line.strip() != '':
                    self.engin_extension.append(line.strip().strip())

    def loadDDGEngins(self):
        year = int(time.strftime('%Y',time.localtime(time.time())))
        if os.path.exists('db/metadata/engin_list-duckduckgo' + str(year)):
            f = open('db/metadata/engin_list-duckduckgo' + str(year),'rU')
            all_lines = f.readlines()
            for line in all_lines:
                record = PriorityRecord(line)
                if record.get_title() != '':
                    self.ddg_search_engin_url_dict[record.get_title().strip()] = record.get_url().strip()
                    self.ddg_search_engin_dict[record.get_title().strip()] = record
        if os.path.exists('db/metadata/engin_type-duckduckgo' + str(year)):
            f = open('db/metadata/engin_type-duckduckgo' + str(year),'rU')
            all_lines = f.readlines()
            for line in all_lines:
                if line.startswith('#'):
                    continue
                record = Record(line)
                if record.get_title() != '':
                    self.ddg_search_engin_type.append(record.get_title().strip())

    def fixUrl(self, baseUrl, url):
        link = url
        if url.startswith('./'):
            url = url[1:]
        if url.find('/', url.find('/') + 1) != -1 and baseUrl.find('/', baseUrl.find('//') + 2) != -1:
            baseUrl = baseUrl[0 : baseUrl.find('/', baseUrl.find('//') + 2) + 1]
        if url.startswith('//'):
            url = 'http:' + url
        if url.startswith('http') == False:
            if baseUrl.endswith('/') and url.startswith('/'):
                link = baseUrl + url[1:]
            elif baseUrl.endswith('/') == False and url.startswith('/') == False:
                if baseUrl.find('/', baseUrl.find('//') + 2) != -1:
                    link = baseUrl[0 : baseUrl.rfind('/')] + '/' + url
                else:
                    link = baseUrl + '/' + url

            else:
                link = baseUrl + url

        if link.startswith('//'):
            return 'http:' + link
        return link

    def gen_pages(self, currentPage, totalPage, libraryUrl):
        html = '<div style="margin-left:auto; text-align:center;margin-top:2px; margin-right:auto;">'
        if currentPage > 1:
            html += '<a href="javascript:toPage(' + str(currentPage - 1) + ", '" + libraryUrl.replace("'", '"') +"');" + '"><font size="5"> <</font></a>'
            html += '&nbsp;&nbsp;&nbsp;&nbsp;'
        for page in range(0, totalPage):
            
            if page + 1 == currentPage:
                html += '<a href="javascript:toPage(' + str(page + 1) + ", '" + libraryUrl.replace("'", '"') +"');" + '"><font size="5" color="#00BFFF"><b>' + str(page + 1) +'</b></font></a>&nbsp;'
            else:
                html += '<a href="javascript:toPage(' + str(page + 1) + ", '" + libraryUrl.replace("'", '"') + "');" +'">' + str(page + 1) +'</a>&nbsp;'
        if currentPage < totalPage -1:
            html += '&nbsp;&nbsp;&nbsp;&nbsp;'
            html += '<a href="javascript:toPage(' + str(currentPage + 1) + ", '" + libraryUrl.replace("'", '"') +"');" + '"><font size="5"> ></font></a>'
        html += '<div style="height: 11px; width: 100px"></div></div>'
        return html

    def gen_menu(self, source):
        db_root = '<a href="http://' + Config.ip_adress + '/?db=?" style="margin-right:6px">Home</a>'
        html = '<div style="margin-left:auto; text-align:center;margin-top:2px; margin-right:auto; ">' + db_root
        for link_dict in Config.fav_links.items():
            src = link_dict[1]
            if src.startswith('http') == False:
                src = 'http://' + src
            html += self.enhancedLink(src, link_dict[0], style='style="margin-right:6px"', library=source, module='main') + '&nbsp;'
        html += '</div><div style="height: 21px; width: 100px"></div>'
        return html

    def gen_libary(self, root=False, user_name='', user_image='', source=''):
        html = ''
        db_root = ''
        origin_user_name = user_name
        if Config.default_library != '':
            user_name = Config.default_library
            if user_name.endswith('-library'):
                user_name = user_name[0 : user_name.rfind('-')]
        #if root:
        #    db_root = '<a href="http://' + Config.ip_adress + '/?db=?" style="margin-right:6px">Home</a>'
        if user_name != None and user_name != '':
            lines = 0
            if os.path.exists('db/library/' + user_name + '-library'):
                f = open('db/library/' + user_name + '-library')
                lines = len(f.readlines())
                f.close()
            html = '<div style="float:right; margin-top:2px; margin-right:10px ">' + db_root
            '''
	    for link_dict in Config.fav_links.items():
		html += '<a href="http://' + link_dict[1] + '" style="margin-right:6px">' + link_dict[0] + "</a>"
            '''
            if user_image != '':
                html += '<img src="' + user_image + '" width="20" height="20" style="border-radius: 50%;"/>'
            content = user_name

            if Config.display_all_library:
                html += self.gen_libary2(user_name, source, libraryList=Config.menu_library_list)
            else:
                html += self.enhancedLink('http://' + Config.ip_adress + '/?db=library/&key=?', 'library', library=source, module='main') + '&nbsp;'

            #html +=  self.enhancedLink('http://' + Config.ip_adress + '/?db=library/&key=' + user_name + '-library&column=3&width=' + Config.default_width, content + '<font size="2">(</font><font size="2" color="#999966">' + str(lines) + '</font><font size="2">)</font>', library=source, module='main') + '&nbsp'
            html +=  self.enhancedLink('http://' + Config.ip_adress + '/?db=library/&key=' + user_name + '-library', content + '<font size="2">(</font><font size="2" color="#999966">' + str(lines) + '</font><font size="2">)</font>', library=source, module='main') + '&nbsp'

            html += self.gen_library_more(source) + '</div>'
        else:
            html = '<div style="float:right; margin-top:2px; margin-right:10px">' + db_root + self.enhancedLink('http://' + Config.ip_adress + '/login', 'Login', library=source, module='main') + '</div>'
        html += '<div style="height: 21px; width: 100px"></div>'

        return html

    def gen_libary2(self, user, source, libraryList=[], inLibary=True):
        html = ''
        file_list = os.listdir("db/library/")
        count = 0
        for item in file_list:
            if item.startswith('.'):
                continue
            if Config.default_library == '' and item.find(user) != -1:
                continue
            if Config.default_library != '' and item.find(Config.default_library) != -1:
                continue
            passItem = False
            found = False
            if len(libraryList) > 0:
                for library in libraryList:
                    if item == library:
                        found = True
                if inLibary:
                    passItem = not(found)      
                else:
                    passItem = found            

            if passItem:
                continue
            count += 1
            f = open('db/library/' + item)
            lines = len(f.readlines())
            f.close()
            #html += self.enhancedLink('http://' + Config.ip_adress + '/?db=library/&key=' + item + '&column=3&width=' + Config.default_width,  item.replace('-library', '') + '<font size="2">(</font><font size="2" color="#999966">' + str(lines) + '</font><font size="2">)</font>', library=source, module='main') + '&nbsp;'
            html += self.enhancedLink('http://' + Config.ip_adress + '/?db=library/&key=' + item,  item.replace('-library', '') + '<font size="2">(</font><font size="2" color="#999966">' + str(lines) + '</font><font size="2">)</font>', library=source, module='main') + '&nbsp;'

            if count > 5 :
                count = 0
                #html += '<br/>' #need adjust config content_margin_top

        return html
        
    def gen_library_more(self, source):
        return self.enhancedLink('', "more", module='menu', library=source, resourceType='menu', dialogMode=True, dialogPlacement='bottom') 

    def getAlexaRank(self, engin):
        engin = engin.lower().strip()
        if len(self.alexa_dict) > 0:
            key = engin.strip()[0 : 1].lower()
            for k, v in self.alexa_dict.items():
                if k.lower() == key:
                    for r in v:
                        title = r.get_title().lower().strip()
                        if title.find(engin) != -1 or engin.find(title) != -1:
                            return r.get_id()[r.get_id().find('-') + 1 : ].strip()
        return '0'

                
    def removeDoubleSpace(self, text):
        text = text.replace('\n',' ')
        while (text.find('  ') != -1):
            text = text.replace('  ', ' ')
        return text

    def validEngin(self, engin):
        records = self.search_engin_dict.keys()
        if self.ddg_mode:
            records = self.ddg_search_engin_dict.keys()
        for item in records:
            if item.lower() == engin.lower():
                return True
        print "invalided search engin: " + engin
        return False

    def caseLine(self, line):
        if line.isupper() == False:
            return line
        if self.check_contain_chinese(line):
            return line
            
        if line.strip().find(' ') == -1:
            return line
        new_line = ''
        for item in line.split(' '):
            new_line += item[0 : 1] + item[1:].lower() + ' '
        return new_line


    def shortFileName(self, file_name):
        pos = 0
        while (file_name.find('/', pos) != -1):
            pos = file_name.find('/', pos) + 1
        return file_name[pos : ]

    cache_records = {}

    """
    matchType: by id(1)  by title(2) by line(3)

    """
    def getRecord(self, keyword, use_subject='', path='', return_all=False, log=False, use_cache=True, matchType=1, accurate=True):
        #print path + 'xxx'

        cacheKey = keyword
        if path != '':
            cacheKey += '-' + path
        if self.cache_records.has_key(cacheKey) and use_cache:
            if log:
                print 'return cached record for ' + keyword
            if return_all:
                return self.cache_records[cacheKey]
            else:
                return self.cache_records[cacheKey][0]
        subject = default_subject;
        if use_subject != "":
            subject = use_subject
        if path == '':
            path = self.getPath(subject)
        if log:
            print 'searching %s'%keyword + " in " + subject + '  matchType:' + str(matchType)
        record_list = []
        if log:
            print keyword
            print path
        files = ''
        if os.path.isfile(path):
            files = [path]
        else:
            files = self.find_file_by_pattern(keyword, path)

        print files
        for file_name in files:
            if os.path.isfile(file_name) == False:
                continue
            if log:
                print file_name
            f = open(file_name)
            for line in f.readlines():
                record = Record(line)
                record.set_path(file_name)
                found_tag = False

                if matchType == 1: # by id 
                    if accurate:
                        if record.get_id().lower().strip() == keyword.lower().strip():
                            found_tag = True
                    else:
                        if record.get_id().lower().find(keyword.lower().strip()) != -1:
                            found_tag = True
                elif matchType == 2: # by title
                    if accurate:
                        if record.get_title().lower().strip() == keyword.lower().strip():
                            found_tag = True
                    else:
                        if record.get_title().lower().strip().find(keyword.lower().strip()) != -1:
                            found_tag = True
                elif matchType == 3: # by line
                    if record.line.lower().strip().find(keyword.lower().strip()) != -1:
                        found_tag = True
                if found_tag:
                    if log:
                        print "found " + record.get_id() + ' ' + record.get_title() + ' ' + record.get_url() + ' in ' + self.shortFileName(file_name)
                    if return_all:
                        record_list.append(record)
                    else:
                        self.cache_records[cacheKey] = [record]
                        return record
        if return_all:
            if len(record_list) > 0:
                self.cache_records[cacheKey] = record_list
                return record_list
            else:
                if log:
                    print "no record found in " + subject +" db"
                return record_list.append(Record(''))
        else:
            if log:
                 print "no record found in " + subject +" db"
            return Record('')

    def getPath(self, subject):
        return os.getcwd() + "/db/" + subject + "/"

    def getEnginUrl(self, engin):
        if self.ddg_mode:
            return self.ddg_search_engin_url_dict[engin]
        if self.search_engin_url_dict.has_key(engin):
            return self.search_engin_url_dict[engin]
        else:
            return ''

    def getEnginUrlOtherInfo(self, record):
        r = CourseRecord(record.line)
        if r.get_author() != None:
            author = r.get_author().strip() 
            if author != '':
                return "&user=" + author.replace(' ', '%20');
        return ""

    def getEnginUrlEx(self, engin, keyword, query=''):
        url = ''

        keyword = self.preprocessSearchKeyword(keyword, engin, '')
        if engin != '':

            url = self.getEnginUrl(engin)
            if url.find('%s') != -1:
                url = self.toAccountUrl(url, keyword.strip())
            else:
                url += keyword.strip()
        if engin == "crunchbase" and query.find(':') != -1:
            url = self.getEnginUrl(engin) + keyword.strip().replace(' ', '-')
            query = query[query.find(':') + 1 :].strip()
            if query == 'star':
                query = 'organization'
            url = self.toAccountUrl(url, query.strip())

        return url

    def preprocessSearchKeyword(self, keyword, engin, url):
        #print "preprocessSearchKeyword:" + keyword + " " + engin
        if (engin != '' and engin == 'github*topic') or (url != '' and url.find('github.com/topic') != -1):
            keyword = keyword.strip().replace(' ', '-').replace('%20', '-')
        if (engin != '' and engin == 'gitplanet'):
            if self.getValueOrTextCheck(keyword):
                keyword = self.getValueOrText(keyword, returnType='value').strip()
            if keyword.find("/") != -1:
                keyword = keyword[keyword.find("/") + 1:].lower()

        return keyword

    def toAccountUrl(self, url, keyword):
        if keyword.find('@') != -1 and keyword.strip().startswith('@') == False:
            temp1 = keyword.split('@')
            temp2 = url.split('%s')
            new_url = url
            #print '1======' + new_url + '<br>'
            for i in range(0, len(temp1)):
                index = new_url.find('%s') + 1
                #print new_url[0: index + 1] + '<br>'
                #print new_url[index + 1:].strip() + '<br>'
                new_url = new_url[0: index + 1].replace('%s', temp1[i]) + new_url[index + 1:].strip()
            #print '======' + new_url + '<br>'
            return new_url
        return url.replace("%s", keyword.strip())

    def getEnginHtmlLink(self, engin, keyword, color=''):
        if color != '':
            return ' <a href="' + self.getEnginUrlEx(engin, keyword) + '" target="_blank"> <font size="2" color="' + color + '">' + engin + '</font></a>'
        else:
            return ' <a href="' + self.getEnginUrlEx(engin, keyword) + '" target="_blank"> <font size="2" color="#999966">' + engin + '</font></a>'

    def getRecommendType(self, fileName):
        if os.path.exists(Config.engin_type_file):
            f = open(Config.engin_type_file, 'rU')
            engin_types = []
            for line in f.readlines():
                if line.startswith('#') or line.strip() == '':
                    continue
                engin_types.append(line.strip())
            f.close()
            for et in engin_types:
                if fileName.rfind(et) != -1:
                    return et
        return ''


    def recommendEngins(self, folder):
        engins = []
        if Config.recommend_engin_type != '':
            if Config.recommend_engin_type.find(' ') != -1:
                engin_types = Config.recommend_engin_type.split(' ')
                per_engin_for_type = Config.recommend_engin_num / len(engin_types)
                for enginType in engin_types:
                    engins += self.realGetEnginList([enginType], self.search_engin_dict.values())[0 : per_engin_for_type]

            else:
                engins = self.realGetEnginList([Config.recommend_engin_type], self.search_engin_dict.values())
        else:
            etype = self.getRecommendType(folder)
            if etype != '':
                engins = self.realGetEnginList([etype], self.search_engin_dict.values())
            elif folder.find('neuro') != -1 or folder.find('biology') != -1 or folder.find('lifescience') != -1:
                engins = self.realGetEnginList(['dxy.cn', 'wikipedia', 'biostars', 'neurostars', 'youtube', 'google', 'baidu', 'gene', 'pubmed', 'ebi', 'gen.lib', 'amazon'], self.search_engin_dict.values(), match_title=True)


        if len(engins) == 0:
            return self.realGetEnginList(['star'], self.search_engin_dict.values())
        else:
            #engins = sorted(engins, key=lambda engin:self.search_engin_dict[engin].get_priority(), reverse=True)
            #for e in engins:
            #    print e + ' p:' + self.search_engin_dict[e].get_priority()

            if len(engins) < Config.recommend_engin_num:
                return engins
            return engins[0 : Config.recommend_engin_num]

    def getTopEngin(self, tag, sort=False, number=1):
        if tag.startswith('d:') == False:
            tag = 'd:' + tag.strip()
        engins = self.getEnginList(tag, sort=sort)
        if len(engins) > 0:
            if number == 1:
                return [engins[0]]
            else:
                if number + 1 <= len(engins):
                    return engins[0 : number]
                else:
                    return engins
        else:
            return []


    def getEnginList(self, engins, folder='', sort=False, recommend=False):
        if engins.startswith('description:') or engins.startswith('d:'):
            key = engins[engins.find(':') + 1 :].strip()
            engin_list = []
            tags = engins[engins.find(':') + 1 :].strip().split(' ')
            cachedEngins = []
            tags2 = []

            if len(tags) > 0 and ''.join(tags).strip() != '':
                for tag in tags:
                    if self.search_engin_type_2_engin_title_dict.has_key(tag.strip()):
                        cachedEngins = cachedEngins + self.search_engin_type_2_engin_title_dict[tag.strip()]
                    else:
                        tags2.append(tag.strip())
                if len(tags2) == 0:
                    self.search_engin_type_2_engin_title_dict[key] = cachedEngins
                    if sort:
                        self.search_engin_type_2_engin_title_dict[key] = self.sortEnginList(cachedEngins)
                    return self.search_engin_type_2_engin_title_dict[key]
                else:
                    tags = tags2

                #print engins
                if self.ddg_mode:
                    self.search_engin_type_2_engin_title_dict[key] = self.getDDGEnginList(tags)
                else:
                    self.search_engin_type_2_engin_title_dict[key] = self.realGetEnginList(tags, self.search_engin_dict.values())

                if len(cachedEngins) > 0:
                    self.search_engin_type_2_engin_title_dict[key] = cachedEngins + self.search_engin_type_2_engin_title_dict[key]
                    if sort:
                        self.search_engin_type_2_engin_title_dict[key] = self.sortEnginList(self.search_engin_type_2_engin_title_dict[key])

            if self.search_engin_type_2_engin_title_dict.has_key(key) and len(self.search_engin_type_2_engin_title_dict[key]) == 0 and recommend:
                self.search_engin_type_2_engin_title_dict[key] = self.recommendEngins(folder)
            
            if self.search_engin_type_2_engin_title_dict.has_key(key):
                return self.search_engin_type_2_engin_title_dict[key] 
            else:
                return []
        else:
            return engins.split(' ')



    def realGetEnginList(self, tags, records, match_title=False, sort=True):
        engin_list = []
        if len(tags) == 0:
            return engin_list
        for record in records:
            if match_title:
                engin = record.get_title().strip()
                str_tags = ' ' + ' '.join(tags) + ' '
                if str_tags.find(' ' + engin + ' ') != -1:
                    engin_list.append(engin)
            else:
                desc = record.get_description().strip()
                desc = desc[desc.find(':') + 1 :].strip()
                for tag in tags:
                    if desc.find(tag) != -1:
                        #engin = record.get_title().strip()
                        engin_list.append(record.get_title().strip())
        if sort:
            return self.sortEnginList(engin_list)
        return engin_list

    def sortEnginList(self, engin_list):
        #print 'sortEnginList'
        return sorted(engin_list, key=lambda engin:self.search_engin_dict[engin].get_priority(), reverse=True)

    def getDDGEnginList(self, tags):
        if len(self.ddg_search_engin_type) == 0 or len(self.ddg_search_engin_dict) == 0:
            self.loadDDGEngins()
        return self.realGetEnginList(tags, self.ddg_search_engin_dict.values())

    def getEnginPriority(self, engin):
        record = None
        if self.ddg_mode:
            record = self.ddg_search_engin_dict[engin]
        else:
            record = self.search_engin_dict[engin]
        return record.get_priority()

    def getAllEnginList(self):
        engin_list = []
        records = None
        if self.ddg_mode:
            records = self.ddg_search_engin_dict.values()
        else:
            records = self.search_engin_dict.values()
        for record in records:
            engin = record.get_title().strip()
            engin_list.append(record.get_title().strip())
        return engin_list

    def getDefaultEnginHtml(self, title, default_links_row):
        count = 0
        html = ''
        for e in self.getEnginList('d:default'):
            html += self.getEnginHtmlLink(e, title)
            count += 1
            if count == default_links_row:
                return html
        return html

    def getEnginListLinks(self, engins, topic, rID='', query = '', color="#999966", fontSize=11, i=0, j=0, useQuote=False, module='', library='', pluginsMode=False):
        if self.ddg_mode:
            return self.getDDGEnginListLinks(engins, topic, rID, query, color, fontSize)
        if topic == '':
            return ''
        result = {}
        keyword = topic.strip()
        engin_display = ''
        for engin in engins:
            engin_display = engin
            engin_display = self.getEnginIcon(engin)
            
            #if engin_display == 'sanity':
            #    engin_display = 'arxiv-sanity'
            if self.searchByID(engin):
                keyword = rID.strip()
            else:
                keyword = topic.strip()
            if Config.hiden_content_after_search and pluginsMode == False:
                script = "var pid = this.parentNode.parentNode.id; hidenMoreContent(pid, 1);"
                style = "color:" + color + '; font-size: ' + str(fontSize) + "pt;"
                result[engin] = self.enhancedLink(self.getEnginUrlEx(engin, keyword, query), self.formatEnginTitle(engin_display), style=style, script=script, useQuote=useQuote, module=module, library=library, searchText=keyword, rid='#rid')
            else:
                style = "color:" + color + '; font-size:' + str(fontSize) + "pt;"
                result[engin] = self.enhancedLink(self.getEnginUrlEx(engin, keyword, query), self.formatEnginTitle(engin_display), style=style, useQuote=useQuote, module=module, library=library, searchText=keyword, rid='#rid')
            result[engin] += '&nbsp;'
        return result

    def formatEnginTitle(self, engin):
        record = None
        if self.search_engin_dict.has_key(engin):
            record = self.search_engin_dict[engin]
        if record == None:
            return engin
        shortname = record.get_shortname()
        if shortname != None and shortname != '':
            return shortname.strip()

        if len(engin) > 10:
            return '[' + engin[0 : len(engin) - (len(engin) / 2) - 1] + ']'
        return engin

    def getEnginIcon(self, engin):
        if Config.disable_icon:
            return engin
        record = self.search_engin_dict[engin]
        icon = record.get_icon()
        if icon != None and icon.strip() != '':
            return '<image margin-right:"2px" width="18px" height="18px" alt="' + engin + '" src="' + icon.strip() + '"/>'
        else:
            return engin

    def getDDGEnginListLinks(self, engins, topic, id='', query = '', color="#999966", fontSize=11):
        return {}

    def getDescDivs(self, divid, enginType, keyword, links_per_row, scrip, color, color2, fontSize, dataMarginTop='', disableNavEngins=False):
        result = '<div id="' + divid + '" style="display: none;">'
        if disableNavEngins == False:
            engin_list = self.getEnginList('d:' + enginType)
            #print engin_list
            remain = len(engin_list)
            last = 0
            count = 0
            while remain > 0:
                #print '---'
                #print 'remain' + str(remain)
                #print 'links_per_row' + str(links_per_row)
                #print 'last' + str(last)
                if remain > links_per_row:
                    engin_list_dive = engin_list[last : last + links_per_row]
                else:
                    engin_list_dive = engin_list[last : ]
                    remain = 0
                #print engin_list_dive
                div = '<div id="' + divid + '-' + str(count) + '" ">'
                link_count = 0
                for e in engin_list_dive:
                    link_count += 1
                    if link_count % 2 == 0:
                        div += self.genLinkWithScript2(scrip, e.strip() , color2, self.priority2fontsize(e.strip(), self.getEnginPriority(e.strip()),fontSize)) + '&nbsp;'
                    else:
                        div += self.genLinkWithScript2(scrip, e.strip(), color, self.priority2fontsize(e.strip(), self.getEnginPriority(e.strip()),fontSize)) + '&nbsp;'
                remain -= links_per_row
                last += links_per_row
                #print remain
                #print last
                div += '</div>'
                count += 1
                result += div
        result += "</div>" 
        if dataMarginTop != '':
            result += '<div id="' + divid + '-data" style="border-radius: 10px 10px 10px 10px; margin-top:' + dataMarginTop + 'px;"></div>'
        else:
            result += '<div id="' + divid + '-data" style="border-radius: 10px 10px 10px 10px;"></div>'
        
        return result



    def output2Disk(self, records, module, fileName, outputFormat='', ignoreUrl=False, append=False):
        data = ''
        if outputFormat == 'markdown':
            data += '## ' + fileName.replace('%20', ' ') + '\n'
            data += '- ### ' + module + '\n'
        fileName = fileName.strip().replace('"', '').replace("'", '').replace('%20', ' ').replace('(', '').replace(')', '').replace(' ', '-').replace('|', '').lower() 
        if outputFormat != '':
            if outputFormat == 'markdown':
                fileName += '.md'
            else:
                fileName += '-' + outputFormat
        else:
            fileName += str(datetime.date.today().year)
        count = 0
        for record in records:
            count += 1
            url = record.get_url().strip()
            if ignoreUrl:
                url = ''
            if outputFormat == 'markdown':
                if record.line.find(' parentid:') != -1 and record.get_parentid().strip() != '':
                    data += '    '
                data += '- [ ] [' + record.get_title().strip() + '](' + url + ')\n'
            else:
                data += record.get_id().strip() + '-' + str(count) + ' | ' + record.get_title().strip() + ' | ' + url + ' | ' + record.get_describe().strip() + '\n'
        outputDir = Config.output_data_to_new_tab_path + module + '/'
        if outputFormat != '':
            outputDir += outputFormat + '/'
        if os.path.exists(outputDir) == False:
            os.makedirs(outputDir)

        flag = 'w'

        if append:
            flag = 'a'

        f = open(outputDir + fileName, flag)
        f.write(data)
        f.close()

        url = ''
        if outputFormat.strip() != '':
            url += 'edit ' + os.getcwd() + '/' + outputDir + fileName
            return url

        url += 'http://' + Config.ip_adress + '/?db=' + Config.output_data_to_new_tab_path.replace('db/', '')
        url += module + '/'
        if outputFormat.strip() != '':
            url += outputFormat + '/'
        
        url += '&key=' + fileName
        return url

    def bestMatchEngin(self, text, resourceType=''):
        #TODO get best engin by resourceType
        #print resourceType
        if text.startswith('http'):
            return text
        if resourceType != '' and ' '.join(self.tag.tag_list_direct_link).find(resourceType) != -1:
            return self.getEnginUrl('glucky')
        return self.getEnginUrl(Config.smart_link_engin)

    def bestMatchEnginUrl(self, text, resourceType='', source=''):
        if source.find('github') != -1 and resourceType.find('author') != -1:
            return 'http://github.com/' + text
        url = self.bestMatchEngin(text, resourceType=resourceType)
        return self.toQueryUrl(url, text)

    def clientQueryEnginUrl(self, originUrl, text, resourceType, module):
        result = {}
        engin = ''
        url = self.toQueryUrl(self.getEnginUrl(Config.smart_link_engin), text)
        
        if originUrl != '':
            url = originUrl

        result[Config.smart_link_engin] = url

        if resourceType !='' and Config.smart_engin_for_tag.has_key(resourceType.strip()):
            result = {}
            for u in self.expandEngins(Config.smart_engin_for_tag[resourceType.strip()]):
                result[u.strip()] = self.toQueryUrl(self.getEnginUrl(u), text)

        '''
        if module != '' and Config.smart_engin_for_extension.has_key(module.strip()):
            result = {}
            for u in self.expandEngins(Config.smart_engin_for_extension[module.strip()]):
                result[u.strip()] = self.toQueryUrl(self.getEnginUrl(u), text)  
        '''
        return result

    dialog_engin_cache = None

    def expandEngins(self, engins):
        result = []
        if isinstance(engins, str):
            engins = [engins]
        for e in engins:
            if e.find(':') != -1:
                result = result + self.getEnginList(e, sort=True)
            else:
                result.append(e)
        return result

    def clientQueryEnginUrl2(self, text, resourceType='', enginArgs=''):
        result = {}
        engins = []
        if resourceType == 'social-tag':
            text = text.replace('#', '')
        if resourceType != '' and Config.smart_engin_for_tag.has_key(resourceType):
            engins = self.expandEngins(Config.smart_engin_for_tag[resourceType])
        elif len(Config.smart_engin_for_dialog) > 0:
            engins = self.expandEngins(Config.smart_engin_for_dialog)
        elif self.dialog_engin_cache != None:
            engins = self.dialog_engin_cache
        else:
            if Config.recommend_engin_type_for_dialog != '':
                if Config.recommend_engin_type_for_dialog.find(' ') != -1:
                    engin_types = Config.recommend_engin_type_for_dialog.split(' ')
                    per_engin_for_type = Config.recommend_engin_num / len(engin_types)
                    for enginType in engin_types:
                        engins += self.getEnginList('d:' + enginType, sort=True)[0 : per_engin_for_type]
                else:
                    engins = self.getEnginList('d:' + Config.recommend_engin_type_for_dialog, sort=True)
            else:
                if resourceType != '' and Config.recommend_engin_by_tag and ' '.join(self.search_engin_type).find(resourceType) != -1:
                    engins = self.getEnginList('d:' + resourceType, sort=True)
                else:
                    if enginArgs != '' and enginArgs.startswith('d:'):
                        engins = self.getEnginList(enginArgs, sort=True)
                    else:
                        engins = self.getEnginList('d:star', sort=True)
            self.dialog_engin_cache = engins.append('glucky');

        for engin in engins:
            result[engin] = self.toQueryUrl(self.getEnginUrl(engin), text, searchEngine=engin)

        return result

    def clientQueryDirs(self, path, rID='', fileName=''):
        dirs = []

        for item in os.listdir(path):
            full_path = os.path.join(os.getcwd() + '/' + path + '/', item)
            if os.path.isfile(full_path) == False:
                dir_path = (path + '/' + item).replace('//', '/')
                dirs.append(dir_path)
                dirs += self.clientQueryDirs(dir_path)
        return dirs

    def genTagLink(self, text, module, library, rid, resourceType, dialogMode, aid, crossref='', accountTag='', suffix=':', searchText='', fileName=''):
        #if crossref:
        #    dialogMode = False
        htmlText = '<font color="#66CCFF">' + text + '</font>'
        if fileName == '':
            fileName = library
        return self.enhancedLink('', htmlText, module=module, library=library, fileName=fileName, rid=rid, resourceType=resourceType, urlFromServer=True, dialogMode=dialogMode, aid=aid, isTag=True, log=False, searchText=searchText) + suffix


    smartLinkTagCache = {}
    def isSmartLinkTag(self, tag, list_smart_link):
        if tag == '':
            return False
        prefix = ''
        if tag.find(':') != -1:
            prefix = tag[0 : tag.find(':') + 1].strip()
        else:
            prefix += tag + ':'

        if self.smartLinkTagCache.has_key(prefix):
            #print 'isSmartLinkTag cache'

            return True


        reslut = ' '.join(list_smart_link).find(prefix) != -1

        if reslut:
            self.smartLinkTagCache[prefix] = ''

        return reslut


    directLinkTagCache = {}
    def isDirectLinkTag(self, tag, list_direct_link):

        if tag == '':
            return False
        prefix = ''
        if tag.find(':') != -1:
            prefix = tag[0 : tag.find(':') + 1].strip()
        else:
            prefix += tag + ':'


        if self.directLinkTagCache.has_key(prefix):
            #print 'isDirectLinkTag cache'
            return True

        result = ' '.join(list_direct_link).find(prefix) != -1

        if result:
            self.directLinkTagCache[prefix] = ''
        return result

    def isAccountTag(self, tag, tag_list_account):
        #print tag + '<br>'
        #if tag.strip().startswith('archiv'):
        #    print tag_list_account
        if tag == '':
            return False
        prefix = ''
        if tag.find(':') != -1:
            prefix = tag[0 : tag.find(':') + 1].strip()
        else:
            prefix += tag + ':'


        #print prefix
        return tag_list_account.has_key(prefix)




    def accountMode(self, tag_list_account, tag_list_account_mode, engin, resourceType):
        if Config.smart_engin_lucky_mode_for_account:
            accountTags = ' '.join(tag_list_account)
            accountModeTags = ' '.join(tag_list_account_mode)
            return accountTags.find(engin + ':') != -1 and accountModeTags.find(resourceType + ':') != -1
        return False

    def toQueryUrl(self, url, text, searchEngine=''):
        if text.startswith('http'):
            return text

        text = self.preprocessSearchKeyword(text, searchEngine, url)
        if url.startswith('http') == False and self.search_engin_dict.has_key(url):
            url = self.getEnginUrl(url)

        query_text = text.replace('"', ' ').replace("'", ' ').replace(' ', "%20") 
        if url.find('%s-%s') != -1:
            url = url.replace('%s-%s', query_text.replace('%20', '-'))
        elif url.find('%s%s') != -1:
            url = url.replace('%s%s', query_text.replace('%20', ''))
        elif url.find('%s') != -1:
            url = self.toAccountUrl(url, query_text.strip())
        else:
            url += query_text

        #print 'url:' + url
        return url


    def getValueOrTextCheck(self, text):
        if text.find('(') != -1 and text.strip().endswith(')'):
            if text.find('+') != -1:
                newText, value = self.getValueOrTextSplit(text)
                if value.find('+') == -1:
                    return False
                for v in value.split('+'):
                    if self.getValueOrTextCheck(v) == False:
                        if v.find('(') == -1 and v.find(')') == -1:
                            return True
                        else:
                            return False
            return True
        return False

    def getValueOrTextSplit(self, text):
        value = text[text.find('(') + 1 :].strip()
        value = value[0 : value.rfind(')')].strip()
        newText = text[0 : text.find('(')].strip() 
        #if self.isShortUrl(value):
        #    value = 'http://' + value
        return newText, value

    def isUrlFormat(self, text):
        if text.find('*') != -1:
            return False
        if text.startswith('http') or self.isShortUrl(text):
            return True
        return False
        
    def isShortUrl(self, text):
        if text.find('http') != -1:
            text = text.replace('http://', '').replace('https://', '')
        if text.startswith('bit.ly') or text.startswith('goo.gl'):
            return True
        return False

    def getValueOrText(self, text, returnType='text'):
        if self.getValueOrTextCheck(text):
            #print 'text:' + text + ' accountTag:' + str(accountTag) + ' returnType:' + returnType + '<br>'
            newText, value = self.getValueOrTextSplit(text)
            if returnType == 'text':
                #print newText + '<br>'
                return newText
            elif returnType == 'value':
                #print value + '<br>'
                return value

        return text.encode('utf-8')

    #hook user usage data

    def getCrossref(self, keyword, path='db/library'):
        cmd = 'grep -riE "' + keyword + '" ' + path
        print cmd
        output = ''
        try:
            output = subprocess.check_output(cmd, shell=True)
        except Exception as e:
            return ''
        adict = {}
        titleDict = {}
        for line in output.split('\n'):
            fileName = line[0 : line.find(':')].strip().replace('//', '/')
            firstIndex = line.find('|')
            rID = line[line.find(':') + 1 : firstIndex].strip().replace(' ', '%20')
            title = line[firstIndex + 1 : line.find('|', firstIndex + 1)].strip()
            if title != '':
                if title.find(',') != -1:
                    title = title.replace(',', '')
                if title.find('+') != -1:
                    title = title[0 : title.find('+')]
                if title.find('#') != -1:
                    title = title[0 : title.find('#')]
                if titleDict.has_key(title):
                    continue
                if adict.has_key(fileName):
                    adict[fileName].append(title)
                else:
                    adict[fileName] = [title]
                titleDict[title] = title
        result = ''
        print '---getCrossref---'
        for k, v in adict.items():
            #print k + ' #' + '#'.join(v)
            prefix = ''
            if k.startswith('db/'):
                prefix = k[3:]
            ft = '+'.join(v).strip()
            if ft.endswith('+'):
                ft = ft[0 : len(ft) - 2]
            result += prefix + '#' + ft
            if k != adict.items()[len(adict) - 1][0]:
                result += ', '

        
        if result != '':
            result = 'crossref:' + result
        print result
        return result

    def getSubSearchinItemList(self, searchItemList, parentCmd, loopSearch=True):
        itemList = [] 
        for item in searchItemList:
            descItem = item[1]
            if descItem.find('searchin:') != -1:
                subSearchinDesc = descItem[descItem.find('searchin:') + len('searchin:') :]
                print 'subSearchinDesc of ' + parentCmd + ':' + subSearchinDesc
                for subCmd in subSearchinDesc.split(','):
                    subCmd = subCmd.strip()
                    if self.searchCMDHistory.has_key(subCmd.lower()) == False:
                        print 'search subCmd:' + subCmd
                        self.searchCMDHistory[subCmd.lower()] = ''
                        sunSearchItemList = self.processCommand(subCmd, '', noDiv=True, unfoldSearchin=False, noFilterBox=True, returnMatchedDesc=True, isRecursion=True)
                        #print sunSearchItemList
                        if len(sunSearchItemList) > 0:
                            itemList = itemList + sunSearchItemList
                            if loopSearch:
                                itemList = itemList + self.getSubSearchinItemList(sunSearchItemList, subCmd, loopSearch=loopSearch)
                    else:
                        print subCmd + ' already be searched###'

        return itemList

    searchCMDHistory = {}


    def unfoldFilter(self, filterStr, filterDict, isRecursion=False, unfoldAll=False):
        print 'unfoldAll:' + str(unfoldAll) + ' ' + filterStr
        result = ''
        unfoldedCmd = ''
        
        for cmd in filterStr.split('+'):  
            cmd = cmd.replace('%20', ' ').strip() 
            if cmd.startswith(':') and filterDict.has_key(cmd):
                result = filterDict[cmd]
                
                if unfoldAll and self.search_engin_type_2_engin_title_dict.has_key(cmd.replace(':', '')):
                    for item in self.search_engin_type_2_engin_title_dict[cmd.replace(':', '')]:
                        if self.isAccountTag(item, self.tag.tag_list_account):
                            unfoldedCmd += item + ':' + ' + '                       

                cmdList = []
                if result.find('+') != -1:
                    #unfoldedCmd = ''
                    for cmd in result.split('+'):
                        cmd = cmd.strip()
                        print cmd
                        cmdList.append(cmd)

                else:
                    cmdList.append(result)

                for cmd in cmdList:
                    if cmd.startswith(':'):
                        unfoldedCmd += self.unfoldFilter(cmd, filterDict, isRecursion=True) + ' + '
                    else:
                        unfoldedCmd += cmd + ' + '
                #else:
                #    if result.startswith(':'):
                #        unfoldedCmd += self.unfoldFilter(result, filterDict, isRecursion=True) + ' + '
                #    else:
                #        unfoldedCmd += result + ' + '
            else:
                unfoldedCmd += cmd + ' + '
    
        if isRecursion == False:
            unfoldedCmd = unfoldedCmd.strip()
            unfoldedCmd = unfoldedCmd.replace('+  +', '+')
            if unfoldedCmd.endswith(' +'):
                unfoldedCmd = unfoldedCmd[0 : len(unfoldedCmd) - 2]

        cmdDict = {}
        result = ''
        for item in unfoldedCmd.split(' + '):
            item = item.strip()
            if cmdDict.has_key(item):
                continue
            else:
                cmdDict[item] = ''
                result += item + ' + '
        if result.endswith(' + '):
            result = result[0 : len(result) - 3]
        print 'unfoldFilter:' + result
        print ''
        return result
    

    def unfoldCommand(self, commandList):
        title = ''
        searchCommand = ''
        postCommand = ''

        append = Config.autoAppendDescFilterCategory


        if len(commandList) == 3:
            title = commandList[0]
            searchCommand = commandList[1]
            postCommand = commandList[2]
            if postCommand == ':append':
                postCommand = ''
                append = True
        elif len(commandList) == 2:
            title = commandList[0]
            searchCommand = commandList[1]
        elif len(commandList) == 1:
            title = commandList[0]

        title = self.unfoldFilter(title, PrivateConfig.processSourceDict, unfoldAll=False)
        if searchCommand != '':
            searchCommand = self.unfoldFilter(searchCommand, PrivateConfig.processSearchCommandDict, unfoldAll=append)


        #if title.find("%") != -1:
        #    title = title.replace("%", '/')
        #print title + ' ' + searchCommand + ' ' + postCommand
        return title, searchCommand, postCommand


    def unfoldCommandEx(self, command, parentCmd=''):
        if command.startswith('_>:'):
            return command
        parts = []
        if command.find('/') != -1:
            parts = command.split('/')
        else:
            parts = [command]
    
        title, searchCommand, postCommand = self.unfoldCommand(parts)
    
        result = title
        if searchCommand != '':
            result += '/' + searchCommand
        if postCommand != '':
            result += '/' +postCommand

        return result

    def getTitleFilter(self, title):
        titleFilter = title[0 : title.find(':') + 1]
        title = title[title.find(':') + 1 :]  
        if Config.tagAliasDict.has_key(titleFilter):
            titleFilter = Config.tagAliasDict[titleFilter]
        return title, titleFilter
   
    def genTitleCommandHtml(self, title, style, parentCmd=''):
        print 'genTitleCommandHtml:' + title
        parts = title.split('+')
        desc = ''
        preCmd = ''
        for part in parts:
            part = part.strip()
            subParts = []

            if part.find('*') != -1:
                subParts = part.split('*')
            else:
                subParts = [part]
                preCmd = part[0 : preCmd.rfind('>') + 1]
            
            for subPart in subParts:
                desc += subPart + ', '

        desc = desc.strip()
        if desc.endswith(','):
            desc = desc[0 : len(desc) - 1]

        html = ''

        if desc != '':
            html = '<div id="titleCmdDiv" align="left" ' + style + '>' + self.genDescHtml('searchin:' + desc, Config.course_name_len, self.tag.tag_list, iconKeyword=True, fontScala=1, module='searchbox', nojs=False, unfoldSearchin=False, parentOfSearchin='') + '</div>'

        

        print 'titleCommandHtml:' + html
        return html
    

    def subprocessCmd(self, command):
        process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
        proc_stdout = process.communicate()[0].strip()
        #print proc_stdout
        return proc_stdout

    '''
    title example: 
        >>dog/blog+home+twitter:dev/:merger
        >dog + >unreal
        >dog *unreal
    '''
    def processCommand(self, title, url, recordObj=None, style='', noDiv=False, nojs=False, unfoldSearchin=True, noFilterBox=False, returnMatchedDesc=False, filterMatchedDesc=False, isRecursion=False, parentOfSearchin='', noDescHtml=False, hiddenDescHtml=False, showDynamicNav=True):
        print 'processCommand ' + title
        topOriginTitle = title
        cutDescText = True
        highLightText = ''
        editMode = False
        if title.startswith('!'):
            return self.genDefaultPluginInfo(title[1:])
        elif title.endswith('!'):
            return self.genDefaultPluginInfo(title[0:len(title) - 1])
    
        if title == '' or title.lower() == Config.history_quick_access_name.lower():
            if os.path.exists('extensions/history/data/quick-access-history'):
                f = open('extensions/history/data/quick-access-history', 'r')
                html = ''
                desc = ''
                for line in f.readlines():
                    if line.strip() == '':
                        continue
                    r = Record(line)
                    lineDesc = r.get_describe()
    
                    desc = self.mergerDesc(desc, lineDesc)
    
                if desc != '':
                    tag = Tag()
                    html = self.genDescHtml(desc, Config.course_name_len, tag.tag_list, iconKeyword=True, fontScala=1, module='searchbox', editMode=editMode)
    
                f.close()
    
                return html
        if isRecursion == False:
            self.searchCMDHistory = {}
    
        titleFilter = ''
        searchCommand = ''
        postCommand = ''
        searchRecordMode = False
        searchRecordTagOrField = ''

        tList = [title]
        if title.find('&') != -1:
            tList = title.split('&')
    
        resultHtmlList = []
        for t in tList:
            title = t.strip()
            if title != '':
                descCacheList = []
                originSearchCommand = '' 
                if title.startswith('library/') == False and title.startswith('_>') == False:
                    if title.find('/') != -1: 
                        print "111" + title
                        parts = title.split('/')
                        title, searchCommand, postCommand = self.unfoldCommand(parts)
                    else:
                        print "222" + title
                        title = self.unfoldFilter(title, PrivateConfig.processSourceDict, unfoldAll=False)
                        if title.find('/') != -1: 
                            parts = title.split('/')
                            title, searchCommand, postCommand = self.unfoldCommand(parts)

                    #postCommand = searchCommand
                    #searchCommand = "github:"

                    if searchCommand.startswith(":deeper"):
                         originSearchCommand = searchCommand
                         searchCommand = searchCommand[searchCommand.find("\\") + 1:]

                    print "=========title====" + title
                    print "=========postCommand====" + postCommand
                    print "============searchCommand==" + searchCommand
                
                if title.find("\\") != -1:
                    title = title.replace("\\", '/')
                if searchCommand.find("\\") != -1:
                    searchCommand = searchCommand.replace("\\", '/')

                if title.find('+') != -1 or title.find('*') != -1:
                    unfoldSearchin = False
                if searchCommand != '':
                    cutDescText = False
                    if searchCommand.startswith(':') == False:
                        highLightText = searchCommand
                    
                titleList = [title]
        
                if title.find('+') != -1:
                    titleList = title.split('+')
                tempTitleList = []
                for title in titleList:
                    if title.startswith("??"):
                        tempTitleList2 = [title]
                        if title.find("|") != -1:
                            tempTitleList2 = title.replace("|", "+??").split("+")

                        for tt in tempTitleList2:
                            tempTitleList.append(tt)
                            tt = tt.strip()
                            if tt.find(" ") != -1:
                                tempTitleList.append("??" + tt[2:].replace(" ", "-"))
                                tempTitleList.append("??" + tt[2:].replace(" ", ""))
                            elif tt.find("-") != -1:
                                tempTitleList.append("??" + tt[2:].replace("-", " "))
                    else:
                        tempTitleList.append(title)
                titleList = tempTitleList

                resultHtml = ''

                newTitleList = []
                print 'titleList:' + str(titleList)
                for title in titleList:
                    title = title.strip()
                    if title.startswith('%>'):
                        title = title[2 :].replace('%20', ' ')
                        newTitleList.append('=>' + title)# search alias
                        newTitleList.append('->' + title)# search searchin
                        newTitleList.append('>' + title) # search title
                        #newTitleList.append('?category:' + title) # search category
                        highLightText = title
                    elif title.startswith('g%>'):
                        title = title[3 :].replace('%20', ' ').strip()
                        newTitleList.append('=>' + title)# search alias
                        newTitleList.append('->' + title)# search searchin
                        newTitleList.append('>' + title) # search title 
                        searchCommand = ':'
                        postCommand = ':group-short %>' + title 
                        highLightText = title                    
                    elif title.startswith('?>'):
                        title = title[2 :].replace('%20', ' ')
                        matchedDescList = self.processCommand('>' + title, '', returnMatchedDesc=True)

                        #print matchedDescList
                        newTitleList.append('=>' + title)# search alias
                        newTitleList.append('->' + title)# search searchin
                        if len(matchedDescList) == 1:
                            desc = matchedDescList[0][1]
                            parentCategory = matchedDescList[0][2]
                            #print desc
                            line = ' | | | ' + desc
                            if desc.find('alias:') != -1:
                                alias = self.reflection_call('record', 'WrapRecord', 'get_tag_content', line, {'tag' : 'alias:'})
                                if alias != None:
                                    for item in alias.split(','):
                                        item = item.strip()
                                        newTitleList.append('=>' + item) # search alias of itself

                            if desc.find('category:') != -1:
                                category = self.reflection_call('record', 'WrapRecord', 'get_tag_content', line, {'tag' : 'category:'})
                                if category != None and parentCategory != '':
                                    newTitleList.append('#' + parentCategory + '->' + category + ':') # search category
                            if desc.find('searchin:') != -1:
                                newTitleList.append('>>' + title)# search searchin and title of itself
                            else:
                                newTitleList.append('>' + title)
                            if desc.find('command:') != -1:
                                command = self.reflection_call('record', 'WrapRecord', 'get_tag_content', line, {'tag' : 'command:'})
                                for cmd in command.split(','):
                                    cmd = cmd.strip()
                                    if self.getValueOrTextCheck(cmd):
                                        newTitleList.append(self.getValueOrText(self.decodeCommand(cmd), returnType='value')) #search command
                                    else:
                                        newTitleList.append(self.decodeCommand(cmd)) #search command


                        print '?>:' + title
                        print newTitleList

                    elif title.startswith('c>'):
                        title = title[2 :].replace('%20', ' ')
                        matchedDescList = self.processCommand('>' + title, '', returnMatchedDesc=True)
                        if len(matchedDescList) == 1:
                            desc = matchedDescList[0][1]
                            rTitle = matchedDescList[0][2]
                            line = ' | | | ' + desc
                            if desc.find('category:') != -1:
                                category = self.reflection_call('record', 'WrapRecord', 'get_tag_content', line, {'tag' : 'category:'})
                                if category != None:
                                    cmd = '#' + rTitle + '->' + category + ':'
                                    newTitleList.append(cmd)
                    elif title.startswith('e>'):
                        title = title[2 :].replace('%20', ' ')
                        newTitleList.append('>' + title)
                        editMode = True
                    elif title.startswith('??'):
                        # ??title  ==   ?title/title
                        title = title[2 :].replace('%20', ' ').strip()
                        if originSearchCommand == '':
                            if searchCommand != "":
                                searchCommand += "+" + title
                            else:
                                searchCommand = title
                        style = 'style="padding-left:20px; padding-top: 10px;"'
                        newTitleList.append('?' + title)
                    elif title.startswith('g=>'):
                        title = title[3 :].replace('%20', ' ').strip()
                        searchCommand = ':'
                        postCommand = ':group-short =>' + title
                        newTitleList.append('=>' + title)
                    elif title.startswith('g?=>'):
                        title = title[4 :].replace('%20', ' ').strip()
                        searchCommand = ':'
                        postCommand = ':group-short ?=>' + title
                        newTitleList.append('?=>' + title)
                    elif title.startswith('g>>'):
                        title = title[3 :].replace('%20', ' ').strip()
                        searchCommand = ':'
                        postCommand = ':group-short >>' + title
                        newTitleList.append('>>' + title)
                    elif title.startswith('g>>>'):
                        title = title[4 :].replace('%20', ' ').strip()
                        searchCommand = ':'
                        postCommand = ':group-short >>>' + title
                        newTitleList.append('>>>' + title)
                    elif title.startswith('g->'):
                        title = title[3 :].replace('%20', ' ').strip()
                        searchCommand = ':'
                        postCommand = ':group-short ->' + title
                        newTitleList.append('->' + title)
                    elif title.startswith('g#'):
                        title = title[2 :].replace('%20', ' ').strip()
                        searchCommand = ':'
                        postCommand = ':group-short #' + title
                        newTitleList.append('#' + title)
                    else:
                        newTitleList.append(title)

                print 'newTitleList:' + str(newTitleList)

                for title in newTitleList:
                    titleFilter = ''
                    title = title.strip()
                    print 'search title:' + title
                    originTitle = title
                    deepSearch = True
                    accurateMatch = False
                    accurateAliasSearchinMatch = True
                    startMatch = False
                    endMatch = False
                    reMatch = False
                    searchinLoopSearch = Config.searchinLoopSearch
                    searchinLoopSearchMore = Config.searchinLoopSearch
                    #highLightText = ''
                    searchRecordMode = False
                    if title.startswith('->'):
                        title = title.replace('->', '?searchin:')
                        unfoldSearchin = False
                    if title.startswith('?->'):
                        title = title.replace('?->', '?searchin:')
                        unfoldSearchin = False
                        accurateAliasSearchinMatch = False
                    if title.startswith('=>'):
                        title = title.replace('=>', '?alias:')
                        unfoldSearchin = False  
                    if title.startswith('?=>'):
                        title = title.replace('?=>', '?alias:')
                        accurateAliasSearchinMatch = False
                        unfoldSearchin = False
                    if title.startswith('_>'):
                        if title.startswith('_>:'):
                            output = ''
                            output = self.subprocessCmd(title[3:])
                            #print 'output:' + output
                            #js = 'onfocus="' + "setbg('custom-textarea','#e5fff3');" + '" onblur="' + "setbg('custom-textarea','white');" + '"'
                            js = ''
                            html = '<br><textarea id="custom-textarea" readonly rows="35" cols="175" style="border: none; font-size: 16px; background-color: black; color:white; border-radius: 10px;" ' + js + '>' + output + '</textarea>'
                            resultHtmlList.append(html)
                            #resultHtmlList.append('<div align="left">' + output.replace('\n', '<br>') + '</div>')
                            continue
                        title = title.replace('_>', '?command:')
                        unfoldSearchin = False 
                        accurateAliasSearchinMatch = False


                    if title.startswith('>>>'):
                        title = title.replace('>>>', '>')
                        searchinLoopSearch = True
                        searchinLoopSearchMore = True

                    if title.startswith('>>'):
                        title = title.replace('>>', '>')
                        searchinLoopSearch = True
                        searchinLoopSearchMore = False
        
                    if title.startswith('?') or title.endswith('?'):
                        if title.startswith('?'):
                            title = title[1:]
                            deepSearch = False
                            unfoldSearchin = False
                        elif title.endswith('?'):
                            title = title[0:len(title) - 1]
                            deepSearch = False  
                        if title.find(':') != -1:
                            title, titleFilter= self.getTitleFilter(title)
                        highLightText = title
                        print 'highLightText:' + title

                    if title.startswith('#>'):
                        title = title[1:]
                        deepSearch = False
                        unfoldSearchin = False
                    if title.startswith(':'):
                        parts = []
                        title = title[1:]
                        if title.find(' of ') != -1:
                            parts = title.split(' of ')
                        elif title.find(' from ') != -1:
                            parts = title.split(' from ')
        
                        if len(parts) == 2:
                            title = parts[1].strip()
                            searchCommand = parts[0].strip()
                        elif len(parts) == 3:
                            title = parts[2].strip()
                            searchCommand = parts[1].strip()
                            postCommand = parts[0].strip()
        
                        if title.find(' and ') != -1:
                            title = title.replace(' and ', '*')
                        if title.find(',') != -1:
                            title = title.replace(',', '*')
                        accurateMatch = True
                    
                    if title.startswith('>'):
                        title = title[1:]
                        accurateMatch = True
                    elif title.endswith('>'):
                        title = title[0:len(title) - 1]
                        accurateMatch = True

                    if title.startswith('#'):
                        title = title[1:]
                        searchRecordMode = True
                        if title.find('->') != -1:
                            searchRecordTagOrField = title[title.find('->') + 2 :]
                            title = title[0 : title.find('->')]
                        accurateMatch = True
                    if title.startswith('^>'):
                        title = title[2:]
                        accurateMatch = True
                        startMatch = True
                    elif title.endswith('^'):
                        title = title[0:len(title) - 1]
                        accurateMatch = True
                        startMatch = True
        
                    if title.startswith('$>'):
                        title = title[2:]
                        accurateMatch = True
                        endMatch = True
                    elif title.endswith('$'):
                        title = title[0:len(title) - 1]
                        accurateMatch = True
                        endMatch = True
        
                    titles = title.split('*')
                    print titles

                    for titleItem in titles:
                        titleItem = titleItem.strip()
                        crossref = ''
                        
                        idOrTitle = ''

                        if titleItem.find('->') != -1:
                            idOrTitle = titleItem[0 : titleItem.find('->')].strip().lower()
                            titleItem = titleItem[titleItem.find('->') + 2:]

                        if recordObj != None:
                            print 'recordObj is not null'
                            crossref = recordObj.get_crossref().strip()
                        elif titleItem != '':
                        #    kg = KnowledgeGraph()
                            if titleItem.startswith('library/'):
                                crossref = 'crossref:' + titleItem[0 : titleItem.find('->')]    
                                titleItem = titleItem[titleItem.find('->') + 2 :]
                            else:
                                crossref = self.getCrossref(titleItem)
                        print crossref
                        print 'titleItem:' + titleItem
                        print 'titleFilter:' + titleFilter
                        #return ''
                        if crossref != '':
                            crossrefList = []
                            if crossref.find(',') != -1:
                                crossrefList = crossref.split(',')
                            else:
                                crossrefList = [crossref]
                
                            html = ''
                            searchinHtml = ''
                            chartHtml = ''
                            resultDict = {}
                            #print crossrefList
                            for cr in crossrefList:
                                cr = cr.replace('crossref:', '')
                                if cr.find('#') != -1:
                                    #print 'cr::::'
                                    #print cr
                                    result = self.getCrossrefUrls(cr)
                                    #print result
                                    for k, v in result.items():
                                        resultDict[k] = v
                                else:
                                    print cr
                                    k, v = self.getCrossrefUrl(cr)
                                    resultDict[k] = v
                                    #print k + ' ' + v
                
                            print 'resultDict:'
                            print resultDict
                            linkDict = self.genPluginInfo(resultDict, returnDict=True)
                
                            rCount = 0
                            #print linkDict

                            titlePathDict = {}

                            if recordObj != None:
                                titlePathDict[recordObj.get_title().strip()] = recordObj.get_path().strip()
                            else:
                                for k, v in resultDict.items():
                                    path = ''
                                    rTitle = ''
                                    for sv in v.split('&'):
                                        if sv.find('db') != -1:
                                            path += 'db/' + sv[sv.find('db') + 3:]
                                        if sv.startswith('key'):
                                            path += sv[sv.find('key') + 4:]
                                        if sv.startswith('filter'):
                                            rTitle = sv[sv.find('filter') + 7:]


                                    titlePathDict[rTitle] = path

                            print 'titlePathDict:'
                            print titlePathDict

                            for rTitle, path in titlePathDict.items():
                                #print k + ' ' + v
                                k = rTitle

                                r = None
                                if searchRecordMode and rTitle.lower() != title.lower():
                                    continue

                                print 'path:' + path + ' ' + rTitle
                                
                                if recordObj != None:
                                    print 'use recordObj'
                                    r = recordObj
                                else:
                                    r = self.getRecord(rTitle, path=path, matchType=2, use_cache=False)
    
                                if r != None and r.line.strip() != '' and r.get_id().strip() != '':
                                    #print r.line + '))0' + r.get_id()
                                    r.set_path(path) 
                                    r.set_crossref(path + '#' + rTitle)
                                    if idOrTitle != '':
                                        recordID = r.get_id().strip().lower()
                                        recordTitle = r.get_title().strip().lower()
                                        if recordID != idOrTitle and recordTitle != idOrTitle:
                                            continue
                                    library = path[path.rfind('/') + 1 :]
                                    print library
                                    tag = Tag()
                                    print '-----'
                                    print titleItem

                                    #return ''
                                    #desc = r.get_desc_field2(utils, title, tag.get_tag_list(library), toDesc=True, prefix=False)
                                    matchedTextList = []
                                    descList = []
                                    matchedcategoryList = []
                                    if searchRecordMode:
                                        ignore = False
                                        if searchRecordTagOrField != '':
                                            print 'searchRecordTagOrField:' + searchRecordTagOrField
                                            if searchRecordTagOrField.endswith(':'):
                                               searchRecordDesc = searchRecordTagOrField + self.reflection_call('record', 'WrapRecord', 'get_tag_content', r.line, {'tag' : searchRecordTagOrField})
                                               r = Record(' | | | ' + searchRecordDesc)

                                            else:
                                                matchedTextList, descList, matchedcategoryList = r.get_desc_field3(self, searchRecordTagOrField, tag.get_tag_list(library), toDesc=True, prefix=False, deepSearch=deepSearch, accurateMatch=accurateMatch, startMatch=startMatch, endMatch=endMatch)
                                                
                                                ignore = True
                                        unfoldSearchin = False
                                        if ignore == False:
                                            matchedTextList, descList = r.record_to_text_desc_list(self, tag.get_tag_list(library), tag.tag_list_account)
                                    else:
                                        matchedTextList, descList, matchedcategoryList = r.get_desc_field3(self, titleItem, tag.get_tag_list(library), toDesc=True, prefix=False, deepSearch=deepSearch, accurateMatch=accurateMatch, startMatch=startMatch, endMatch=endMatch)
                                    if len(descList) == 0:
                                        continue

                                    
                                    #print descList
                                    #print matchedTextList
                                    #print str(len(matchedTextList))
                                    #print str(len(descList))

                                    #count = 0
                                    #print 'debug:'
                                    #for desc in descList:
                                    #    print str(count)
                                    #    print matchedTextList[count]
                                    #    print descList[count]
                                    #    count += 1

                                    #continue
                                    once = True
                                    count = 0
                                    rCount += 1
                                    for desc in descList:
                                        if desc == None or desc == '':
                                            count += 1
                                        else:
                                            #print k
                                            #print desc
                                            matchedText = ''
                                            matchedCategory = ''
                                            if len(matchedTextList) - 1 >= count: 
                                                matchedText = matchedTextList[count]
                                                if len(matchedcategoryList) > 0:
                                                    matchedCategory = matchedcategoryList[count]

                                                #if matchedText == '':
                                                #    print 'error:'
                                                #    print str(count)
                                                #    print desc
                                            
                                            count += 1
                                            crossref = ''
                                            start = desc.find('searchin:')
                                            end = 0
                                            searchinDesc = ''
                                            #desc += " command:g->" + matchedText + "(g->" + matchedText + "), ->" + matchedText + "(->" + matchedText + "/:), g>>" + matchedText + "(g>>" + matchedText + "), >>" + matchedText + "(>>" + matchedText + "/:), g>>>" + matchedText + "(g>>>" + matchedText+ "), >>>" + matchedText + "(>>>" + matchedText + "/:), " + "Social(>>" + matchedText + "/:social), Video(>>" + matchedText + "/:video), Project(>>" + matchedText + "/:project), Paper(>>" + matchedText + "/:paper), News(>>" + matchedText + "/:news), State(>>" + matchedText + "/:state)" 
                                            if start != -1:
                                                descPart1 = desc[0 : start]
                                                descPart2 = desc[start : ]
                                                descPart3 = ''
                                                end = self.next_pos(descPart2, len('searchin:'), 1000, self.tag.tag_list)
                                                if end != -1:
                                                    descPart3 = descPart2[0 : end]
                                                    descPart2 = descPart2[end :]

                                                desc = descPart1.strip() + ' ' + descPart2.strip()

                                                if desc.find('category:') == -1 and matchedCategory != '':
                                                    desc += ' category:' + matchedCategory

                                                desc += ' ' + descPart3.strip()

                                                searchinDesc = descPart3
                                                #print desc
                                            elif desc.find('category:') == -1 and matchedCategory != '':
                                                desc += ' category:' + matchedCategory


                                            descHtml = ''

                                            if searchCommand != '' and searchinDesc != '' and searchinLoopSearch:
                                                for cmd in titleList:
                                                    if self.searchCMDHistory.has_key(cmd.lower()) == False:
                                                        self.searchCMDHistory[cmd.lower()] = ''
                                                cmds = searchinDesc[searchinDesc.find(':') + 1 :].split(',')
                                                cmds = self.doUnfoldSearchin(cmds, '', returnCmdList=True, editMode=editMode)
                                                #print 'searchin cmdList:' + str(cmds)
                                                for cmd in cmds:
                                                    cmd = cmd.strip()
                                                    cmdList = [cmd]
                                                    #if cmd.startswith('&>') and self.getValueOrTextCheck(cmd):
                                                    #    value = self.getValueOrText(cmd, returnType='value')
                                                    #    cmdList = value.split('&')
                                                    for cmd in cmdList:
                                                        if self.searchCMDHistory.has_key(cmd.lower()) == False:
                                                            print 'search cmd:' + cmd
                                                            self.searchCMDHistory[cmd.lower()] = ''
                                                            searchDescList = self.processCommand(cmd, '', noDiv=True, unfoldSearchin=False, noFilterBox=True, returnMatchedDesc=True, isRecursion=True, parentOfSearchin=originTitle)
                                                            #print searchDescList
                                                            if len(searchDescList) > 0:
                                                                descCacheList = descCacheList + searchDescList
                                                                print 'searchinLoopSearchMore:' + str(searchinLoopSearchMore)
                                                                if searchinLoopSearchMore:
                                                                    subSearchItemList = self.getSubSearchinItemList(searchDescList, cmd, loopSearch=searchinLoopSearchMore) 
    
                                                                    if len(subSearchItemList) > 0: 
                                                                        descCacheList = descCacheList + subSearchItemList                                                                       


                                            fontScala = 1                     

                                            if returnMatchedDesc == False and searchCommand == '':
                                                rID = r.get_id().strip()
                                                fileName = r.get_path().strip()
                                                if noDescHtml:
                                                    descHtml = '<br>'
                                                else:
                                                    descHtml = self.genDescHtml(desc, Config.course_name_len, tag.tag_list, iconKeyword=True, fontScala=fontScala, module='searchbox', nojs=nojs, unfoldSearchin=False, parentOfSearchin=originTitle, cutText=cutDescText, parentOfCategory=rTitle, rid=rID, library=fileName, field=matchedText, editMode=editMode, previewLink=True)
                                                    if hiddenDescHtml:
                                                        descHtml = '<br>'
                                                if searchinDesc != '' and unfoldSearchin:
                                                    searchinHtml += self.genDescHtml(searchinDesc, Config.course_name_len, tag.tag_list, iconKeyword=True, fontScala=1, module='searchbox', nojs=nojs, unfoldSearchin=unfoldSearchin, parentOfSearchin=originTitle, rid=rID, library=fileName, field=matchedText, editMode=editMode)
                                                if unfoldSearchin and desc.find('chart:') != -1:
                                                    chartHtml = self.genChartHtml(desc)
                                                    
                                            print 'titleFilter:' + titleFilter + ' title:' + title
                                            
                                            if titleFilter != '':
                                                descTemp = ''
                                                if desc.find(titleFilter) != -1:
                                                    tagStr = titleFilter
                                                    #print 'tagStr:' + tagStr
                                                    line = ' | | | ' + desc
                                                    descTemp = self.reflection_call('record', 'WrapRecord', 'get_tag_content', line, {'tag' : tagStr})
                                                    if descTemp != None:
                                                        print 'descTemp:' + descTemp
                                                '''
                                                index1 = desc.find(titleFilter)
                                                index2 = desc.find(':', index1 + len(titleFilter))
                                                if index1 != -1:
                                                    if index2 != -1:
                                                        descTemp = desc[index1 : index2]
                                                    else:
                                                        descTemp = desc[index1 :]
                                                print descTemp
                                                '''
                                                found = False
                                                if accurateAliasSearchinMatch and titleFilter == 'alias:' or titleFilter == 'searchin:':
                                                    prefix = ''
                                                    itemList = descTemp.split(',');
                                                    if titleFilter == 'searchin:':
                                                        prefix = '>'
                                                        itemList = self.doUnfoldSearchin(itemList, '', returnCmdList=True, editMode=editMode)
                                                    if titleFilter == 'alias:' and matchedText.lower() == title.lower():
                                                        found = True

                                                    for item in itemList:
                                                        item = item.strip().lower()
                                                        if titleFilter == 'searchin:' and item.startswith('&>'):
                                                            for innerItem in self.getValueOrText(item, returnType='value').split('&'):
                                                                if innerItem.lower().strip() == prefix + title.lower():
                                                                    found = True
                                                                    break
                                                        else:
                                                            if item == prefix + title.lower():
                                                                found = True
                                                                break
                                                else:
                                                    found = descTemp.lower().find(title.lower()) != -1
                                                if descTemp != None and descTemp != '' and found:
                                                    print 'found'
                                                    #print desc + '111' + descTemp
                                                    #print desc
                                                    #print str([matchedText, desc])
                                                    dcSubList = [matchedText, desc, rTitle, r.get_crossref(), r.get_id().strip(), r]
                                                    if filterMatchedDesc and searchCommand != '':
                                                         filterDescList, filterDesc, filterHtml = self.genFilterHtml(searchCommand, [dcSubList], highLight=False, editMode=editMode)
                                                         desc = filterDesc
                                                    descCacheList.append([matchedText, desc, rTitle, r.get_crossref(), r.get_id().strip(), r]) 
                                                else:
                                                    descHtml = ''
    
                                            else:
                                                #print matchedText
                                                #print desc
                                                dcSubList = [matchedText, desc, rTitle, r.get_crossref(), r.get_id().strip(), r]
                                                if filterMatchedDesc and searchCommand != '':
                                                    filterDescList, filterDesc, filterHtml = self.genFilterHtml(searchCommand, [dcSubList], highLight=False, editMode=editMode)
                                                    desc = filterDesc
                                                descCacheList.append([matchedText, desc, rTitle, r.get_crossref(), r.get_id().strip(), r])

                                            if matchedText != '' and descHtml != '':
                                                #once = False
                                                script = ''
                                                script2 = ''
                                                if matchedText.strip()  != '':
                                                    crossref = path[path.find('/') + 1 :].strip() + '#' + rTitle + '->' + matchedText.strip() 
                                                    #script = "exclusiveCrossref('plugin', '" + matchedText + "' ,'' ,'" + crossref + "');"
                                                    script = "typeKeyword('>" + matchedText + "', '');chanageLinkColor(this, '#E9967A', '');"
                                                    #script2 = "typeKeyword('%>" + matchedText + "/:/:group-short >" + matchedText + "', '')"
                                                    #g%>world tr;g>>world tr
                                                    line = ' | | | ' + desc
                                                    aliasStr = self.reflection_call('record', 'WrapRecord', 'get_tag_content', line, {'tag' : 'alias:'})
                                                    typeCmd = "g->" + matchedText + ";g>>" + matchedText

                                                    if len(matchedcategoryList) > 0:
                                                        for ct in matchedcategoryList:
                                                            typeCmd += ';#' + rTitle + '->' + ct + ':/:/:group-short #' + rTitle + '->' + ct + ':'

                                                    if aliasStr != None and aliasStr != '':
                                                        print 'aliasStr:' + aliasStr
                                                        typeCmd += ';g=>' + matchedText
                                                        for alias in aliasStr.split(','):
                                                            alias = alias.strip()
                                                            typeCmd += ';g=>' + alias


                                                    script2 = "typeKeyword('" + typeCmd + "', '');chanageLinkColor(this, '#E9967A', '');"

                                                else:
                                                    crossref = path[path.find('/') + 1 :].strip() + '#' + rTitle
            
                                                    crossrefHtml = '<font style="font-size:10pt; font-family:San Francisco; color:red">' + crossref + '</font>'
            
                                                if script != '':
                                                    print 'rTitle:' + rTitle
                                                    print 'path:' + path

                                                    libraryText = path[path.find('/') + 1 :].strip()
                                                    libraryPart = '<font style="font-size:9pt; font-family:San Francisco; color:#b2adeb">' + libraryText + '</font>'
                                                    titlePart = '<font style="font-size:10pt; font-family:San Francisco; color:#8178e8">' + rTitle + '</font>'
                                                    arrowPart = '<font style="font-size:10pt; font-family:San Francisco; color:#EC7063">-></font>'
                                                    matchedTextPart = '<font style="font-size:12pt; font-family:San Francisco; color:#1a0dab">' + matchedText.strip() + '</font>'
                                                    libraryUrl = 'http://' + Config.ip_adress + '/?db=library/&key=' + libraryText[libraryText.rfind('/') + 1 :]
                                                    js = "lastHoveredText='" + libraryText + "'; lastHoveredUrl='" + libraryUrl + "';"
                                                    js2 = "lastHoveredText='" + rTitle + "'; lastHoveredUrl='" + libraryUrl + '&filter=' + rTitle + "'; search_box.value='#" + rTitle + "/:'"
                                                    js3 = "lastHoveredText='" + matchedText + "'; lastHoveredUrl='" + self.toQueryUrl(self.getEnginUrl('google'), matchedText) + "'; search_box.value='>" + matchedText + "'"
                                                    crossrefHtml = '<a target="_blank" href="' + libraryUrl + '" onmouseover="' + js + '">' + libraryPart + '</a>' +\
                                                                    '<font style="font-size:10pt; font-family:San Francisco; color:#EC7063">#</font>' +\
                                                                    '<a href="javascript:void(0);" onclick="typeKeyword(' + "'#" + rTitle.replace('%20', ' ') + "/:/:group-short #" + rTitle + "', '');" + '" onmouseover="' + js2 + '">' + titlePart + '</a>' +\
                                                                    '<a href="javascript:void(0);" onclick="' + script2 + '">' + arrowPart + '</a>' +\
                                                                    '<a href="javascript:void(0);" onclick="' + script + '" onmouseover="' + js3 + '">' + matchedTextPart + '</a>'
                                                
                                                    if unfoldSearchin == False:
                                                        js = "showPopupContent(0, 20, 1444, 900, '>" + matchedText.strip() + "');"
                                                        crossrefHtml += '<a href="javascript:void(0);" onclick="' + js + '" >' + self.getIconHtml('', 'url', width=10, height=8) + '</a>'
 
                                                countStr = matchedText.replace(' ', '-').lower().strip() + '-' + str(rCount) + '-' + str(count)
                                                linkID = 'a-plugin-more-' + countStr
                                                ref_divID = 'div-plugin-' + countStr
                                                ref_div_style = 'style="display: none;"'
                                                #rID = 'custom-plugin-' + countStr
                                                rID = 'custom-plugin-' + r.get_id().strip() + '-pg'
                                                #print rID
                                                originTitle = crossref.replace('->', '==')
                                                url = ''
                                                appendID = countStr
                                                script = ''
                                                script = self.genMoreEnginScript(linkID, ref_divID, rID.replace(' ', '-') + '-' + str(appendID), originTitle, url, originTitle, hidenEnginSection=True)
                                                moreHtml = self.genMoreEnginHtml(linkID, script.replace("'", '"'), '...', ref_divID, '', False, descHtml='', content_divID_style=ref_div_style).strip();
                                                #print script
                                                #print moreHtml
                                                categoryButton = ''
                                                if searchRecordMode:
                                                    if searchRecordTagOrField.endswith(':') == False:
    
                                                        js = "typeKeyword('c>" + matchedText + "', '');"
                                                        
                                                        categoryButton = '<a href="javascript:void(0);" onclick="' + js +'">' + self.getIconHtml('', 'category').strip() + '</a>'


                                                html += crossrefHtml + categoryButton + ' ' +  moreHtml + '<br>'
    
            
                                            if descHtml != '':
                                                if linkDict.has_key(k):
                                                    script = ''
                                                    moreHtml = ''
                                                    if r.get_title().strip() == k:
                                                        parentText = matchedText.strip().lower().replace(' ', '-')
                                                        if parentText != '':
                                                            parentText = parentText + '-'
                                                        linkID = 'a-plugin-' + parentText + 'parent-more-' + k.lower().replace(' ', '-') + '-' + str(rCount) + '-' + str(count) + '-0'
                                                        ref_divID = 'div-' + parentText + k.lower().replace(' ', '-') + '-' + str(rCount) + '-' + str(count) + '-0'
                                                        ref_div_style = 'style="display: none;"'
                                                        rID = r.get_id().strip()
                                                        originTitle = r.get_title().strip()
                                                        if crossref.find('->') != -1:
                                                            originTitle = crossref[0: crossref.find('->')] + '==' + originTitle
                                                        script = self.genMoreEnginScript(linkID, ref_divID, rID, originTitle, '', originTitle, hidenEnginSection=True)
                                                        moreHtml = self.genMoreEnginHtml(linkID, script.replace("'", '"'), '...', ref_divID, '', False, descHtml='', content_divID_style=ref_div_style).strip();
                                                                                   
                                                     
                                                    '''
                                                    if crossref.find('#') != -1:
                                                        lib = crossref[0 : crossref.find('#')].replace('library/', '').replace('-library', '')
                                                        lib = lib[0 : 1].upper() + lib[1:]
                                                        url = Config.ip_adress + '/?db=library/&key=' + lib
    
                                                        html += '<a href="' + url + '"><font style="font-size:10pt; font-family:San Francisco;">' + lib + '</font></a> ' + self.getIconHtml(url) + ' '
                                                    '''
                                                    if searchRecordMode == False:
                                                        html += linkDict[k]

                                                        quickAccess = self.queryQuickAccess(r.get_id().strip())
                                                        if quickAccess != None:
                                                            html += self.genQuickAcessButton(quickAccess, 'plugin').strip()
                                                        if moreHtml != '':
                                                            html += ' ' + moreHtml
                                                        html += '<br>' 
                                                    html += descHtml + '<br>'
                                                    #linkDict[k] = ''
                                                else:
                                                    html += descHtml + '<br>'
                
                                path = ''
                
                            html2 = ''
                            if accurateMatch == False and titleFilter == '':
                                for k, v in linkDict.items():
                                    if v != '':
                                        html2 += v + '  '
                    
                            if html2 != '':
                                html = html + '<br>' + html2

                            if html != '' and noDiv == False:
                                html = '<div align="left" ' + style + ' >' + html + '</div>' + chartHtml + searchinHtml 
                            resultHtml += html
                #print descCacheList

                if returnMatchedDesc:
                    return descCacheList
                #else:
                    #print "returnMatchedDesc:" + str(descCacheList)
                
                if searchCommand != '':
                    if searchCommand.find(':') == -1 and self.isAccountTag(searchCommand, self.tag.tag_list_account):
                        #tagListStr = ' ' + ' '.join(tag.tag_list)
                        #if tagListStr.find(' ' + searchCommand + ':') != -1:
                        searchCommand = searchCommand + ':'
                    #else:
                        #if self.isAccountTag(descFilter[0 : descFilter.find(':')], self.tag.tag_list_account):
                        #    highLightText = descFilter[descFilter.find(':') + 1 :]
                    group = True
                    onlyHighLight = False
                    onlyHighLightFilter = ''
                    if postCommand == ':merger':
                        group = False
                        postCommand = ''

                    if postCommand.startswith(':and'):
                        if postCommand.find(' ') != -1:
                            onlyHighLightFilter = postCommand[postCommand.find(' ') :].strip()
                        onlyHighLight = True
                        if postCommand.startswith(':andm'):
                            group = False
                    #print descCacheList
                    #print 'searchCommand:' + searchCommand


                    engine = ''
                    if postCommand.startswith(':engine') or postCommand.startswith(':e '):
                        if postCommand.find(' ') != -1:
                            engine = postCommand[postCommand.find(' ') :].strip()

                    highLight = False
                    if highLightText != '':
                        highLight = True
                    #if postCommand == ':split':
                    #    highLight = False


                    innerSearchWord = ''
                    if postCommand.startswith(':innersearch') or postCommand.startswith(':ins'):
                        if postCommand.find(' ') != -1:
                            innerSearchWord = postCommand[postCommand.find(' ') :].strip()
                    
                        #postCommand = ':preview 2'
                    filterStyle = style
                    fontScala = 0
                    gridView = False
                    if showDynamicNav == False:
                        fontScala = 1
                    if postCommand.startswith(':style'):
                        showDynamicNav = False
                        gridView = True
                        cutDescText = True
                        if postCommand.find(' ') != -1:
                            filterStyle = 'style="' + postCommand[postCommand.find(' ') :].strip() + '"'
                        else:
                            #filterStyle = 'style="float:left; width:350px; height:100px;"'
                            filterStyle = 'style="float:left; width:471px;"'

                    print 'highLightText:' + highLightText
                    print 'innerSearchWord:' + innerSearchWord
                    #print 'style:' + style
                    print 'searchCommand:' + searchCommand
                    #print 'descCacheList:' + str(descCacheList)

                    combineResult = False

                    if postCommand == ":combine":
                        combineResult = True
                    
                    filterDescList, filterDesc, filterHtml = self.genFilterHtml(searchCommand, descCacheList, fontScala=fontScala, group=group, parentCmd=topOriginTitle, unfoldSearchin=unfoldSearchin, cutDescText=cutDescText, highLight=highLight, highLightText=highLightText, onlyHighLight=onlyHighLight, onlyHighLightFilter=onlyHighLightFilter, showDynamicNav=showDynamicNav, style=filterStyle, engine=engine, innerSearchWord=innerSearchWord, gridView=gridView, editMode=editMode, parentOfSearchin='>'+title, combineResult=combineResult)
                     

                    if postCommand.startswith(':style'):
                        filterHtml = '<br>' + filterHtml

                    if postCommand.startswith(':group'):
                        groupName = 'group'
                        if postCommand.find(' ') != -1:
                            groupName = postCommand[postCommand.find(' ') :].strip()
                    
                        if groupName == ':searchin':
                            line = ' | | | ' + filterDescList[0]
                            searchin = self.reflection_call('record', 'WrapRecord', 'get_tag_content', line, {'tag' : 'searchin:'})
                            if searchin != None:
                                runCMD = True
                                if postCommand.startswith(':group-short'):
                                    runCMD = False
                                return self.doUnfoldSearchin(searchin.split(','), '', runCMD=runCMD, editMode=editMode)
                            return ''
                        else:
                            layer = '&>' + groupName + '('
                            for desc in filterDescList:
                                line = ' | | | ' + desc
                                matchedTitle = self.reflection_call('record', 'WrapRecord', 'get_tag_content', line, {'tag' : 'title:'})
                                if matchedTitle != None:
                                    layer += '>' + matchedTitle.strip()
                                    if searchCommand != '' and searchCommand != ':':
                                        layer += '/' + searchCommand
                                    layer +='&'
                            if layer.endswith('&'):
                                layer = layer[0 : len(layer) - 1]
                            layer += ')'
                            runCMD = True
                            if postCommand.startswith(':group-short'):
                                runCMD = False
                            html, layerHeight = self.loadSearchinGroup([layer], parentOfSearchin, runCMD=runCMD)
                            return html

                    if innerSearchWord != '':
                        linkDict = self.genDescLinks(filterDesc, self.tag.tag_list, innerSearchWord=innerSearchWord)
                        htmlList, notSuportLink = self.genAllInOnePage(linkDict.keys(), linkDict.values(), frameCheck=False, column=2, changeBG=False, hindenLinks=True)
                        
                        filterHtml += '<div id="innersearch_preview">' + htmlList[0] + '</div>'

                    cmdResult = self.processPartPostCommand(postCommand, filterDesc, self.tag.tag_list, innerSearchWord=innerSearchWord)

                    #print 'cmdResult:' + cmdResult
                    if cmdResult != '':
                        filterHtml += cmdResult
                    #print filterDesc
                    #print searchCommand + '(' + self.desc2ValueText(filterDesc, self.tag.tag_list) + ')'
                    if postCommand.startswith(':deeper'):
                        args = ''
                        args2 = ''
                        postCommand = postCommand.replace('%20', ' ')
                        if postCommand.find(' ') != -1:
                            args = postCommand[postCommand.find(' ') :].strip()
                            if args.find(':deeper') != -1:
                                args2 = args[args.find(':deeper') + len(':deeper') : ].strip()
                                args = args[0 : args.find(':deeper') + len(':deeper')]

                            postCommand = postCommand[0 : postCommand.find(' ')]

                        sourcePart = ''
                        
                        argsList = args.split('\\')

                        sourcePart = argsList[0]

                        postCommandPart = ''

                        if len(argsList) > 1:
                            searchCommand = argsList[1]

                        if len(argsList) > 2:
                            postCommandPart = argsList[2]

                        cmd = ''
                        count = 0
                        for desc in filterDescList:
                            line = ' | | | ' + desc
                            matchedTitle = self.reflection_call('record', 'WrapRecord', 'get_tag_content', line, {'tag' : 'title:'})

                            print 'matchedTitle-->:' + sourcePart + matchedTitle
                            count += 1
                            if matchedTitle != None:
                                cmd += sourcePart + matchedTitle
                                if count != len(filterDescList):
                                    cmd += ' + '
                        cmd = cmd + '/' + searchCommand
                        if postCommandPart != '':
                            cmd += '/' + postCommandPart
                        if args2 != '':
                            cmd += ' ' + args2
                        print 'deeper cmd:' + cmd

                        return self.processCommand(cmd, '', style=style, nojs=False, noFilterBox=True, unfoldSearchin=unfoldSearchin)


                    #print 'filterDesc:' + filterDesc
                    if isRecursion == False and showDynamicNav:
                        if len(self.searchCMDHistory) > 0:
                            print 'searchCMDHistory:'
                            history = ''
                            filterHtml += self.getIconHtml('', title='searchin') + ':'
                            for k, v in self.searchCMDHistory.items():
                                history += k + ' '

                                filterHtml += '<a href="javascript:void(0);" onclick="typeKeyword(' + "'" + k + "', ''" +')" style="color: rgb(153, 153, 102); font-size:9pt;">' + k + '</a> '


                            print history
                    if postCommand != '':
                        print 'postCommand:' + postCommand
        
                        if postCommand.startswith(':contentsearch') or postCommand.startswith(':cts'):
                            cmdArgs = ''

                            if postCommand.find(' ') != -1:
                                cmdArgs = postCommand[postCommand.find(' ') : ].strip()
                                postCommand = postCommand[0 : postCommand.find(' ')]
                                print 'cmdArgs:' + cmdArgs
                            convertableCheck = True
                            if cmdArgs.find('tag=') != -1:
                                convertableCheck = False
                            url, titleList, realUrlList = self.contentSearch(filterDesc, postCommand, title=searchCommand, convertableCheck=convertableCheck)
                            
                            if url != '':
                                if cmdArgs != '':
                                    exclusiveUrl = self.doExclusive('', title, ','.join(realUrlList), '')
                                    if exclusiveUrl != '':
                                        exclusiveUrl += "&nosearchbox=true&crossrefQuery=" + cmdArgs + "&extension=convert"
                                        #print 'xx:' + url
                                        #if cmdArgs != '':
                                        #    self.localOpenFile(exclusiveUrl)
                                        url = exclusiveUrl
                                contentSearchHtml = self.enhancedLink(url, 'Content Search', module='searchbox', library='', rid='', aid='cs', refreshID='cs', resourceType='website:') 
                                
                                if len(titleList) > 0:
                                    count = 0
                                    contentSearchHtml += '<br>&nbsp;&nbsp;&nbsp;&nbsp;' + self.getIconHtml('','website') + ':'
                                    for title in titleList:
                                        title = title.strip()
                                        url = realUrlList[count]

                                        contentSearchHtml += self.enhancedLink(url, title, module='searchbox', library='', rid='', aid='cs-' + str(count), refreshID='cs-' + str(count), resourceType='website:') 

                                        #title = title + '(' + url + ')'
                                        js = "crossrefQuery ='" + cmdArgs + "';"
                                        js += "var title ='" + title + '(' + url + ')' + "';"
                                        js += "var url ='" + url + "';";
                                        js += "if (urlArray.length > 0) {\
                                                   urlArray.unshift(url);\
                                                   url = urlArray.join(',');\
                                                   urlArray = new Array();\
                                                   title = '" + title + '(' + "' + url + ')';\
                                               }\n"
                                        js += "exclusiveEx('exclusive', title, '', true, '', '', '', '', false, 'convert');"
                                        js += "crossrefQuery='';"
                                        contentSearchHtml += '<a href="javascript:void(0);" onclick="' + js + '">' + self.getIconHtml('', 'data') + '</a>'
                                        
                                        js = ''
                                        print 'cmdArgs:' + cmdArgs
                                        cQuery = cmdArgs
                                        if cmdArgs.find('=') != -1:
                                            js = "convertArgv='" + cmdArgs + "';"
                                            cQuery = ''
                                        if postCommand == ':ctsp':
                                            js += "convertPreview = true;"
                                        js += "KEY_C_DOWN = true; crossrefQuery ='" + cQuery + "' ; onHoverPreview('-website-1', '" + title + "', '" + url + "', 'searchbox', true);"
                                        contentSearchHtml += '<a href="javascript:void(0);" onclick="' + js + '">' + self.getIconHtml('', 'preview') + '</a>'
                                        
                                        count += 1

                                        if count < len(titleList):
                                            contentSearchHtml += ', '


                                filterHtml = '<div id="contentSearch" align="left" ' + style + '>' + contentSearchHtml + '</div><br>' + filterHtml

                        if postCommand.startswith(':glucky') or postCommand.startswith(':search'):

                            cmdArgs = ''
                            if postCommand.find(' ') != -1:
                                cmdArgs = postCommand[postCommand.find(' ') : ].strip()
                                postCommand = postCommand[0 : postCommand.find(' ')]
                            line = ' | | | ' + filterDesc
                            websites = self.reflection_call('record', 'WrapRecord', 'get_tag_content', line, {'tag' : 'website:'})

                            gluckyDesc = ''
                            if websites != None:
                                for website in websites.split(','):
                                    text = self.clearHtmlTag(self.getValueOrText(website, returnType='text'))
                                    engineType = 'd:star'
                                    if cmdArgs != '':
                                        engineType = 'd:' + cmdArgs
                                    engineList = self.getEnginList(engineType)
                                    if postCommand == ':glucky':
                                        engineList = ['homepage'] + engineList
                                    for engine in engineList:
                                        icon = self.getIconHtml('',engine.replace('.', ''))
                                        if icon == '':
                                            icon = engine
                                        url = ''
                                        if postCommand == ':glucky':
                                            url = self.toQueryUrl(self.getEnginUrl('glucky'), text + ' ' + engine)
                                        else:
                                            url = self.toQueryUrl(self.getEnginUrl(engine), text)

                                        gluckyDesc +=  text + ' ' + icon + '(' + url + '), '

                            if gluckyDesc.endswith(', '):
                                gluckyDesc = gluckyDesc[0 : len(gluckyDesc) - 2]
                            filterHtml += '<br>' + self.genDescHtml('website:' + gluckyDesc, Config.course_name_len, tag.tag_list, iconKeyword=True, fontScala=1, module='searchbox', nojs=False, unfoldSearchin=False, parentOfSearchin='', cutText=False, parentOfCategory='', editMode=editMode)


                            print 'gluckyDesc:' + gluckyDesc


                                #filterHtml += '<a href="' + url + '"><font style="font-size:10pt; font-family:San Francisco;">contentSearch</font></a>'
                    #style="padding-left: 455; padding-top: 5px;"
                    if noDiv == False:
                        if showDynamicNav:
                            filterHtml = '<div id="filter_div" align="left" ' + style + '>' + filterHtml + '</div>'

                    resultHtmlList.append(filterHtml)
                elif len(descCacheList) > 1 and noFilterBox == False:
                    descList = []
                    for item in descCacheList:
                        descList.append(item[1])
                    data = subprocess.check_output('echo "' + '\n'.join(descList) + '" > web_content/desc', shell=True)
                    resultHtmlList.append(self.genFilterBox() + resultHtml)
                else:
                    resultHtmlList.append(resultHtml)
            #elif request.form.has_key('url') and request.form['url'].find(Config.ip_adress) == -1:
            #    form = self.getExtensionCommandArgs('plugin', '', request.form['url'], 'plugin', 'social', 'getPluginInfo', '')
            #    print form
            #    resultHtmlList.append(self.handleExtension(form))
        
            #else:
            #    resultHtmlList.append(self.genPluginInfo(lastOpenUrlsDict))
  

        html = ''
        if len(resultHtmlList) > 1:
            html = '<br>'.join(resultHtmlList)
        elif len(resultHtmlList) == 1:
            result = resultHtmlList[0]
            if result != '':
                html = result
            else:
    
                #html = self.genDefaultPluginInfo(title)
                html = ''

        return html


    def genChartHtml(self, desc):
        chartHtml = ''
        line = ' | | | ' + desc
        chartDesc = self.reflection_call('record', 'WrapRecord', 'get_tag_content', line, {'tag' : 'chart:'})
        print 'chartDesc:' + chartDesc
        if chartDesc != None:
            for item in chartDesc.split(','):
                if self.getValueOrTextCheck(item):
                    item = self.getValueOrText(item, returnType='value')
                chartHtml += '<div style="width: 1440px; height: 720px; margin: 0px; position: relative;"><iframe allowfullscreen frameborder="0" style="width:1400px; height:720px" src="https://www.lucidchart.com/documents/embeddedchart/' + item + '" id="sXJgXX-ZoNSN"></iframe></div>'

        return chartHtml
    def processPartPostCommand(self, postCommand, filterDesc, tagList, innerSearchWord=''):

        if postCommand.startswith(':preview'):
            column = 2
            if postCommand.find(' ') != -1:
                column = int(postCommand[postCommand.find(' ') :].strip())
            linkDict = self.genDescLinks(filterDesc, tagList, innerSearchWord=innerSearchWord)
            print 'keys:' + str(linkDict.keys())
            print 'values:' + str(linkDict.values())

            if column == 0:
                if len(linkDict) < 5:
                    column = 1
                else:
                    column = 2
                htmlList, notSuportLink = self.genAllInOnePage(linkDict.keys(), linkDict.values(), frameCheck=False, column=column, changeBG=False)
                return htmlList[0]
            else:
                url, notSuportLink = self.genAllInOnePageUrl(linkDict.keys(), linkDict.values(), 'searchbox', frameCheck=False, column=column)
                self.localOpenFile(url)
            
        if postCommand.startswith(':open'):
            print filterDesc
            linkDict = self.genDescLinks(filterDesc, tagList)
            print linkDict
            
            self.localOpenFile('" "'.join(linkDict.values()))

        return ''

    def genAllInOnePageUrl(self, textArray, urlArray, module, frameCheck=True, column=3):
        htmlList, notSuportLink = self.genAllInOnePage(textArray, urlArray, frameCheck=frameCheck, column=column)
        url = ''
        #print htmlList
        if len(htmlList) > 0:
            for html in htmlList:
                outputDir = Config.output_data_to_new_tab_path + module + '/'
                if os.path.exists(outputDir) == False:
                    os.makedirs(outputDir)
                fileName = 'onepage.html'
                cmd = "echo '" + html + "' > " + outputDir + fileName
                #print cmd
                output = subprocess.check_output(cmd, shell=True)        
                url =  Config.one_page_path_root + outputDir + fileName    
                #for k, v in notSuportLink.items():
                #    if k != Config.history_quick_access_name:
                #        utils.localOpenFile(v, fileType='.html')
        return url, notSuportLink

    def genCodeFile(self, fileName):

        field = ''
        if fileName.find('-i') != -1:
            field = fileName[fileName.find('-i') + 2 :].strip().replace('"', '').replace("'", '')
            fileName = fileName[0 : fileName.find('-i')].strip()

        print 'field:' + field
        if os.path.exists(fileName) == False:

            print 'gen code file:' + fileName

            className = fileName[fileName.rfind('/') + 1 :].replace('.py', '')

            f = open('extensions/code/code-template.py')
            template = f.read()
            f.close()

            template = template.replace('[className]', className)


            f = open(fileName, 'w')
            f.write(template)
            f.close()

            cmd = 'chmod 777 ' + fileName[fileName.find('extensions') :]

            print cmd 
            output = subprocess.check_output(cmd, shell=True) 

            print template

        return fileName

    def isCodeFile(self, fileName):

        if fileName.find('-i') != -1:
            fileName = fileName[0 : fileName.find('-i')].strip()

        return fileName.endswith('.py')

    def localOpenFile(self, fileName, fileType=''):
        cmd = 'localOpenFile "' + fileName + '"'
        app = ''
        if self.isCodeFile(fileName):
            fileName = self.genCodeFile(fileName)
        if fileType == '':
            fileType = fileName
        for k, v in Config.application_dict.items():
            if fileType.lower().strip().endswith(k):
                app = v
                break
        if app == '':
            app = Config.application_dict['*']
        if os.path.exists(app):
            cmd = app.replace(' ', '\ ') + ' "' + fileName + '"'
            print cmd
            output = subprocess.check_output(cmd, shell=True)

    def genDefaultPluginInfo(self, title):
        linkID = 'a-plugin-more-0'
        ref_divID = 'div-plugin-0'
        ref_div_style = 'style="display: none;"'
        rID = 'custom-plugin-0-pg'
        #print rID
        originTitle = title
        url = ''
        appendID = 0
        script = ''
        script = self.genMoreEnginScript(linkID, ref_divID, rID.replace(' ', '-') + '-' + str(appendID), originTitle, url, originTitle, hidenEnginSection=True)
        moreHtml = self.genMoreEnginHtml(linkID, script.replace("'", '"'), '...', ref_divID, '', False, descHtml='', content_divID_style=ref_div_style).strip();
          
        titleHtml = '<a href="javascript:void(0);"  onmouseover="lastHoveredUrl = ' + "'" + "'" + '; lastHoveredText = ' + "'" + title.strip() + "'" + ';">' + title + '</a>'
        result = '<div id="filter_div" align="left" style="padding-left: 455; padding-top: 5px;">' + titleHtml + ' ' +moreHtml + '</div>'
        return result
    
    def doExclusive(self, rID, title, url, desc):
       record = Record('custom-exclusive-' + rID + ' | '+ title + ' | ' + url + ' | ' + desc)
       return self.output2Disk([record], 'main', 'exclusive', append=Config.exclusive_append_mode) 
   
   
    
    
    def contentSearch(self, desc, filter, title='', convertableCheck=True):
    
        if filter == ':local':
            url = self.doExclusive('contentSearch-local', title, '' , desc + ' keyword:' + title + '(' + self.desc2ValueText(desc, tag.tag_list) + ')')
            return url, ''
    
        textList =[]
        convertableTitleList = []
        start = 0
        desc = desc.strip()
        tag = Tag()
        while True:
            end = self.next_pos(desc, start, 10000, tag.tag_list)
            if end < len(desc):
                text = desc[start : end].strip()
                textList.append(text)
                start = end
            else:
                text = desc[start : ]
                textList.append(text)
                break
        urlList = []
        for text in textList:
            tagStr = text[0: text.find(':') + 1].strip()
            tagValue =  text[text.find(':') + 1 : ].strip()
    
            if tagStr == 'website:':
                for v in tagValue.split(','):
                    if self.getValueOrTextCheck(v):         
                        url = self.getValueOrText(v, returnType='value')
                        if convertableCheck:
                            if self.urlConvertable(url):
                                urlList.append(url)
                                convertableTitleList.append(self.getValueOrText(v, returnType='text'))
                        else:
                            urlList.append(url)
                            convertableTitleList.append(self.getValueOrText(v, returnType='text'))
            elif self.isAccountTag(tagStr, tag.tag_list_account):
                url = tag.tag_list_account[tagStr]
                if convertableCheck:
                    if self.urlConvertable(url):
                        for v in tagValue.split(','):
                            v = v.strip()
                            title = v
                            if self.getValueOrTextCheck(v):
                                title = self.getValueOrText(v, returnType='text')
                                v = self.getValueOrText(v, returnType='value')
                            urlList.append(url.replace('%s', v))
                            convertableTitleList.append(v)
                else:
                    for v in tagValue.split(','):
                        v = v.strip()
                        title = v
                        if self.getValueOrTextCheck(v):
                            title = self.getValueOrText(v, returnType='text')
                            v = self.getValueOrText(v, returnType='value')
                        urlList.append(url.replace('%s', v))
                        convertableTitleList.append(title) 
    
         
        #line = ' | contentSearch | ' + ','.join(urlList) + ' | argv=contain=' + filter
        url = ''
        if len(urlList) > 0:
            url = self.doExclusive('', 'contentSearch', ','.join(urlList) , 'argv:contain=' + filter)
            print url
        #print line
        return url, convertableTitleList, urlList
    
    def mergerDescList(self, descList):
        desc = ''
        for line in descList:
            if desc == '':
                desc = line
            else:
                desc = self.mergerDesc(desc, line)
        return desc    

    def saveTempResult(self, title, desc, lib="xlinkbook-library", resType="keyword", editRID="custom-temp-result"):
        fName = "db/library/" + lib
        rT = title
        fd = desc
        print "saveTempResult=============" + title + ": "  + fd
        editedData = rT + '(' + self.desc2ValueText(fd, self.tag.get_tag_list(lib)) + ")"
        tempR = self.getRecord(editRID, path=fName, use_cache=False)
        newData = tempR.edit_desc_field2(self, tempR, resType, rT, editedData, self.tag.get_tag_list(lib), library=lib)

        if newData != '':
            newData = self.clearHtmlTag(newData)
            desc = newData.replace('id:' + editRID, '').replace('title:' + tempR.get_title().strip(), '').replace('url:', '').strip()
            #descValue = self.getValueOrText(desc, returnType='value')
            #desc =  resType + ":" + self.descToValueText(desc)

            newRecord = Record(editRID + ' | ' + tempR.get_title().strip() + ' |  | ' + desc)
            #newRecord = Record(editRID + ' | ' + rT + ' |  | ' + self.valueText2Desc(desc))
            result = tempR.editRecord(self, editRID, newRecord, fName, library=fName, resourceType=resType)
            return True
        return False
    
    def genFilterHtml(self, command, itemList, fontScala=0, group=True, parentCmd='', unfoldSearchin=False, cutDescText=True, highLight=True, highLightText='', onlyHighLight=False, onlyHighLightFilter='', showDynamicNav=True, style='', engine='', innerSearchWord='', gridView=False, editMode=False, parentOfSearchin='', combineResult=False):
        #print 'genFilterHtml command:' + command 
        descList = []
        tagCloud = {}
        categoryCloud = {}
        recordHistory = {}
        commandCloud = {}
        #print itemList
        tagHtml = ''
        categoryHtml = ''
        crossrefHtml = ''
        commandHtml = ''
        descHtmlList = []
        for item in itemList:
            #print item[0] + ' ' + item[1]
            descList.append(item[1])

        if combineResult:
            #descList = [', '.join(descList)]
            desc1 = ''
            desc2 = ''
            count = 0
            for desc in descList:
                if count == 0:
                    desc1 = descList[count]
                else:
                    desc2 = descList[count]

                if desc1 != '' and desc2 != '':
                    desc1 = self.mergerDesc(desc1, desc2)
                    desc2 = ''

                count += 1

            if desc1 != '':
                descList = [desc1]


        if group:
            count = 0
            descHtmCount = 0
            maxDivHeight = 0
            filterDescList = []
            descHtml = ''
            filterCache = {}
            splitChar = '<br>&nbsp;&nbsp;&nbsp;&nbsp;'
            #splitChar = '<br>'

            for desc in descList:
                #print len(descList)
                #print str(count)
                appendDesc = '' 
                title = itemList[count][0]
                if combineResult:
                    title = "Combine Result"
                    appendDesc = "command:"
                    for item in itemList:
                        appendDesc += item[0] + "(>" + item[0] + "/" + command.replace("+", "&") + "), "
                    if desc.find("command:") != -1 and desc.find(itemList[0][0] + "(>") != -1:
                        appendDesc = ''
                parentCategory = itemList[count][2]
                path = itemList[count][3]
                rID = itemList[count][4]
                #print title + ' count:' + str(count)
                parentDivID = 'filter-div-'+ title.replace(' ', '-').lower() + '-' + str(count)

                parentOfSearchin = ">" + title 
                fd, dh = self.genFilterHtmlEx(command, desc, fontScala=fontScala, splitChar=splitChar, unfoldSearchin=unfoldSearchin, cutDescText=cutDescText, addPrefix=False, highLight=highLight, highLightText=highLightText, onlyHighLight=onlyHighLight, onlyHighLightFilter=onlyHighLightFilter, parentCategory=parentCategory, parentDivID=parentDivID, engine=engine, innerSearchWord=innerSearchWord, editMode=editMode, parentOfSearchin=parentOfSearchin, title=title, appendDesc=appendDesc)
                #print 'genFilterHtmlEx<-:' + dh
                #print 'genFilterHtmlEx<-:' + fd
                if combineResult:
                    self.saveTempResult('Combine Result', fd)
                    '''
                    lib = "xlinkbook-library"
                    fName = "db/library/" + lib
                    resType = "keyword"
                    rT = 'Combine Result'
                    print "=============Combine Result: "  + fd
                    editedData = rT + '(' + self.desc2ValueText(fd, self.tag.get_tag_list(lib)) + ")"
                    editRID = "custom-temp-result"
                    tempR = self.getRecord(editRID, path=fName, use_cache=False)
                    newData = tempR.edit_desc_field2(self, tempR, resType, rT, editedData, self.tag.get_tag_list(lib), library=lib)

                    if newData != '':
                        newData = self.clearHtmlTag(newData)
                        desc = newData.replace('id:' + editRID, '').replace('title:' + tempR.get_title().strip(), '').replace('url:', '').strip()
                        #descValue = self.getValueOrText(desc, returnType='value')
                        #desc =  resType + ":" + self.descToValueText(desc)

                        newRecord = Record(editRID + ' | ' + rT + ' |  | ' + desc)
                        #newRecord = Record(editRID + ' | ' + rT + ' |  | ' + self.valueText2Desc(desc))
                        result = tempR.editRecord(self, editRID, newRecord, fName, library=fName, resourceType=resType)
                    '''
                if fd.strip() != '' and dh.strip() != '':
                    if title != '':
                        fd += ' title:' + title
                        key = title + '-' + str(len(fd))
                        if filterCache.has_key(key):
                            count += 1
                            continue
                        else:
                            filterCache[key] = fd;
                    filterDescList.append(fd.strip())
                    #for domain process
                    #titleHtml = '<li><span>' + str(count + 1) + '</span><p>'
                    onmouseover = 'onmouseover="lastHoveredUrl =' + "'>" + title + "'" + '; lastHoveredText =' + "'" + title + "'" + '; lastHoveredCMD =' + "'>" + title + "/'" + ';"'
                    titleHtml = '<a href="javascript:void(0);" style="color:#1a0dab;" onclick="' + "typeKeyword('>" + title + "','" + parentCmd + "');" + '" ' + onmouseover + '>' + title + '</a>'
                    
                    js = "showPopupContent(pageX, pageY, 550, 480, '#>" + title + "/:');"
                    titleHtml += '<a href="javascript:void(0);" onclick="' + js + '" >' + self.getIconHtml('', 'tabs', width=10, height=8) + '</a>'
                    js = "showCmdBox(pageX, pageY, 550, 480, '>" + title + "');"
                    titleHtml += '<a href="javascript:void(0);" onclick="' + js + '" >' + self.getIconHtml('', 'search', width=10, height=8) + '</a>'
                    js = "showCmdBoxEx(pageX, pageY, 550, 480, '>" + title + "', '" + parentDivID + "');"
                    titleHtml += '<a href="javascript:void(0);" onclick="' + js + '" >' + self.getIconHtml('', 'search', width=10, height=8) + '</a>'
                    titleHtml += '<a href="javascript:void(0);" onclick="' + "typeKeywordEx('>" + title + "/:" + ' ; ->' + title + '/:/:group-short ->' + title + "','" + parentCmd + "', false, '" + parentDivID + "');" + '">' + self.getIconHtml('', 'command', width=11, height=9) + '</a>'
                    line = ' | | | ' + desc
                    if desc.find('searchin:') != -1:
                        searchin = self.reflection_call('record', 'WrapRecord', 'get_tag_content', line, {'tag' : 'searchin:'})
                        searchinCMD = searchin.replace(",", "+") + "/:"
                        titleHtml += '<a href="javascript:void(0);" onclick="' + "typeKeywordEx('" + searchinCMD + "','" + parentCmd + "', false, '" + parentDivID + "');" + '">' + self.getIconHtml('', 'command', width=11, height=9) + '</a>'

                        #print "((((((((((((((((" + searchin

                    if desc.find('homepage') != -1 and fd.find('homepage') == -1:
                        start = desc.find('homepage')
                        end = desc.find(')', start)
                        homeUrl = self.getValueOrText(desc[start : end + 1], returnType='value')
                        if homeUrl != '':
                            titleHtml += '<a href="' + homeUrl + '">' + self.getIconHtml('', 'homepage', width=11, height=9) + '</a>'
                    #if desc.find('searchin:') != -1:
                        #titleHtml += '<a href="javascript:void(0);" onclick="' + "typeKeyword('>>" + title + "/" + command + "','" + parentCmd + "');" + '">' + self.getIconHtml('', 'searchin', width=11, height=9) + '</a>'

                    if desc.find('alias:') != -1:
                        
                        alias = self.reflection_call('record', 'WrapRecord', 'get_tag_content', line, {'tag' : 'alias:'})
                        if alias != None and alias != '':
                            for item in alias.split(','):
                                item = item.strip().lower()
                                if tagCloud.has_key(item):
                                    tagCloud[item] += 1
                                else:
                                    tagCloud[item] = 1
                    if desc.find('category:') != -1 and parentCategory != '':
                        category = self.reflection_call('record', 'WrapRecord', 'get_tag_content', line, {'tag' : 'category:'})
                        if category != None:
                            key = '#' + parentCategory + '->' + category + ':'
                            categoryCloud[key] = key

                    if desc.find('command:') != -1:
                        commandDesc = self.reflection_call('record', 'WrapRecord', 'get_tag_content', line, {'tag' : 'command:'})
                        if commandDesc != None and commandDesc != '':
                            for item in commandDesc.split(','):
                                item = item.strip().lower()
                                commandCloud[item] = item

                    if recordHistory.has_key(path) == False:
                        recordHistory[path] = title

                    titleHtml += '<a href="javascript:void(0);" onclick="' + "typeKeyword('%>" + title + "/" + command + "','" + parentCmd + "');" + '">' + self.getIconHtml('', 'relationship', width=11, height=9) + '</a>'
                    titleHtml += '<a href="javascript:void(0);" onclick="' + "typeKeyword('?>" + title + "/" + command + "','" + parentCmd + "');" + '">' + self.getIconHtml('', 'graph', width=11, height=9) + '</a>'

                    titleHtml += '<a href="javascript:void(0);" onclick="' + "typeKeyword('>" + title + "/:" + "','" + parentCmd + "');" + '">' + self.getIconHtml('', 'zoom', width=11, height=9) + '</a>'

                    titleHtml += '<a href="javascript:void(0);" onclick="' + "typeKeyword('>>" + title + "/:" + "','" + parentCmd + "');" + '">' + self.getIconHtml('', 'zoom-more', width=11, height=9) + '</a>'

                    #if showDynamicNav == False:
                    js = "showCmdBoxEx(pageX, pageY, 550, 480, 'r>" + title + "', '" + parentDivID + "');"
                    titleHtml += '<a href="javascript:void(0);" onclick="' + js + '" >' + self.getIconHtml('', 'search', width=10, height=8) + '</a>'
                    titleHtml += '<a href="javascript:void(0);" onclick="' + "typeKeywordEx('>" + title + "/chat ; :chat','" + parentCmd + "', false, '" + parentDivID + "');" + '">' + self.getIconHtml('', 'chat', width=11, height=9) + '</a>'
                    js = "onHoverPreview('', '', 'https://edgeservices.bing.com/edgediscover/query?&darkschemeovr=1&FORM=SHORUN&udscs=1&udsnav=1&setlang=en-US&features=udssydinternal&clientscopes=windowheader%2Ccoauthor%2Cchat%2C&udsframed=1', 'searchbox', true);"
                    titleHtml += '<a href="javascript:void(0);" onclick="' + js + '" >' + self.getIconHtml('', 'chat', width=11, height=9) + '</a>'
                    remoteCMD = ':'
                    if command != '':
                        remoteCMD = command
                    titleHtml += '<a href="javascript:void(0);" onclick="runRemoteCommandEx(' + "'>" + title + "/" + remoteCMD + "'," + "'" + parentDivID + "'" + ');" >' + self.getIconHtml('', 'command', width=11, height=9) + '</a>'
                    titleHtml += '<a href="javascript:void(0);" onclick="runRemoteCommand(' + "'>" + title + "/" + remoteCMD.replace("+", "%2B")+ "'" + ');" >' + self.getIconHtml('', 'url', width=11, height=9) + '</a>'
                    js = "$('#' + '" + parentDivID + "').remove();"
                    titleHtml += '<a href="javascript:void(0);" onclick="' + js + '">' + self.getIconHtml('', 'delete', width=11, height=9) + '</a>'


                    ref_divID = 'search-div-' + title.replace(' ', '-').lower() 
                    linkID = ref_divID + '-' + str(count) + '-more'
                    ref_divID += '-' + str(count)
                    appendID = str(count)
                    
                    #custom-plugin-CS15662-pg-realtime-rendering-1-1
                    itemID = "custom-plugin-" + rID.strip().replace(' ', '-') + '-pg-' + title.lower().replace(' ', '-') + '-' + str(count) + '-' + str(count)

                    title = path.replace('db/', '') + '==' + title
                    originTitle = title
                    script = self.genMoreEnginScript(linkID, ref_divID, itemID, title, '', originTitle, hidenEnginSection=Config.history_hiden_engin_section)
                    titleHtml += '&nbsp;' + self.genMoreEnginHtml(linkID, script.replace("'", '"'), '...', ref_divID, '', False, descHtml='', content_divID_style='style="display: none;"').strip();

                    #titleHtml += '</p></li>'
                    style = style.replace(';"', '; border-radius:10px 15px 15px 15px; height:#height;"')
 
                    if gridView:
                        descHtmlList.append('<div id="' + parentDivID + '" align="left" ' + style + ' onmouseout="normal(this);" onmouseover="hover(this);">' + titleHtml + splitChar + dh + '</div>')
                    else:
                        descHtml += '<div id="' + parentDivID + '" align="left" ' + style + ' onmouseout="normal(this);" onmouseover="hover(this);">' + titleHtml + splitChar + dh + '</div>'
                
                count += 1

            subDescHtmlList = []
            totalDivHeight = 0
            print 'descHtmlList len:' + str(len(descHtmlList))
            if gridView and len(descHtmlList) > 0:
                for html in sorted(descHtmlList):

                    descHtmCount += 1
                    divHeight = self.getDivHeight(self.clearHtmlTag(html), self.getBrCount(html), '') 
                    if divHeight > maxDivHeight:
                        maxDivHeight = divHeight
                    print descHtmCount
                    if descHtmCount == 3:
                        subDescHtmlList.append(html)
                        for html in subDescHtmlList:
                            descHtml += html.replace('#height', str(maxDivHeight + 20) + 'px')
                        totalDivHeight += maxDivHeight + 20
                        subDescHtmlList = []
                        descHtmCount = 0
                        maxDivHeight = 0

                    else:
                        subDescHtmlList.append(html)
                if len(subDescHtmlList) > 0:
                    totalDivHeight += maxDivHeight + 20
                    for html in subDescHtmlList:   
                        descHtml += html.replace('#height', str(maxDivHeight + 20) + 'px')

            if descHtml != '':

                if showDynamicNav:
                    tagDesc = ''
                    categoryDesc = ''
                    crossrefDesc = ''
                    commandDesc = ''
                    for item in tagCloud.items():
                        tagDesc += item[0] + ', '
                    for item in categoryCloud.items():
                        categoryDesc += item[0] + ', '
    
                    for item in commandCloud.items():
                        commandDesc += item[0] + ', '
    
                    for item in recordHistory.items():
                        crossrefDesc += item[0].replace('db/', '') + ', '
    
                    if tagDesc != '':
                        tagHtml = self.genSubDescHtml(tagDesc, 'alias:', editMode=editMode)
                    if categoryDesc != '':
                        categoryHtml = self.genSubDescHtml(categoryDesc, 'category:', editMode=editMode)
                    if crossrefDesc != '':
                        crossrefHtml = self.genSubDescHtml(crossrefDesc, 'crossref:', editMode=editMode)
                    if commandDesc != '':
                        commandHtml = self.genSubDescHtml(commandDesc, 'command:', editMode=editMode)
    
                    descHtml = descHtml + '<br>' + crossrefHtml + categoryHtml + tagHtml + commandHtml
                    #print filterDescList

                return filterDescList, self.clearHtmlTag(self.mergerDescList(filterDescList)), descHtml

        else:

            desc = self.mergerDescList(descList)
            fd, dh = self.genFilterHtmlEx(command, desc, fontScala=fontScala, splitChar='<br>', cutDescText=cutDescText, highLight=highLight, highLightText=highLightText, onlyHighLight=onlyHighLight, onlyHighLightFilter=onlyHighLightFilter, editMode=editMode)
            self.saveTempResult('Merger Result', fd)
    
            return [], self.clearHtmlTag(fd), dh
        return [], '', ''

    def genSubDescHtml(self, subDesc, tagStr, editMode=False):
        subDescHtml = ''
        subDesc = subDesc.strip()
        if subDesc.endswith(','):
            subDesc = subDesc[0 : len(subDesc) - 1]
        if subDesc != '':
            subDescHtml = self.genDescHtml(tagStr + subDesc, Config.course_name_len, self.tag.tag_list, iconKeyword=True, fontScala=1, module='searchbox', nojs=True, unfoldSearchin=False, parentOfSearchin='', cutText=False, editMode=editMode)

        return subDescHtml

    def genFilterHtmlEx(self, command, desc, fontScala=0, splitChar='', unfoldSearchin=False, cutDescText=True, addPrefix=True, prefixText='', highLight=True, highLightText='', onlyHighLight=False, onlyHighLightFilter='', parentCategory='', parentDivID='', engine='', innerSearchWord='', editMode=False, parentOfSearchin='', title='', appendDesc=''):
        filterDesc = ''
        tag = Tag()
        #print 'genFilterHtmlEx:' + command

        if command != '':
            start = 0
            loop = True
            if command == ':':
                filterDesc = desc
                #print 'filterDesc:' + filterDesc
                loop = False
            found = False
            while loop:
                end = self.next_pos(desc, start, 10000, tag.tag_list)
                if end < len(desc):
                    text = desc[start : end].strip()
                    result = self.doFilter(command.split('+'), text, addPrefix=addPrefix, highLight=highLight, highLightText=highLightText, onlyHighLight=onlyHighLight, onlyHighLightFilter=onlyHighLightFilter).strip()
                    if result != '' and result.startswith('searchin:') == False:
                        found = True
                    if result != '' and found:
                        filterDesc +=  result + ' '
                    start = end
                else:
                    text = desc[start : ]
                    result = self.doFilter(command.split('+'), text, addPrefix=addPrefix, highLight=highLight, highLightText=highLightText, onlyHighLight=onlyHighLight, onlyHighLightFilter=onlyHighLightFilter).strip()
                    if result != '' and found:
                        filterDesc += result + ' '
    
                    break
            #print 'genFilterHtmlEx filterDesc:' + filterDesc
            if highLightText.find("+") != -1:
                 print "+++++++++++ highLightText:" + highLightText
                 htList = []
                 for text in highLightText.split("+"):
                     text = text.strip()
                     if text.find(":") != -1:
                         text = text[text.find(":") + 1 :]
                     if text != "":
                         htList.append(text)
                 if len(htList) > 0:
                     highLightText = "+".join(htList)
                 else:
                     highLightText = ""
            #    highLightText = ""
            if filterDesc != '':
                filterDesc = filterDesc.strip()
                if appendDesc != '':
                    filterDesc += ", " + appendDesc
                #print 'filterDesc:' + filterDesc
                descHtml = self.genDescHtml(filterDesc, Config.course_name_len, tag.tag_list, iconKeyword=True, fontScala=fontScala, module='searchbox', previewLink=True, splitChar=splitChar, unfoldSearchin=unfoldSearchin, field=command, cutText=cutDescText, parentOfCategory=parentCategory, parentDivID=parentDivID, engine=engine, innerSearchWord=innerSearchWord, editMode=editMode, parentOfSearchin=parentOfSearchin, title=title, highLightText=highLightText)
    
                if descHtml == splitChar:
                    descHtml = ''
                return filterDesc, descHtml
        return '', ''


    def doHighLight(self, text, highLightText, appendValue=True):
        replaceStr = '<i><strong>' + highLightText.lower() + '</strong></i>'
        highLightItem = ''
        if self.getValueOrTextCheck(text):
            itemText = self.getValueOrText(text, returnType='text')
            itemValue = self.getValueOrText(text, returnType='value')
            highLightItem = self.replaceEx(itemText, highLightText, replaceStr) + '(' + itemValue + ')'
        else:

            highLightItem = self.replaceEx(text, highLightText, replaceStr)
            if appendValue:
                highLightItem += '(' + text + ')'
        return highLightItem


    def doFilter(self, commandList, text, highLight=True, addPrefix=True, highLightText='', onlyHighLight=False, onlyHighLightFilter='', includeSearchin=False):
        if includeSearchin and text.startswith("searchin:"):
            return text
        text = text.strip()
        tagStr = text[0: text.find(':') + 1].strip()
        tagValue =  text[text.find(':') + 1 : ].strip()

        isAccountTag = False
        if self.isAccountTag(tagStr, self.tag.tag_list_account):
            isAccountTag = True
        desc = ''
        desc2 = ''
        print 'doFilter start:' + text
        print "commandList:"
        print commandList
        print "tagStr:" + tagStr
        print 'highLightText:' + highLightText
        
        if len(commandList) == 1:
            # youtube: -> youtube: y-playlist: y-video:
            if commandList[0].startswith("youtube:"):
                keyword = commandList[0][commandList[0].find(":") + 1 :]
                commandList.append("y-playlist:" + keyword)
                commandList.append("y-video:" + keyword)
            print "commandList:"
            print commandList

        processedCommand = {}

        for command in commandList:
            command = command.strip()
            if command.find(':') != -1:

                print "command1111:" + command

                if command == ':all':
                    return text
               

                if command.endswith(':') and command.strip() == tagStr:
                    processedCommand[command] = command

                    result = text
                    #print "1111111"
                    if highLight:
                        print 'highLightText:' + highLightText
                        #print "====text:" + text
                        if isAccountTag and highLightText != '':
                            result = ''
                            
                            text = text[text.find(':') + 1 :]
                            count = 0
                            items = text.split(',')
                            for item in items:
                                item = item.strip()
                                count += 1

                                print 'before:' + item
                                if onlyHighLight:
                                    if item.lower().find(highLightText.lower()) == -1:
                                        continue
                                    if onlyHighLightFilter != '' and item.lower().find(onlyHighLightFilter.lower()) == -1:
                                        continue
                                highLightItem = self.doHighLight(item, highLightText)
                                print 'after:' + highLightItem
                                result += highLightItem 
                                #if addPrefix:
                                #    result += text
                                if count != len(items):
                                    result += ', '
                            result = result.strip()
                            if result.endswith(','):
                                result = result[0 : len(result) - 1]
                            if result != '':
                                return tagStr + result.strip()

                    return result
                elif command[0 : command.find(':') + 1] == tagStr or command.startswith(':'):

                    processedCommand[command] = command

                    desc = tagStr.strip()

                    filter = ''
                    print command

                    name = ''
                    urls = []
                    originCommand = command.strip()


                    if command.startswith(':'):
                        filter = command[ 1 :]
                    else:
                        filter = command[command.find(':') + 1 :]

                    ftList = filter.split('*')
                    print ftList
                    #print "tagValue:" + tagValue


                    for tagItem in tagValue.split(','):
                        tagItem = tagItem.strip()
                        if originCommand.startswith("website:"):
                            #print "----------------------" + tagItem
                            name = self.getValueOrText(tagItem, returnType='text')
                            urls = self.getValueOrText(tagItem, returnType='value').split("*")
                            if name != '' and len(urls) > 0:
                                newUrls = []
                                for url in urls:
                                    for ft in ftList:
                                        ft = ft.strip()
                                        if url.find(ft) != -1:
                                            newUrls.append(url)
                                #print newUrls
                                if len(newUrls) > 0:
                                    tagItem = name + "(" + "*".join(newUrls) + ")"
                                    #print tagItem
                                    if highLight and highLightText != '':
                                        tagItem = self.doHighLight(tagItem, highLightText)
                                    desc += tagItem + ', '
                        else:

                            for ft in ftList:
                                ft = ft.strip()
                                print tagItem
                                print "ft:" + ft
                                if tagItem.lower().find(ft.lower()) != -1:
                                    if highLightText.lower().strip() != ft.lower().strip():
                                        highLightText = ft
                                    if highLight and highLightText != '' and (isAccountTag or tagStr == "website:"):
                                        tagItem = self.doHighLight(tagItem, highLightText)
                                    desc += tagItem + ', '
                    #print '  @@@'
                    #print desc
                    #print desc[0 : len(desc) - 2]
                    if desc != '':
                        if tagStr == desc:
                            return ''
                        return desc[0 : len(desc) - 2]
                elif len(commandList) > 0 and tagStr == "website:" and  self.isAccountTag(command[0 : command.find(':') + 1], self.tag.tag_list_account):
                    processedCommand[command] = command


                    #print "**********************" + command
                    newTagStr = command[0 : command.find(':') + 1]
                    newTagStr2 = ''
                    if newTagStr == commandList[0].strip():
                        desc2 = newTagStr
                    elif desc2 != "":
                        desc2 += " "
                        newTagStr2 = newTagStr

                    if newTagStr2 == "" and newTagStr != "website:":
                        newTagStr2 = newTagStr

                        #print "desc***************************:" + desc


                    filter = ''
                    #print "!!!!!!!!!!:" + command
                    if command.startswith(':'):
                        filter = command[ 1 :]
                    else:
                        filter = command[command.find(':') + 1 :]
                    ftList = filter.split('*')
                    descTemp = ''

                    for tagItem in tagValue.split(','):
                        urls = self.getValueOrText(tagItem, returnType='value').split("*")
                        #print "urls:" + str(urls)
                        for url in urls:
                            newUrl = ''
                            if newTagStr == "github:" and url.find("github.com") != -1:
                                newUrl = url[url.find("/", url.find("//") + 2) + 1 :].strip()
                                if filter.find("issues") == -1 and (newUrl == "" or newUrl.find("/") == -1 or newUrl.find("%") != -1 or newUrl.find("?") != -1):
                                    newUrl = ''
                                    continue
                                if newUrl.endswith("/"):
                                    newUrl = newUrl[0 : len(newUrl) - 1]
                            elif newTagStr == "twitter:" and url.find("twitter.com") != -1:
                                newUrl = url[url.find("/", url.find("//") + 2) + 1 :].strip()
                            elif newTagStr == "telegram:" and url.find("t.me") != -1:
                                newUrl = url[url.rfind("/") + 1 :].strip()

                            if newUrl != '':
                                #print "++++++++++++newUrl:" + newUrl
                                for ft in ftList:
                                    ft = ft.strip()
                                    if ft != "":
                                        if newUrl.lower().find(ft.lower()) != -1:
                                            #print "match:" + newUrl + " ft:" + ft
                                            descTemp += newUrl + ", "
                                    else:
                                        descTemp += newUrl + ", "
                    if descTemp != '':
                        if newTagStr2 != '':
                            #print "================"
                            #print filter
                            #print "================"
                            if filter != '':
                                desc2 = desc2 + newTagStr2 + descTemp
                            else:
                                desc2 = desc2  + descTemp
                        else:
                            desc2 += descTemp

                    #print "++++++++++++:" + desc
                    if desc2 != '':
                        if len(commandList) > 1 and self.isLastAccountTag(commandList, newTagStr) == False:
                            continue
                        elif len(commandList) == 1:
                            if newTagStr == desc2:
                                return ''
                            return desc2[0 : len(desc2) - 2]

        if len(processedCommand) != len(commandList):
             
            print "command2222:" + command

            for item in tagValue.split(','):
                item = item.strip()
                originItem = item


                for command in commandList:
                    command = command.strip()

                    #if processedCommand.has_key(command) and tagStr == "website:":
                    #    continue

                    if command.startswith('>'):
                        command = command[1:]
                        item = self.getValueOrText(item, returnType='text')

                    processedCommand[command] = command
                    if item.lower().find(command.lower()) != -1:
                        print "===========command333:" + command
                        print "highLightText:" + highLightText
                        print "item:" + item

                        if highLightText.find("+") != -1:
                            highLight = False
                            highLightText = command

                        prefix = ''
                        highLightItem = originItem
                        replaceStr = ''
                        if highLightText != '' and command == highLightText:
                            replaceStr = '<i><strong>' + highLightText.lower() + '</strong></i>'
                        else:
                            replaceStr = '<i><strong>' + command.lower() + '</strong></i>'

                        
                        if self.getValueOrTextCheck(originItem):
                            urlText = self.getValueOrText(originItem, returnType='text')
                            url = self.getValueOrText(originItem, returnType='value')
                            if addPrefix and tagStr == 'website:':
                                if len(urlText.split(' ')) < 3 and url.find(Config.ip_adress) == -1:
                                    urlTemp = url.replace('https://', '').replace('http://', '').replace('www.', '')
                                    prefix = urlTemp[0 : urlTemp.find('.')]
                            if highLight:
                                prefix = self.replaceEx(prefix, command, replaceStr)
                                highLightItem = self.replaceEx(urlText, command, replaceStr) + '(' + url + ')'
                        else:
                            if highLight and isAccountTag:
                                highLightItem = self.replaceEx(originItem, command, replaceStr) + '(' + originItem + ')'

                        if addPrefix and prefix != '' and originItem.lower().startswith(prefix.lower()) == False:
                            desc += prefix + ' - ' + highLightItem + ', '
                        else:
                            desc += highLightItem + ', '
                        break    


        #print 'doFilter command:' + str(commandList) + ' desc:' + desc
        #print 'doFilter end:' + desc
        if desc != '':
            desc = desc.strip()
            if desc.endswith(','):
                desc = desc[0 : len(desc) - 1]
            return tagStr + desc + " " + desc2
        else:
            return ''

    def isLastAccountTag(self, cmdList, tag):

        for i in range(len(cmdList) - 1, -1, -1):
            item = cmdList[i].strip()

            if item == tag:
                return True
        return False
    
    def genFilterBox(self):
        command = ''
        script = "var text = $('#command_txt'); console.log('', text[0].value);"
        divID = 'filter_div'
        script += "var dataDiv = $('#" + divID + "'); dataDiv.html('');"
        script += "var postArgs = {command : text[0].value, divID : '" + divID + "'};";
        script += "$.post('/filter', postArgs, function(data) { \
                            var div = document.getElementById('filter_div');\
                            div.innerHTML = data;\
                        });"
        box = '<br><div style="text-align:center;width:100%;margin: 0px auto;"><input id="command_txt" style="border-radius:5px;border:1px solid" maxlength="256" tabindex="1" size="46" name="word" autocomplete="off" type="text" value="' + command + '">&nbsp;&nbsp;'\
              '&nbsp;&nbsp;<button alog-action="g-search-anwser" type="submit" id="command_btn" hidefocus="true" tabindex="2" onClick="' + script + '">Run</button></div><div id="filter_div" align="left" style="padding-left: 455; padding-top: 5px;"></div>'
        return box
    
    def genPluginInfo(self, dataDict, returnDict=False):
        html = ''
        lens = 0
        linkDict = {}
        for k, v in dataDict.items():
            lens += len(k)
            onmouseover = 'onmouseover="' + "lastHoveredUrl = '" + v + "'; lastHoveredText = '" + k + "';" + '"'
            link = '<a target="_blank" href="' + v + '" style="font-family:San Francisco;" ' + onmouseover + '><font style="font-size:9pt; font-family:San Francisco;">' + k + '</font></a>'
            icon = self.getIconHtml(v)
            if returnDict:
                linkDict[k] = link + icon
            else:
                html += link + icon + '  '
            if lens > 70:
                lens = 0
                html += '<br>'
        if returnDict:
            return linkDict
        else:
            return html   
    

    def enhancedLink(self, url, text, aid='', refreshID='', style=Config.smart_link_style, script='', showText='', originText='', useQuote=False, module='', library='', img='', rid='', field='', haveDesc=True, newTab=True, searchText='', resourceType='', urlFromServer=False, dialogMode=False, ignoreUrl=False, fileName='', dialogPlacement='top', isTag=False, log=True, nojs=False):

        #print text
        url = url.strip()
        user_log_js = ''
        query_url_js = ''
        chanage_color_js = ''
        rid = rid.strip()
        text = text.replace('"', '').replace("'", '')
        #text = self.clearHtmlTag(text).replace('\n', '')

        if originText == '':
            originText = text
        if fileName == '':
            fileName = library

        if refreshID == '':
            refreshID = aid;

        newTabArg = 'false'
        haveDescArg = 'true'
        if newTab:
            newTabArg = 'true'
        if haveDesc == False:
            haveDescArg = 'false'
        #if originText.find('(') != -1:
        #    print originText
        #    print 'dialogMode:' + str(dialogMode)

        send_text = self.clearHtmlTag(originText).replace('\n', ' ')
        if send_text.find('<') != -1:
            send_text = self.clearHtmlTag(send_text)
        if searchText == '':
            searchText = send_text.strip()

        newTabArgs = 'false'
        isTagArgs = 'false'
        islog = 'true'
        if newTab:
            newTabArgs = 'true'
        if isTag:
            isTagArgs = 'true'

        if log == False:
            islog = 'false'
        if module != '' and ' '.join(Config.igon_log_for_modules).find(module) != -1:
            log = False
        if useQuote:
            # because array.push('') contain ', list.py will replace "'" to ""
            # so use  #quote as ', in appendContent wiil replace #quote back to '
            if log:
                user_log_js = "if (opened) { userlogEx(#quote" + aid+ "#quote,#quote" + refreshID + "#quote,#quote" + send_text + "#quote,#quote" + url + "#quote,#quote" + module + "#quote,#quote" + library + "#quote, #quote" + rid + "#quote, #quote" + searchText+ "#quote, #quote" + resourceType + "#quote);}"

            query_url_js = "queryUrlFromServer(#quote" + send_text + "#quote,#quote" + url + "#quote,#quote" + module + "#quote,#quote" + library + "#quote, #quote" + rid + "#quote, #quote" + searchText+ "#quote, " + newTabArgs + ", " + isTagArgs+ ", #quote" + fileName + "#quote," + islog + ");"
            if Config.background_after_click != '' and text.find('path-') == -1:
                chanage_color_js = "chanageLinkColor(this, #quote"+ Config.background_after_click +"#quote, #quote" + Config.fontsize_after_click + "#quote, #quote" + resourceType + "#quote);"

        else:
            if log:
                user_log_js = "if (opened) { userlogEx('" + aid + "','" + refreshID + "','"+ send_text + "','" + url + "','" + module + "','" + library + "', '" + rid + "', '" + searchText + "', '" + resourceType + "');}"
            query_url_js = "queryUrlFromServer('" + send_text + "','" + url + "','" + module + "','" + library + "', '" + rid + "', '" + searchText + "', '" + resourceType + "', " + newTabArgs + ", " + isTagArgs + ", '" + fileName + "'," + islog +");"
            if Config.background_after_click != '' and text.find('path-') == -1:
                chanage_color_js = "chanageLinkColor(this, '" + Config.background_after_click + "', '" + Config.fontsize_after_click + "');"

        open_js = 'var opened = true; '
        onHover_js = ''

        if url.startswith('http') == False and url != '':
            #js = "$.post('/exec', {command : 'open', fileName : '" + url + "'}, function(data){});"
            cmd = 'open'
            if url.endswith('.md'):
                cmd = 'edit'

            js = "exec('" + cmd + "','" + searchText + "','" + url + "');"
            onHover_js = "onHover('" + aid + "', '" + searchText + "', '" + url + "', '" + rid + "', '" + module + "', '" + fileName+ "', '" + haveDescArg + "');"

            link = '<a href="javascript:void(0);" onclick="' + js + chanage_color_js + open_js + user_log_js + '" onmouseover="' + onHover_js + '"'

            if style != '':
                link += ' style="' + style + '"'
                link +='>'
            if showText != '':
                link += showText + '</a>'
            else:
                link += text + '</a>'
            return link


        if ignoreUrl == False:
            if urlFromServer:
                user_log_js = ''
                open_js = query_url_js;
            else:
                urls = [url]    
                if (module != '' or resourceType != '') and url == '':
                    resultDict = self.clientQueryEnginUrl(url, searchText, resourceType, module)
                    if resultDict != None and len(resultDict) > 0:
                        urls = resultDict.values()
                for link in urls:
                    if link == '':
                        continue

                    if field != '':
                        searchText = field + ' - ' + searchText
                    if searchText.find(' + ') != -1:
                        if searchText.find(' - ') != -1:
                            searchText = searchText[searchText.find(' - ') + 3 :].strip()
                        else:
                            searchText = ""
                    if useQuote:
                        open_js += "opened = openUrl(#quote" + link + "#quote, #quote" + searchText + "#quote, " + newTabArg + ", " + newTabArg + ", #quote" + rid + "#quote, #quote" + resourceType + "#quote, #quote" + refreshID + "#quote, #quote" + module + "#quote, #quote" + fileName + "#quote);"
                        onHover_js+= "onHover(#quote" + aid + "#quote, #quote" + searchText + "#quote, #quote" + link + "#quote, #quote" + rid + "#quote, #quote" + module + "#quote, #quote" + fileName+ "#quote, #quote" + haveDescArg + "#quote);"
                    else:
                        open_js += "opened = openUrl('" + link + "', '" + searchText + "', " + newTabArg + ", " + newTabArg + ", '" + rid + "', '" + resourceType + "', '" + refreshID + "', '" + module + "', '" + fileName + "');"
                        onHover_js+= "onHover('" + aid + "', '" + searchText + "', '" + link + "', '" + rid + "', '" + module + "', '" + fileName+ "', '" + haveDescArg + "');"

                    if newTab == False:
                        break
        #open_js = ''
 
        result = ''
        
        if dialogMode:
            result = '<a href="#" class="bind_hover_card" data-toggle="popover" data-placement="' + dialogPlacement + '" data-trigger="hover" data-popover-content="' + rid + '#' + resourceType + '#' + aid + '#' + str(isTag) + '#' + originText + '" id="' + aid + '"' 
            if style != '':
                result += ' style="' + style + '"'
            result +='>'
        else:
            result = ''
            if nojs:
                result = '<a href="' + url + '"'

            else:
                result = '<a href="javascript:void(0);"'


                if aid != '' and aid.endswith('-') == False:
                    result += ' id=' + aid 
    
                if script != '':
                    script = script.replace('"', "'")
                    if useQuote:
                        script = script.replace("'", '#quote')
                    result += ' onclick="' + script + open_js + chanage_color_js + user_log_js + '"'
                else:
                    result += ' onclick="' + open_js + chanage_color_js + user_log_js + '"'
    
                if onHover_js != '' and aid != '':
                    result += ' onmouseover="' + onHover_js + '"'
    

            if style != '':
                result += ' style="' + style + '"'

            result += '>' 

        if img != '':
            result += img + '</a>'
        else:
            if showText != '':
                #print showText.encode('utf-8')
                #print result.encode('utf-8')
                result += showText
            else:
                result += originText#text
            result += '</a>'

        return result


    def toSmartLink(self, text, br_number=Config.smart_link_br_len, engin='', noFormat=False, showText='', module='', library='', rid='', resourceType='', aid=''):
        if text != '':
            url = ''
            if engin != '':
                url = self.toQueryUrl(self.getEnginUrl(engin.strip()), text)
            else:
                url = self.bestMatchEnginUrl(text, resourceType=resourceType)
            if noFormat:
                return self.enhancedLink(url, text, showText=showText, module=module, library=library, rid=rid, resourceType=resourceType, aid=aid)
            else:
                return self.enhancedLink(url, self.formatTitle(text, br_number), showText=showText, module=module, library=library, rid=rid, resourceType=resourceType, aid=aid)
        return text

    def formatTitle(self, title, br_number=Config.smart_link_br_len, keywords=[]):
        if title.find(': Amazon.com: Books') != -1:
            title = title.replace(': Amazon.com: Books', '')
            title = title[0 : title.rfind(':')]

        if len(title) > br_number:
            at = title.find(' ', br_number)
            if at != -1:
                return self.replaceKeyword(title[0 : at], keywords) + '<br>' + self.formatTitle(title[at:], br_number)
            else:
                return self.replaceKeyword(title, keywords)
        else:
            return self.replaceKeyword(title, keywords)

    def replaceKeyword(self, text, keywords=[]):
        if len(keywords) == 0:
            return text
        for kw in keywords:
            if text.find(kw.strip()) != -1:
                colorText = '<font color="red">' + kw.strip() + '</font>'
                return text.replace(kw, colorText)
        return text

    def priority2fontsize(self, engin, priority, baseFontSize):
        if priority.strip() == '':
            return baseFontSize
        if priority.strip() == '0':
            rank = int(self.getAlexaRank(engin))
            if rank == 0:
                return baseFontSize
            fontSize = int(self.revertRount((500 -rank) / 50.0 )) + 1
            #print 'rank:' + str(rank) + ' engin:' + engin + ' fontsize:' + str(fontSize)
            #print '<br/>'
            return baseFontSize + fontSize + 1
            
        else:
            priorityInt = int(priority.strip())
            return baseFontSize + priorityInt + 1
        
    def revertRount(self, number):
        if number > round(number):
            return round(number) + 1
        else:
            return round(number)
             
    def getNavLinkList(self, engin, searchEnginOnly=False):
        if self.ddg_mode:
            if len(self.ddg_search_engin_type) == 0 or len(self.ddg_search_engin_dict) == 0:
                self.loadDDGEngins()
            return self.ddg_search_engin_type
        else:
            if Config.extension_mode:
                return self.engin_extension
            else:
                if searchEnginOnly:
                    return self.search_engin_type
                else:
                    return self.search_engin_type + self.engin_extension
        #return ['paper', 'book', 'project', 'course', 'talk', 'organization', 'people', 'social']

    def getEnginTypes(self):
        return self.search_engin_type

    def getEnginExtensions(self):
        return self.engin_extension

    def getLastEnginType(self):
        return self.search_engin_type[len(self.search_engin_type) - 1]

    def genMoreEnginHtml(self, aid, script, text, content_divID, color='', doubleQ=True, descHtml='', descMarginTop=13, content_divID_style=''):
        #return ' <a id="' + aid +'" href="' + 'javascript:void(0);' + '" onClick="' + script + ';"> <font size="2" color="#999966">more</font></a>'
        div = '<div id="' + content_divID + '" ' + content_divID_style + '></div>';
        html = ''
        desc_divID = aid + '-desc'
        if descHtml != '':
            script += "hidendiv_3('" + desc_divID + "');"
        if color != '':
            if doubleQ:
                html = ' <font size="2"><a id="' + aid +'" href="' + 'javascript:void(0);' + '" onClick="' + script + '"><font color="' + color + '">' + text + '</font></a></font>'
            else:
                html = ' <font size="2"><a id="' + aid +'" href="' + 'javascript:void(0);' + '" onClick=' + script + '><font color="' + color + '">' + text + '</font></a></font>'
        else:
            if doubleQ:
                html = ' <font size="2"><a id="' + aid +'" href="' + 'javascript:void(0);' + '" onClick="' + script + '"><font color="#999966">' + text + '</font></a></font>'
            else:
                html = ' <font size="2"><a id="' + aid +'" href="' + 'javascript:void(0);' + '" onClick=' + script + '><font color="#999966">' + text + '</font></a></font>'
            html = html + div
        if descHtml != '':
            html += '<div id="' + desc_divID + '" style="display: none;margin-top:' + str(descMarginTop) + 'px;">' + descHtml + '</div>'
        return html

    def genMoreEnginScript(sefl, linkID, content_divID, id, title, url, info, hidenEnginSection=False):
        script = ''
        script += "setText('" + linkID +"');"
        script += "showdiv('" + content_divID + "','" + linkID +"');"
        title = title.replace('"', '%20').replace("'",'%20').replace('&', '%20').replace(' ', '%20')
        info = info.replace('"', '%20').replace("'",'%20').replace(' ', '%20')
        hidenEngin = 'false'
        if hidenEnginSection:
            hidenEngin = 'true'
        script += "appendContent('" + content_divID + "','" + id + "','" + title.strip().replace(" ", '%20') + "','" + url.strip().replace(" ", '%20') + "','" + info + "'," + hidenEngin + ");"
        return script

    def genMoreEnginScriptBox(sefl, linkID, content_divID, boxid):
        script = ''
        script += "setText('" + linkID +"');"
        script += "showdiv('" + content_divID + "', '" + linkID +"');"
        script += "appendContentBox('" + content_divID + "', '" + boxid + "');"
        return script

    def genLinkWithScript2(self, script, text, color='', fontSize=12, aid=''):
        #return ' <a id="' + aid +'" href="' + 'javascript:void(0);' + '" onClick="' + script + ';"> <font size="2" color="#999966">more</font></a>'
        atag = " <a "
        if aid != '':
            atag += ' id="' + aid + '" '
        if color != '':
            return atag + 'href="' + 'javascript:void(0);' + '" onClick=' + script + ' style="color:' + color + ' ; font-size: ' + str(fontSize) + 'pt;">' + text + '</a>'
        else:
            return atag + 'href="' + 'javascript:void(0);' + '" onClick=' + script + ' style="color: rgb(136, 136, 136);" font-size: ' + str(fontSize) + 'pt;>' + text + '</a>'

    def searchByID(self, engin):
        if engin.strip() == 'textbooksearch':
            return True
        return False

    def isEnginUrl(self, url):
        if url.find('soku.com') != -1 or url.find('google.com.hk/videohp') != -1:
            return True

        records = self.search_engin_dict.keys()
        if self.ddg_mode:
            records = self.ddg_search_engin_dict.keys()

        for key in records:
            if url.find(key) != -1:
                return True
        return False

    def getUrl(self, keyword, use_subject='', engin=''):
        urls = []
        url = ""
        subject = default_subject;
        if use_subject != "":
            subject = use_subject
        print 'searching %s'%keyword + " in " + subject

        for file_name in self.find_file_by_pattern(".*", self.getPath(subject)):
            f = open(file_name)
            for line in f.readlines():
                record = Record(line)
                if record.get_id().lower().strip() == keyword.lower().strip():
                    print "found " + record.get_id() + ' ' + record.get_title() + ' ' + record.get_url() + ' in ' + self.shortFileName(file_name)
                    title = record.get_title().strip()
                    if engin != "" and self.validEngin(engin) == True:
                        urls.append(self.getEnginUrl(engin.lower()) + title)
                    else:
                        urls.append(record.get_url().strip())

            f.close()


        if len(urls) > 1:
            for u in urls:
                if self.isEnginUrl(u) == False:
                    url = u
                    break
                if url == "":
                    url = urls[0]
        elif len(urls) == 1:
            url = urls[0]
        else:
            print "no url found in " + subject +" db"

        return url


    def toDescDict(self, desc, library):
        descDict = {}
        start = 0
        keywordList = self.tag.get_tag_list(library)
        while True:
            end = self.next_pos(desc, start, 10000, keywordList)
            if end < len(desc):

                item = desc[start : end].strip()
                if item.find(':') != -1:
                    descDict[item[0 : item.find(':')]] = item[item.find(':') + 1 :]

                start = end
            else:
                item = desc[start : ].strip()
                if item.find(':') != -1:
                    descDict[item[0 : item.find(':')]] = item[item.find(':') + 1 :]

                break

        #for k, v in descDict.items():
        #    print k + ':' + v

        return descDict

    def mergerDescDict(self, descDict1, descDict2):
        reslut = {}

        keySet1 = descDict1.keys()
        keySet2 = descDict2.keys()
        keySet = keySet1 + keySet2

        for k in keySet:
            if k == 'clickcount':
                continue
            if descDict1.has_key(k) and descDict2.has_key(k):
                desc1 = descDict1[k].encode('utf-8')
                desc2 = descDict2[k].encode('utf-8')

                desc1List = []

                descList = []

                if desc1.find(',') != -1:
                    desc1List = desc1.split(',')
                else:
                    desc1List = [desc1]

                for item in desc1List:
                    item = item.strip()

                    if item == '':
                        continue

                    if desc2.find(item) != -1:
                        continue
                    else:
                        descList.append(item)

                if len(descList) > 0:
                    desc1 = ', '.join(descList)
                    desc = desc1 + ', ' + desc2
                else:
                    desc = desc2

                reslut[k] = desc
            elif descDict1.has_key(k):
                reslut[k] = descDict1[k]
            else:
                reslut[k] = descDict2[k]

        return reslut

    def dict2Desc(self, descDict):
        desc = ''
        for k, v in descDict.items():
            desc += k + ':' + v.strip() + ' '

        return desc

    def getBatchOpenScript(self, textList, linkList, module, onePage=True):
        script = ''
        if Config.open_all_link_in_one_page and onePage:
            script = "openAllOnePage('" + ','.join(textList) + "', '" + ','.join(linkList) + "', '" + module + "');"
        else:
            script = "openAll('" + ','.join(textList) + "', '" + ','.join(linkList) + "');" 

        return script


    def getQuickAccessHistoryFileName(self):
        return 'extensions/history/data/' + Config.history_quick_access_name.lower().replace(' ', '-')+ '-history'

    def queryQuickAccess(self, rid):
        fileName = self.getQuickAccessHistoryFileName()

        if os.path.exists(fileName):
            #print 'queryQuickAccess:' + rid + ' '+ fileName

            r = self.getRecord(rid, path=fileName, use_cache=False)
            return r

        return None

    def queryAllTags(self, rid, fileName):
        r = self.getRecord(rid, path=fileName, use_cache=False)

        if r != None:
            line = rid + ' -all-tags | All Tags | http://nothing | clickcount:999'
            allTagsRecord = Record(line)

            return allTagsRecord

        return None

    def genAllInOnePage(self, textArray, urlArray, frameWidth=470, frameHeight=700, frameCheck=True, changeBG=True, column=3, hindenLinks=False):
        html = ''
        suportLinkHtml = ''
        notSuportLinkHtml = ''
        suportLink = {}
        notSuportLink = {}
        url = ''
        style = ''
        if changeBG:
            style = '<style>body {width:100%; background-color:#E6E6FA;}</style>'
        head = '<html><head>' + style + '</head><body><table>'
        end = '</body></html>'
        count = 0
        if frameWidth == 470:

            if column == 1 or len(urlArray) == 1:
                frameWidth *= 3
            elif column == 2 or len(urlArray) == 2:
                frameWidth += 230
            
            if column >= 2 and len(urlArray) > 5:
                frameHeight = frameHeight / 2

        for i in range(0, len(urlArray)):
            itemText = textArray[i].replace('%20', ' ').strip()
            if self.getValueOrTextCheck(itemText):
                itemText = self.getValueOrText(itemText, returnType='text')
            itemUrl = urlArray[i].replace('%20', ' ').strip()
            space = ''


            if frameCheck:
    
                if self.suportFrame(itemUrl, 0.9):
                #if True:
            
                    print itemUrl + ' suport'
                    suportLink[itemText] = itemUrl
                    suportLinkHtml += '<a target="_black" href="' + itemUrl + '"><font style="font-size:10pt;">' + itemText + '</font></a>&nbsp;'
                else:
                    notSuportLink[itemText] = itemUrl
                    notSuportLinkHtml += '<a target="_black" href="' + itemUrl + '"><font style="font-size:10pt;">' + itemText + '</font></a>&nbsp;'
            else:
                suportLink[itemText] = itemUrl
                suportLinkHtml += '<a target="_black" href="' + itemUrl + '"><font style="font-size:10pt;">' + itemText + '</font></a>&nbsp;'

        count = 0
        row = ''
        htmlList = []
        frameCount = 0
        if Config.open_all_link_in_frameset_mode == False:
            for k, v in suportLink.items():
                frameCount += 1
                id = 'iframe' + str(frameCount)
                imageurl = v
                if v.find("bookmark") != -1:
                    imageurl = imageurl[imageurl.find("url=") + 4 :]
                    if imageurl.find("&mode") != -1:
                        imageurl = imageurl[0 : imageurl.find("&mode")]
                elif v.find("socialify") != -1:
                    imageurl = "https://github.com/" + imageurl[imageurl.find("ci/") + 3 : imageurl.find("/image")]

                row += '<td><iframe  id="' + id + '" width="' + str(frameWidth) + '" height="' + str(frameHeight) + '" frameborder="0"  scrolling="auto" src="' + v +'" ></iframe>' + '<a href="javascript:void(0);" onclick="window.open(' + "'" + imageurl + "'" + ');"><img src="https://cdn3.iconfinder.com/data/icons/iconano-web-stuff/512/109-External-512.png" width="18" height="16" style="border-radius:10px 10px 10px 10px; opacity:0.7;"></a>' + '</td><td width="60" ></td><td width="60" ></td><td width="60" ></td>'
                count = count + 1
                if count == column:
                    html += '<tr>' + row + '</tr>'
                    count = 0
                    row = ''
    
            if row != '':
                html += '<tr>' + row + '</tr>' 
    
            bgc = ''
            if changeBG:
                bgc = 'background-color:#E6E6FA'
            
            if hindenLinks:
                newhtml = head + '<div style="width:100%; ' + bgc + '">' + html + '</div>' + end
            else:
                newhtml = head + '<div style="width:100%; ' + bgc + '"><div style="margin-left:auto; text-align:center;margin-top:2px; margin-right:auto; ">' + suportLinkHtml + \
                '&nbsp;&nbsp;/&nbsp;&nbsp; ' + notSuportLinkHtml + '</div><div style="height: 21px; width: 100px"></div>' + html + '</div>' + end
    
            htmlList = [newhtml]
        else:
            for k, v in suportLink.items():
                row += '<frame src="' + v +'" ></frame>'
                count = count + 1
                if count == 4:
                    frameset = '<frameset cols="25%,*,25%, 25%">' + row + '</frameset>'
                    html += frameset
                    htmlList.append(frameset)
                    count = 0
                    row = ''
    
            if row != '':
                if count == 1:
                    
                    frameset = '<frameset cols="100%">' + row + '</frameset>' 
                    html += frameset
                if count == 2:
                    frameset = '<frameset cols="*,50%">' + row + '</frameset>' 
                    html += frameset
                if count == 3:
                    frameset = '<frameset cols="*,30%,30%">' + row + '</frameset>' 
                    html += frameset
                htmlList.append(frameset)
    
        return htmlList, notSuportLink

    def genQuickAcessBtn(self, rid, module):
        return self.genQuickAcessButton(self.queryQuickAccess(rid), module)

    def genQuickAcessButton(self, record, module, iconType='quickaccess'):
        url = record.get_url().strip()
        urlDict = self.genDescLinks(record.get_describe().strip(), self.tag.tag_list)

        #print 'genQuickAcessButton:' + record.get_title()
        #print urlDict

        script = ''

        textList = []
        linkList = []

        if len(urlDict.items()) == 0:
            return ''
        for k, v in urlDict.items():
            if v == url:
                url = ''
            textList.append(k)
            linkList.append(v)
        if url != '':
            textList.append(Config.history_quick_access_name)
            linkList.append(url)

        script = self.getBatchOpenScript(textList, linkList, module)

        html = '<a href="javascript:void(0);" onclick="' + script + '">' + self.getIconHtml('', iconType) + '</a>'

        return html  


    def genDescLinks(self, desc, keywordList, library='', innerSearchWord=''):
        start = 0
        desc = ' ' + desc
        linksDict = {}
        while True:
            end = self.next_pos(desc, start, 10000, keywordList, library=library)
            if end < len(desc):
                #print desc[start : end].strip()
                urlDict = self.genDescLinkHtml(desc[start : end], 100, library=library, returnUrlDict=True, innerSearchWord=innerSearchWord)
                start = end
                for k, v in urlDict.items():
                    linksDict[k] = v
            else:
                urlDict = self.genDescLinkHtml(desc[start : ], 100, library=library, returnUrlDict=True, innerSearchWord=innerSearchWord)
                for k, v in urlDict.items():
                    linksDict[k] = v
                break


        return linksDict

    def genDescHtml(self, desc, titleLen, keywordList, library='', genLink=True, rid='', field='', aid='', refreshID='', iconKeyword=False, fontScala=0, splitChar="<br>", parentDesc='', module='', nojs=False, unfoldSearchin=True, parentOfSearchin='', previewLink=False, cutText=True, parentOfCategory='', parentDivID='', engine='', innerSearchWord='', editMode=False, title='', highLightText=''):
        start = 0
        html = ''
        desc = ' ' + desc
        if genLink:
            while True:
                end = self.next_pos(desc, start, 10000, keywordList, library=library)
                if end < len(desc):
                    rawText = desc[start : end].strip()
                    if iconKeyword:
                        html += self.icon_keyword(self.genDescLinkHtml(rawText, titleLen, library=library, rid=rid, field=field, aid=aid, refreshID=refreshID, fontScala=fontScala, accountIcon=False, parentDesc=parentDesc, module=module, nojs=nojs, unfoldSearchin=unfoldSearchin, parentOfSearchin=parentOfSearchin, previewLink=previewLink, cutText=cutText, parentOfCategory=parentOfCategory, parentDivID=parentDivID, engine=engine, innerSearchWord=innerSearchWord, editMode=editMode, highLightText=highLightText), keywordList, rawText=rawText, parentOfSearchin=parentOfSearchin, title=title, parentDivID=parentDivID) + splitChar

                    else:
                        html += self.color_keyword(self.genDescLinkHtml(rawText, titleLen, library=library, rid=rid, field=field, aid=aid, refreshID=refreshID, fontScala=fontScala, parentDesc=parentDesc, module=module, nojs=nojs, unfoldSearchin=unfoldSearchin, parentOfSearchin=parentOfSearchin, previewLink=previewLink, cutText=cutText, parentOfCategory=parentOfCategory, parentDivID=parentDivID, engine=engine, innerSearchWord=innerSearchWord, editMode=editMode, highLightText=highLightText), keywordList) + splitChar
                    start = end
                else:
                    rawText = desc[start : ]
                    if iconKeyword:
                        html += self.icon_keyword(self.genDescLinkHtml(rawText, titleLen, library=library, rid=rid, field=field, aid=aid, refreshID=refreshID, fontScala=fontScala, accountIcon=False, parentDesc=parentDesc, module=module, nojs=nojs, unfoldSearchin=unfoldSearchin, parentOfSearchin=parentOfSearchin, previewLink=previewLink, cutText=cutText, parentOfCategory=parentOfCategory, parentDivID=parentDivID, engine=engine, innerSearchWord=innerSearchWord, editMode=editMode, highLightText=highLightText), keywordList, rawText=rawText, parentOfSearchin=parentOfSearchin, title=title, parentDivID=parentDivID) + splitChar

                    else:
                        html += self.color_keyword(self.genDescLinkHtml(rawText, titleLen, library=library, rid=rid, field=field, aid=aid, refreshID=refreshID, fontScala=fontScala, parentDesc=parentDesc, module=module, nojs=nojs, unfoldSearchin=unfoldSearchin, parentOfSearchin=parentOfSearchin, previewLink=previewLink, cutText=cutText, parentOfCategory=parentOfCategory, parentDivID=parentDivID, engine=engine, innerSearchWord=innerSearchWord, editMode=editMode, highLightText=highLightText), keywordList) + splitChar
                    break
        else:
            while True:
                end = self.next_pos(desc, start, titleLen, keywordList, library=library)
                if end < len(desc):
                    if iconKeyword:
                        html += self.icon_keyword(desc[start : end], keywordList) + splitChar

                    else:
                        html += self.color_keyword(desc[start : end], keywordList) + splitChar
                    start = end
                else:
                    if iconKeyword:
                        html += self.icon_keyword(desc[start : ], keywordList) + splitChar
                    else:
                        html += self.color_keyword(desc[start : ], keywordList) + splitChar
                    break

        return html


    def getLinkShowText(self, accountTag, originText, tagStr, linkCount, column_num='3', fontScala=0, accountIcon=True, cutText=True):
        text = self.getValueOrText(originText, returnType='text')
        col = int(column_num)
        font_size = 0
        if column_num == '1':
            font_size = '10'
        elif column_num == '2':
            font_size = '9'
        else:
            font_size = '8'
            if linkCount < 5:
                font_size = '11'
            elif linkCount < 7:
                font_size = '10'
            elif linkCount < 8:
                font_size = '9'

        if fontScala != 0:
            font_size = str(int(font_size) - fontScala)

        if accountTag or tagStr == 'social-tag':
            if text.find('</') != -1 and cutText:
                text = self.clearHtmlTag(text)

            prefix = '@'
            icon = ''
            if accountIcon and Config.website_icons.has_key(tagStr):
                icon = self.getIconHtml('', title=tagStr, width=10, height=8)
            if tagStr == 'goodreads':
                text = text[text.find('-') + 1 :]
            elif tagStr == 'slack':
                prefix = '#'
            elif tagStr == 'social-tag':
                prefix = '#'
            #if (tag == 'github' or tag == 'bitbucket') and text.find('/') != -1:
            if text.find('/') != -1 and text.find('</') == -1:
                text = text[text.rfind('/') + 1 : ]
            if text.find('___') != -1:
                text = text[text.rfind('___') + 3 : ]
            if text.find(prefix) != -1:
                text = text[text.find(prefix) + 1 :]

            if cutText:
                text = text[0: self.getCutLen(tagStr, text)]
            if text.startswith(prefix) == False:
                text = prefix + text + icon


            showText = '<i>' + text.encode('utf-8') + '</i>'

            return '<font style="color:#008B00; font-size:' + str(font_size) + 'pt; ' + Config.smart_link_style + '">' + showText + '</font>'
        else:
            #return '<font style="font-size:' + str(font_size) + 'pt;" color="#8E24AA">' + text + '</font>'
             
            if Config.backgrounds[Config.background] != '':
                return '<font style="font-size:' + str(font_size) + 'pt;" color="#8E24AA" ' + Config.smart_link_style + '>' + text + '</font>'
            else:
                return '<font style="font-size:' + str(font_size) + 'pt; ' + Config.smart_link_style + '">' + text + '</font>'
            
        return text

    def getCutLen(self, tagStr, text):
        if self.getValueOrTextCheck(text):
            text = self.getValueOrText(text, returnType='text')
        if tagStr == 'github':
            return len(text)
        elif len(text) > 14 and self.check_contain_chinese(text) == False:
            return 14
        else:
            return len(text)

    def removeDumpValue(self, value):
        valueDict = {}
        valueList = []

        for v in value.split("*"):
            v = v.strip()
            if valueDict.has_key(v):
                continue
            else:
                valueDict[v] = v
                valueList.append(v)
        if len(valueDict.items()) > 0:
            newValue = ''
            for v in valueList:
                newValue += v + "*"
            return newValue[0 : len(newValue) - 1]
            #return "*".join(valueDict.values())
        else:
            return value

    def desc2ValueText(self, desc, tagList):
        start = 0
        valueText = ''
        print "desc2ValueText desc:" + desc
        while True:

            end = self.next_pos(desc, start, 1000, tagList, shortPos=True) 

            if end > 0:
                item = desc[start : end].encode('utf-8')
                tag = item[0 : item.find(':')].strip()
                #print 'tag:' + tag
                if tag == 'website':
                    valueText += item[item.find(':') + 1 :].replace(', ', '+') + '+'
                else:
                    value = item[item.find(':') + 1 :].replace(', ', '*').strip()
                    value = self.removeDumpValue(value)
                    valueText += tag + '(' + value + ')+'
                start = end

            if end >= len(desc):
                break

        valueText = valueText[0 : len(valueText) - 1]

        print 'desc2ValueText valueText:' + valueText
        return valueText

    def valueText2Desc(self, originText, text='', value='', form=None, record=None, tagSplit=' ', prefix=True):
        if text == '' or value == '':
            text = self.getValueOrText(originText, returnType='text')
            value = self.getValueOrText(originText, returnType='value')

        if self.getValueOrTextCheck(originText):
            values = []
            if value.find('+') != -1:
                values = value.split('+')
            else:
                values = [value]
            result = ''
            desc = 'description:'
            website = 'website:'
            command = 'command:'
            classTag = 'class:'
            preData = ''
            #print originText
            #print values
            crossrefDesc = ''
            for v in values:
                #print 'v:' + v
                #if v.endswith('))'):
                #    v = v[0 : len(v) - 1]
                subText = v
                subValue = v
                if self.getValueOrTextCheck(v):
                    subText = self.getValueOrText(v, returnType='text').strip()

                    subValue = self.getValueOrText(v, returnType='value').strip()

                    #if subValue.find('+') != -1:
                    #    result += ' ' + self.valueText2Desc(v)
                    #    continue
                    originSubValue = subValue
                    #print subText + ' ' + subValue

                    subValueIsEngin = False
                    if self.isAccountTag(subText, self.tag.tag_list_account) == False:
                        if self.search_engin_dict.has_key(subValue):
                            subValue = self.getEnginUrl(subValue)
                            subValueIsEngin = True
    
                        if Config.smart_engin_for_tag.has_key(originSubValue):
                            subValue = 'http://_blank'
                            subValueIsEngin = True

                    if self.isAccountTag(text, self.tag.tag_list_account):
                        result = self.accountValue2Desc(subText, text, subValue, result, tagSplit)

                    elif self.isAccountTag(subText, self.tag.tag_list_account) or subText == 'alias' or subText == 'category' or subText == 'searchin':

                        result = self.accountValue2Desc(text, subText, subValue, result, tagSplit)


                    elif self.isUrlFormat(subValue):
                        subTextList = [subText]
                        if subText.startswith('[') and subText.endswith(']'):
                            subsubText = subText[1:len(subText) -1 ]

                            subTextList = self.splitText(subsubText)

                        for st in subTextList:
                            sv = subValue
                            if subValueIsEngin:
                                sv = self.toQueryUrl(subValue, st)
                            else:
                                if subValue.find('%s') != -1:
                                    sv = subValue.replace('%s', st)

                            if prefix:
                                website += text + ' - ' + st + '(' + self.validSubvalue(sv) + '), '
                            else:
                                website += st + '(' + self.validSubvalue(sv) + '), '

                    elif subText == 'crossref':
                        values = []
                        if subValue.find('*') != -1:
                            values = subValue.split('*')
                        else:
                            values = [subValue]
                        count = 0
                        for v in values:
                            count += 1
                            cDesc = self.crossref2Desc(v)
                            if cDesc != '':
                                if cDesc.startswith('website:'):
                                    website += cDesc[cDesc.find(':') + 1 :]
                                    if count != len(values):
                                        website += ', '
                                else:
                                    crossrefDesc += cDesc + ' '

                    elif subText == 'command':

                        subValueList = [subValue]
                        if subValue.find('*') != -1:
                            subValueList = subValue.split('*')

                        for sb in subValueList:

                            newSubText = sb
                            newSubValue = sb
                            if self.getValueOrTextCheck(sb):
                                newSubText = self.getValueOrText(sb, returnType='text').strip()
                                newSubValue = self.getValueOrText(sb, returnType='value').strip() 


                                command += newSubText + '(' + newSubValue + ')'+ ', '
                            else:
                                command += sb + ', '
                    elif subText == 'class':
                        for item in subValue.split('*'):
                            item = item.strip()

                            classTag += item + ', '
                        
                    elif subValue.startswith('d:'):
                        engineList = self.getTopEngin(subValue, sort=True, number=4)
                        urlList = self.engineList2UrlList(engineList, subText)
                        website += subText + '(' + '*'.join(urlList) + '), '
                    elif self.isUrlFormat(subValue) == False and subValue.find('*') != -1 and self.isAccountTag(subText, self.tag.tag_list_account) == False:
                        engineList = subValue.split('*')
                        urlList = self.engineList2UrlList(engineList, subText)
                        website += subText + '(' + '*'.join(urlList) + '), '
                    elif self.getValueOrTextCheck(subValue):
                        newSubText = self.getValueOrText(subValue, returnType='text').strip()
                        newSubValue = self.getValueOrText(subValue, returnType='value').strip()
                        #print newSubText + ' ' + newSubValue

                        if self.isAccountTag(newSubText, self.tag.tag_list_account):
                            if result.find(newSubText + ':') != -1:
                                split = result.find(newSubText + ':') + len(newSubText) + 1
                                result = result[0 : split] + subText + '(' + newSubValue + '), ' + result[split:]
                            else:
                                result += newSubText + ':' + subText + '(' + newSubValue + ')' + tagSplit
                        elif self.search_engin_dict.has_key(newSubValue):
                            website += subText + '(' + self.validSubvalue(self.toQueryUrl(self.getEnginUrl(newSubValue), newSubText)) + '), '
                        elif newSubValue.startswith('d:'):
                            engineList = self.getTopEngin(newSubValue, sort=True, number=4)
                            urlList = self.engineList2UrlList(engineList, newSubText)
                            website += subText + '(' + '*'.join(urlList) + '), '
                        elif self.isUrlFormat(newSubValue) == False and newSubValue.find('*') != -1 and self.isAccountTag(newSubText, self.tag.tag_list_account) == False:
                            engineList = newSubValue.split('*')
                            urlList = self.engineList2UrlList(engineList, newSubText)
                            website += subText + '(' + '*'.join(urlList) + '), '

                        elif subValue.find('@') != -1:
                            #for item in subValue.split('@'):
                            #    item = item.strip()
 
                            desc += subValue + ' '
                    else:
                        desc += subText + ' '

                elif self.isAccountTag(text, self.tag.tag_list_account):
                    result = self.accountValue2Desc(text, text, v, result, tagSplit)
                else:
                    desc += v + ' '
            
            result = result.strip()
            if website != 'website:':
                website = website.strip()
                if website.endswith(','):
                    website = website[0 : len(website) - 1]
                result += tagSplit + website

            if command != 'command:':
                command = command.strip()
                if command.endswith(','):
                    command = command[0 : len(command) - 1]
                result += tagSplit + command

            if classTag != 'class:':
                classTag = classTag.strip()
                if classTag.endswith(','):
                    classTag = classTag[0 : len(classTag) - 1]
                result += tagSplit + classTag                

            if desc != 'description:':
                result += tagSplit + desc.replace('(', ' ')

            #print result
            if crossrefDesc != '':
                
                result = self.mergerDesc(result, crossrefDesc)

            #print result
            return result

        else:
            return ''

    def engineList2UrlList(self, engineList, keyword):
        urlList = []
        #print 'engineList2UrlList:' + str(engineList)
        for engine in engineList:
            engine = engine.strip()
            if engine.startswith('http'):
                url = engine
            elif engine.endswith(':') and self.isAccountTag(engine, self.tag.tag_list_account):
                accountUrl = self.tag.tag_list_account[engine]
                url = self.toQueryUrl(accountUrl, keyword)
            elif self.getValueOrTextCheck(engine):
                text = self.getValueOrText(engine, returnType='text')
                value = self.getValueOrText(engine, returnType='value')
                if value.startswith('http'):
                    url = value
                elif self.isAccountTag(text, self.tag.tag_list_account):
                    accountUrl = self.tag.tag_list_account[text + ':']
                    url = self.toQueryUrl(accountUrl, value)
                elif value.endswith(':') and self.isAccountTag(value, self.tag.tag_list_account):
                    accountUrl = self.tag.tag_list_account[value]
                    url = self.toQueryUrl(accountUrl, text)
                elif self.search_engin_dict.has_key(value):
                    url = self.toQueryUrl(self.search_engin_dict[value].get_url().strip(), text)
                else:
                    url = self.toQueryUrl(self.getEnginUrl(value), text)
            else:
                url = self.toQueryUrl(self.getEnginUrl(engine), keyword)
            urlList.append(url)
        return urlList

    def decodeCommand(self, command):
        if command.find('&') != -1:
            command = command.replace('&', '+')
        if command.find('|') != -1:
            command = command.replace('|', '*')
        return command

    def splitText(self, args):
        keys = []
        if args.find('**') != -1:
           args = args.split('**')
           for i in range(int(args[0]), int(args[1]), int(args[2])):
               keys.append(str(i))
        elif args.find('*') != -1:
            keys = args.split('*')
        return keys  


    def lazyLoad(self, url, delay=3):
    
        browser = webdriver.Chrome(executable_path='/Users/wowdd1/dev/xlb_env/xlinkbook/chromedriver')
    
        browser.get(url)
        delay = delay # seconds
        myElem = ''
        try:
            myElem = WebDriverWait(browser, delay)
            #print "Page is ready!"
        except TimeoutException:
            print "Loading took too much time!"
    
   
        html = self.scrollDownAllTheWay(browser)
        #html = browser.page_source
        #print 'page_source:' + html
        return browser.page_source


    
    def scrollDown(self, driver, value):
        driver.execute_script("window.scrollBy(0,"+str(value)+")")
    
    # Scroll down the page
    def scrollDownAllTheWay(self, driver, scrollDownNum=2000, scrollDownStep=1000):
        html = ''
    
        scrollDownCount = scrollDownNum / scrollDownStep
        old_page = driver.page_source
        html += old_page
        while True:
            #logging.debug("Scrolling loop")
            for i in range(scrollDownCount):
                self.scrollDown(driver, scrollDownStep)
                time.sleep(2)
            new_page = driver.page_source
            if new_page != old_page:
                old_page = new_page
                html += new_page
            else:
                break
        return html

    
    def crossref2Record(self, crossref, rID=''):
        if crossref.find('==') != -1:
            crossref = crossref.replace('==', '->')
        print 'crossref2Record crossref:' + crossref
        path = 'db/' + crossref[0 : crossref.find('#')]
        field = ''
        rTitle = ''
        record = None
        if crossref.find('->') != -1:
            field = crossref[crossref.find('->') + 2 :]
            rTitle = crossref[crossref.find('#') + 1 : crossref.find('->')]
        else:
            rTitle = crossref[crossref.find('#') + 1 :]
        if field != '':
            desc = self.crossref2Desc(crossref)
            if rID == '':
                rID = 'crossref2record'
            record = Record(rID + ' | ' + field + ' | | ' + desc)
        else:
            record = self.getRecord(rTitle, path=path, matchType=2)

              
        return record

    def crossref2Desc(self, crossref):
        v = crossref
        crossrefDesc = ''
        #print '-----crossref2Desc-----'
        #print crossref
        r = None
        key, link = self.getCrossrefUrl(v)
        if v.find('/') != -1:
            text = v[v.rfind('/') + 1 :]
            if text.find('#') != -1:
                path = 'db/' + v[0 : v.rfind('#')]
                text = text[text.find('#') + 1 :]
                if text.find('->') != -1:
                    keywords = text[text.find('->') + 2 :]
                    text = text[0 : text.find('->')]
                    link = link[0 : link.find('->')]
                    print '--->yyy' + keywords + ' ' + path
                    for keyword in keywords.split('&'):
                        keyword = keyword.strip()
                        r = self.getRecord(text, path=path, matchType=2, use_cache=True, log=True)
                        if r != None and r.get_id().strip() != '':
                            matchedText, descList, matchedcategoryList = r.get_desc_field3(self, keyword, self.tag.get_tag_list(''), toDesc=True, prefix=False, deepSearch=False, accurateMatch=True, startMatch=True, endMatch=True)
                            #print '--->xxx'
                            #print ' '.join(descList)
                            crossrefDesc = self.mergerDesc(crossrefDesc, ' '.join(descList))
                            #crossrefDesc += ' '.join(descList) + ' '
                        else:
                            print '**** crossref error ****:' + keyword + ' ' + v
                else:
                    crossrefDesc = 'website:' + text + '(' + self.validSubvalue(link) + ')'
            else:

                crossrefDesc = 'website:' + text + '(' + self.validSubvalue(link) + ')'

        #print crossrefDesc
        return crossrefDesc

    def mergerDesc(self, desc1, desc2):
        if desc1 == '':
            return desc2
        if desc2 == '':
            return desc1

        return self.dict2Desc(self.mergerDescDict(self.toDescDict(desc1, ''), self.toDescDict(desc2, '')))

    def accountValue2Desc(self, text, subText, subValue, result, tagSplit):
        #print 'text:' + text + ' subText:' + subText + ' subValue:' + subValue
        subValue = self.validSubvalue(subValue)
        if subValue.startswith('http'):
            subValue = text + '(' + subValue + ')'
        if subValue.find('*') != -1:
            subValue = ', '.join(subValue.split('*'))

        if result.find(subText + ':') != -1:
            split = result.find(subText + ':') + len(subText) + 1
            result = result[0 : split] + subValue + ', ' + result[split:]
        else:
            result += subText + ':' + subValue + tagSplit

        #print result

        return result


    def validSubvalue(self, subValue):
        if subValue.find(')') != -1 and subValue.find('(') == -1:
            subValue = subValue.replace(')', '')

        return subValue

    def genPreviewLink(self, aid, text, url):

        js = "onHoverPreview('" + aid + "', '" + text + "', '" + url + "', 'searchbox', true);"

        html = '<a href="javascript:void(0);" onclick="' + js + '">' + self.getIconHtml('', 'preview', width=12, height=10) + '</a>'

        return html

    def genCrawlerPreviewLink(self, aid, text, url, parentDivID):

        js = "onCrawlerPreview('" + aid + "', '" + text + "', '" + url + "', '" + parentDivID + "');"

        html = '<a href="javascript:void(0);" onclick="' + js + '">' + self.getIconHtml('', 'crawler', width=12, height=10) + '</a>'

        return html
    
    def genSimilarLink(self, rID, title, url):
        newUrl = ''
        try:
            newUrl = "https://metaphor.systems/search?q=" + urllib.quote(url).replace("/", "%2F")
        except Exception as e:
            return ''
        js = "window.open('" + newUrl + "');"
        html = '<a href="javascript:void(0);" onclick="' + js + '">' + self.getIconHtml('', 'similar2', width=12, height=10) + '</a>'
        return html


    def genDoexclusiveLink(self, rID, title, url, desc):
        if rID == "github" and url == "https://github.com/stars" and title.startswith("stars/"):
            url = "https://github.com/" + self.clearHtmlTag(title)
        js = "doexclusive('" + rID + "', '" + title + "', '" + url + "', '" + desc + "');"
        html = '<a href="javascript:void(0);" onclick="' + js + '">' + self.getIconHtml('', 'url', width=12, height=10) + '</a>'
        return html

    def genChatGPTLink(self, message):
        js = "talkWithChatGPT('https://chatgpt.playingapi.workers.dev/', '" + str(uuid.uuid4()) + "', '" + message + "', '" + str(uuid.uuid4()) + "');"

        html = '<a href="javascript:void(0);" onclick="' + js + '">' + self.getIconHtml('', 'chatgpt', width=12, height=10) + '</a>'

        return html


    def genSearchBoxLink(self, aid, url, parentDivID):
        if url.find("//") != -1:
            url = url.replace("//", "/")
        js = "showSearchBox(pageX, pageY, 550, 480, '" + url + "');"
        html = '<a href="javascript:void(0);" onclick="' + js + '">' + self.getIconHtml('', 'search', width=12, height=10) + '</a>'
        return html


    def genDescEngineHtml(self, keyword, engine):
        print 'genDescEngineHtml:' + keyword + ' ' + engine
        engine = engine.strip()

        html = ''

        if engine == '':
            return ''

        if engine.startswith('d:'):
            engineList = self.getTopEngin(engine, sort=True, number=5)
            urlList = []
            for e in engineList:
                url = self.toQueryUrl(self.getEnginUrl(e), keyword)
                urlList.append(url)

            
            js = "openAll('" + ','.join(urlList) + "','" + ','.join(urlList) + "');"
            html += '<a href="javascript:void(0);" onclick="' + js + '">' + self.getIconHtml('', 'quickaccess') + '</a>'
        
                
        else:
            for e in engine.split(' '):
                url = self.toQueryUrl(self.getEnginUrl(e), keyword)
                #print url
                js = "openUrl('" + url + "', '" + keyword + "', true, true, '', '', '', '', '');"
                hoverJS = "onHover('link', '" + keyword + "', '" + url + "', '', 'searchbox', '', 'false');"

                icon = self.getIconHtml(url, '')
                if icon.strip() == '':
                    icon = self.getIconHtml('', 'website')

                html += '<a href="javascript:void(0);" onclick="' + js + '" onmouseover="' + hoverJS + '">' + icon + '</a>'
        

        #print html
        return html


    def innerSearchWebsite(self, text, url, keyword, aid):
        print 'innerSearchWebsite:' + url
        html = ''
        urlDict = {}
        urlDict2 = {}
        keyword = keyword.replace('%20', ' ').strip()
        
        r = requests.get(url)
        soup = BeautifulSoup(r.text);
        count = 0
        for a in soup.find_all('a'):
            text = str(a.text.lower())
            href = ''
            if a.has_key('href'):
                href = a['href'].lower()
                #print href
            matched = False
            if keyword.startswith(':'):
                if PrivateConfig.innerSearchDict.has_key(keyword):
                    for k in PrivateConfig.innerSearchDict[keyword].split('+'):
                        k = k.strip()
                        if text.find(str(k.strip().lower())) != -1:
                            matched = True
                            break
                else:
                    kd = keyword[1:]
                    for k in kd.split('+'):
                        k = k.strip()
                        if text.find(str(k.lower())) != -1 or href.find(str(k.lower())) != -1:
                            matched = True
                            break
                    #else:
                    #    print href + ' not match'
            else:
                matched = text.find(str(keyword.lower())) != -1
            if href != '' and matched:
                print 'innerSearchWebsite:' + text + ' ' + href
                newAID= aid + str(count)
                itemValue = href
                if itemValue.startswith('http') == False:
                    itemValue = url[0 : url.find('/', url.find('://') + 3)] + '/' + itemValue
                    itemValue = itemValue.replace('//', '/')
                itemText = a.text.strip()

                if urlDict2.has_key(itemValue):
                    continue
                else:
                    urlDict2[itemValue] = ''
                count += 1
                
                key = itemText + '-' + str(count)
                urlDict[key] = itemValue
                html += self.enhancedLink(itemValue, itemText, aid=newAID)
                iconHtml = self.getIconHtml(itemValue, title=itemText)
                if iconHtml != '':
                    html = html.strip() + iconHtml
                html += self.genPreviewLink(newAID, itemText, itemValue)
                html += ', '

        html = html.strip()
        if html.endswith(','):
            html = html[0 : len(html) - 1]
        return html, urlDict


    def getAccountUrl(self, tagStr, tagValue, innerSearchWord):
        url = tagValue
        innerSearchAble = False
        if PrivateConfig.innerSearchDict.has_key(tagStr) and innerSearchWord != '':
            if tagStr == 'github:' and tagValue.find('/') == -1:
                innerSearchWord = 'user%3A' + tagValue + ' ' + innerSearchWord
                tagValue = ''

            url = PrivateConfig.innerSearchDict[tagStr].replace('%w', innerSearchWord)
            innerSearchAble = True
        elif self.tag.tag_list_account.has_key(tagStr):
            accountUrl = self.tag.tag_list_account[tagStr]
            if innerSearchWord != '':
                newUrl = self.urlSearchable(accountUrl)
                if newUrl != '':
                    url = newUrl
            elif tagValue.startswith('http') == False:
                url = accountUrl
        else:
            url = utils.getEnginUrl('glucky')


        if tagValue.startswith('http') == False:
            url = self.toQueryUrl(url, tagValue)

        #url = url.replace('//', '/')

        return url, innerSearchAble

    def getPreviewUrl(self, website, link):
        if website == "github":
            
            repo = link[link.find("com/") + 4 :]
            if repo.endswith("/"):
                repo = repo[0 : len(repo) -1]
            themeList = ["Light", "Dark"]
            fontList = ["Inter", "Bitter", "Raleway", "Rokkitt", "Source Code Pro", "KoHo"]
            bgPatternList = ["Signal", "Charlie Brown", "Formal Invitation", "Plus", "Circuit Board", "Overlapping Hexagons", "Brick Wall", "Floating Cogs", "Diagonal Stripes", "Solid"]
            imageUrl = "https://socialify.git.ci/%s/image?description=1&font=" + choice(fontList) +"&forks=1&issues=1&language=1&name=1&owner=1&pattern=" + choice(bgPatternList) + "&pulls=1&stargazers=1&theme=" + choice(themeList)
            imageUrl = imageUrl.replace("%s", repo)

            imageUrl += "*" + "https://svg.bookmark.style/api?url=https://github.com/" + repo + "&mode=" + choice(themeList)
            return imageUrl
        elif website == "twitter":
            user = link[link.find("com/") + 4 :]
            if user.endswith("/"):
                user = user[0 : len(user) -1]
            imageUrl = "https://syndication.twitter.com/srv/timeline-profile/screen-name/%s?theme=dark"
            imageUrl = imageUrl.replace("%s", user)
            return imageUrl
        elif website == "telegram":
            channel = link[link.find("me/") + 3 :]
            if channel.find("s/") != -1:
                channel = link[link.find("s/") + 2 :]
            if channel.endswith("/"):
                channel = channel[0 : len(channel) -1]

            imageUrl = "https://webfollow.cc/#/channel/" + urllib.quote("https://rsshub.app/telegram/channel/" + channel).replace('/', "%2F")
            #return imageUrl
        return link


    def getExtensionHtml(self, website, title, url, group=False, parent=''):
        return self.extensionManager.getExtensionHtml(website, title, url, group, parent)


    def getWebsiteData(self, website, args):

        html = ''
        if website == "github":
            repos = args.split("*")
            repoDict = {}
            tk = base64.b64decode("Z2hwX2xiOVFuUWJ0VlFRUlRPbzdDd0xZMmJnVUl2NWlXWjBNZkRlSg==") 
            g = Github(tk)
            for repo in repos:
                repo = repo.strip()
                if self.getValueOrTextCheck(repo):
                    repo = self.getValueOrText(repo, returnType='value')
                if repo.endswith('/'):
                    repo = repo[0 : len(repo) - 1]
                if repo.find("/") == -1:
                    continue
                #url = "https://api.github.com/repos/" + repo
                #print url
                #r = requests.get(url)
                #jobj = json.loads(r.text)
                data = ''
                try:
                    data = g.get_repo(repo)
                except Exception as e:
                    print repo + " not found"
                    continue
                if data.stargazers_count != None:
                    repoDict[repo] = data.stargazers_count
                else:
                    print data
            repoList = []
            #html += '<div align="left">'
            for item in sorted(repoDict.items(), key=lambda repoDict:int(repoDict[1]), reverse=True):
                #print item
                #html += item[0] + " " + str(item[1])
                repoList.append(item[0])
                html += '&nbsp;' * 3 + item[0][item[0].find("/") + 1 :] + " " + self.getIconHtml("star") + str(item[1])
                html += ' <img src="https://flat.badgen.net/github/stars/' + item[0] + '" style="max-width: 100%;"/>'
                html += self.genCrawlerPreviewLink('', item[0], "https://github.com/" + item[0], '')
                html += ' <a target="_blank" href="' + "https://github.com/" + item[0] + '"><img src="https://cdn3.iconfinder.com/data/icons/iconano-web-stuff/512/109-External-512.png" width="12" height="10" style="border-radius:10px 10px 10px 10px; opacity:0.7;"></a><br>'
                 
            if len(repoList) > 0:
                html += self.genRepoBottomHtml(repoList)
            #html += "</div>"

        return html

    def genJsIconLinkHtml(self, clickJS, iconUrl, radius=0, width=12, height=10):
        html = '<a href="javascript:void(0);" onclick="' + clickJS + '">' + self.genIconHtml(iconUrl, radius, width, height) + '</a>'
        return html

    searchinCache = {}
    def genDescLinkHtml(self, text, titleLen, library='', rid='', field='', aid='', refreshID='', fontScala=0, accountIcon=True, returnUrlDict=False, haveDesc=False, parentDesc='', module='', nojs=False, unfoldSearchin=False, parentOfSearchin='', previewLink=False, cutText=True, parentOfCategory='', parentDivID='', engine='', innerSearchWord='', editMode=False, highLightText=''):
        tagStr = text[0: text.find(':') + 1].strip()
        tagValue =  text[text.find(':') + 1 : ].strip()

        html = ''
        count = 0
        urlDict = {}
        htmlSpace = ' '
        if fontScala < -4:
            htmlSpace = '&nbsp;' * 3

        if tagStr == 'website:':
            tagValues = tagValue.split(', ')
            for item in tagValues:
                count += 1
                newAID = aid + '-website-' + str(count)
                shwoText = self.getLinkShowText(False, item, tagStr.replace(':', ''), len(tagValues), fontScala=fontScala, cutText=cutText)

                if self.getValueOrTextCheck(item):
                    itemText = self.getValueOrText(item, returnType='text')
                    #print itemText
                    itemValue = self.getValueOrText(item, returnType='value')

                    if innerSearchWord != '':
                        innerhtml, innerUrlDict= self.innerSearchWebsite(itemText, itemValue, innerSearchWord, newAID)
                        html += innerhtml
                        for k, v in innerUrlDict.items():
                            urlDict[k] = v
                        continue
                    urlDict[item] = itemValue
                    html += self.enhancedLink(itemValue, itemText, module=module, library=library, rid=rid, field=field, aid=newAID, refreshID=refreshID, resourceType=tagStr.replace(':', ''), showText=shwoText, dialogMode=False, originText=item, haveDesc=haveDesc, nojs=nojs)
                    #print itemValue
                    #print "========itemText " + itemText
                    filterText = itemText
                    if filterText.find("/") != -1:
                        filterText = filterText[0 : filterText.find("/")].strip()

                    iconHtml = self.getIconHtml(itemValue, title=itemText, desc=text, parentDesc=parentDesc, convertableCheek=True, highLightText=highLightText, filterText=itemText, parentOfSearchin=parentOfSearchin[1:])
                    if highLightText != '' and itemValue.find("*") != -1 and iconHtml != '':
                        filterUrls = []
                        for url in itemValue.split("*"):
                            if highLightText.find("+") != -1:
                                highLightTextArray = highLightText.split("+")
                                for subHighLightText in highLightTextArray:
                                    subHighLightText = subHighLightText.lower().strip()
                                    if url.lower().find(subHighLightText) != -1:
                                        filterUrls.append(url)
                                        break
                            else:
                                if url.lower().find(highLightText.lower()) != -1:
                                    filterUrls.append(url)
                            
                        if len(filterUrls) > 0 and len(filterUrls) != len(itemValue.split("*")):
                            if len(filterUrls) == 1:
                                filterUrls.append("")
                            iconHtml += " " + self.getIconHtml('*'.join(filterUrls), title=itemText, desc=text, parentDesc=parentDesc, convertableCheek=True, highLightText=highLightText, filterText=itemText, parentOfSearchin=parentOfSearchin[1:])

                    if iconHtml != '':
                        html = html.strip() + iconHtml
                    if previewLink:
                        html += self.genPreviewLink(newAID, itemText, itemValue)
                    html += self.genChatGPTLink(itemText)
                    if engine != '':
                        html += self.genDescEngineHtml(itemText, engine)
                else:
                    url = self.toQueryUrl(self.getEnginUrl('glucky'), item)
                    urlDict[item] = url
                    html += self.enhancedLink(url, item, module=module, library=library, rid=rid, field=field, aid=newAID, refreshID=refreshID, resourceType=tagStr.replace(':', ''), showText=shwoText, dialogMode=False, originText=item, haveDesc=haveDesc, nojs=nojs)
                    if previewLink:
                        html += self.genPreviewLink(newAID, item, url)
                    if engine != '':
                        html += self.genDescEngineHtml(item, engine)
                if count != len(tagValues):
                    html += ',' + htmlSpace
            if highLightText != '':
                js = "typeKeyword('??" + tagStr + highLightText + "');"
                html += self.genJsIconLinkHtml(js, Config.website_icons["similar"]) + ' <font style="font-size:7pt; font-family:San Francisco;">' + '</font>'

            js = "tabsPreviewEx(this, '', '" + "*".join(urlDict.values()).replace("www.", '') + "', '', 'website:', '" + parentOfSearchin[1:] + "');"
            html += self.genJsIconLinkHtml(js, Config.website_icons["tabs"]) + ' <font style="font-size:7pt; font-family:San Francisco;">' + str(len(('*'.join(urlDict.values()).split('*')))) + '</font>'

            #html += str(len(urlDict.values()))
        elif self.isAccountTag(tagStr, self.tag.tag_list_account):
            url = ''
            #print 'innerSearchWord:' + innerSearchWord

            urlList = []
            titleList = []
            tagValues = tagValue.split(',')
            for item in tagValues:
                item = item.strip()
                count += 1
                newAID = aid + '-' + tagStr.replace(':', '').strip().lower() + '-' + str(count)
                shwoText = self.getLinkShowText(True, item, tagStr.replace(':', ''), len(tagValues), fontScala=fontScala, accountIcon=accountIcon, cutText=cutText)
                exclusiveLink = ''
                if self.getValueOrTextCheck(item):
                    itemText = self.getValueOrText(item, returnType='text')
                    #print itemText
                    itemValue = self.getValueOrText(item, returnType='value')

                    #print 'itemValue:' + itemValue
                    link, innerSearchAble = self.getAccountUrl(tagStr, itemValue, innerSearchWord)

                    #print 'link:' + link
                    if innerSearchWord != '' and innerSearchAble == False:
                        print 'ignore'
                    else:
                        urlDict[item] = link

                    urlList.append(link)
                    titleList.append(itemText)
                    html += self.enhancedLink(link, itemText, module=module, library=library, rid=rid, field=field, aid=newAID, refreshID=refreshID, resourceType=tagStr.replace(':', ''), showText=shwoText, dialogMode=False, originText=item, haveDesc=haveDesc, nojs=nojs)
                    html += self.getIconHtml('remark', title=itemText, desc=text, parentDesc=parentDesc)
                    if previewLink:
                        if link.find("github.com") != -1:
                            html += self.genPreviewLink(newAID, itemText, self.getPreviewUrl("github", link))
                            html += self.genCrawlerPreviewLink(newAID, itemText, link, parentDivID)

                            #html += self.genSearchBoxLink(newAID,link + "/search?q=", parentDivID)
                        elif link.find("twitter.com") != -1:
                            html += self.genPreviewLink(newAID, itemText, self.getPreviewUrl('twitter', link))
                        elif link.find("t.me") != -1:
                            html += self.genPreviewLink(newAID, itemText, self.getPreviewUrl('telegram', link))

                        else:    
                            html += self.genPreviewLink(newAID, itemText, link)  


                    html += self.genSimilarLink(tagStr[0 : len(tagStr) - 1], itemText, link)
                    html += self.genChatGPTLink(itemText)

                    exclusiveLink = link
                    group = previewLink == False
                    if tagStr == "github:":
                        group = True
                        exclusiveLink = "https://github.com/" + itemValue[0 : itemValue.find("/")]

                    
                    html += self.genDoexclusiveLink(tagStr[0 : len(tagStr) - 1], itemText, exclusiveLink, "")
                    html += self.extensionManager.getExtensionHtml(tagStr[0 : len(tagStr) - 1], itemText, link, group, parentOfSearchin[1:])

                    if engine != '':
                        html += self.genDescEngineHtml(itemText, engine)         
                else:
                    link, innerSearchAble = self.getAccountUrl(tagStr, item, innerSearchWord)
                    if innerSearchWord != '' and innerSearchAble == False:
                        print 'ignore'
                    else:
                        urlDict[item] = link
                    urlList.append(link)
                    titleList.append(item)
                    html += self.enhancedLink(link, item, module=module, library=library, rid=rid, field=field, aid=newAID, refreshID=refreshID, resourceType=tagStr.replace(':', ''), showText=shwoText, dialogMode=False, originText=item, haveDesc=haveDesc, nojs=nojs)
                    if previewLink:
                        if link.find("github.com") != -1:
                            html += self.genPreviewLink(newAID, item, self.getPreviewUrl('github', link))
                            html += self.genCrawlerPreviewLink(newAID, item, link, parentDivID)
                            #html += self.genSearchBoxLink(newAID,link + "/search?q=", parentDivID)
                        elif link.find("twitter.com") != -1:
                            html += self.genPreviewLink(newAID, item, self.getPreviewUrl('twitter', link))
                        elif link.find("t.me") != -1:
                            html += self.genPreviewLink(newAID, item, self.getPreviewUrl('telegram', link))
                        else:
                            html += self.genPreviewLink(newAID, item, link) 
                    
                    html += self.genSimilarLink(tagStr[0 : len(tagStr) - 1], item, link)
                    html += self.genChatGPTLink(item)

                    exclusiveLink = link
                    group = previewLink == False
                    if tagStr == "github:":
                        group = True
                        exclusiveLink = "https://github.com/" + item[0 : item.find("/")]
                    html += self.genDoexclusiveLink(tagStr[0 : len(tagStr) - 1], item, exclusiveLink, "")
                    html += self.extensionManager.getExtensionHtml(tagStr[0 : len(tagStr) - 1], item, link, group, parentOfSearchin[1:])


                    if engine != '':
                        html += self.genDescEngineHtml(item, engine)  
                if count != len(tagValues):
                    html += htmlSpace
            js = "typeKeyword('?>" + parentOfSearchin[1:] + "/" + tagStr + " + "  + tagStr[0 : len(tagStr) - 1] + "/:combine" + "');"
            html += self.genJsIconLinkHtml(js, Config.website_icons["combine"])

            #for domain process
            if tagStr == "github:" and len(tagValues) > 1:
                js = "onRepoPreview('" + "*".join(tagValues) + "');"
                html += self.genJsIconLinkHtml(js, Config.website_icons["crawler"])
            if tagStr == "github:" or tagStr == "twitter:":
                if len(tagValues) > 1:
                    userList = []
                    for user in tagValues:
                        if user.find("/") != -1:
                            user = user[0 : user.find("/")].strip()
                        if tagStr == "github:":
                            userList.append("https://github.com/" + user.strip())
                        elif tagStr == "twitter:":
                            userList.append("https://twitter.com/" + user.strip())
                    if len(userList) > 0:
                        exclusiveLink = ",".join(userList)
                        html += self.genDoexclusiveLink(tagStr[0 : len(tagStr) - 1], tagStr[0 : len(tagStr) - 1], exclusiveLink, "")

            if len(tagValues) > 1:
                #js = "tabsPreview(this, '" + "*".join(titleList) + "', '" + "*".join(urlList) + "', '');"
                js = "tabsPreviewEx(this, '', '" + "*".join(urlList).replace("www.", '') + "', '', '" + tagStr + "', '" + parentOfSearchin[1:] + "');"
                html += self.genJsIconLinkHtml(js, Config.website_icons["tabs"]) + ' <font style="font-size:7pt; font-family:San Francisco;">' + str(len(urlList)) + '</font>'

            if highLightText != '':
                js = "typeKeyword('??" + tagStr + highLightText + "');"
                html += self.genJsIconLinkHtml(js, Config.website_icons["similar"]) + ' <font style="font-size:7pt; font-family:San Francisco;">' + '</font>'

            if self.urlConvertable(self.tag.tag_list_account[tagStr]):
                #html += self.getIconHtml('', 'data')
                #if tagStr == "github:":

                js = "getWebsiteData('" + tagStr[0 : len(tagStr) - 1]+ "', '" + '*'.join(tagValues) + "');"
                html += self.genJsIconLinkHtml(js, Config.website_icons["data"])
                

        elif tagStr == 'icon:':
            html += '<img src="' + tagValue + '" height="14" width="14" />'

        elif tagStr == 'searchin:':
            print 'unfoldSearchin:' + str(unfoldSearchin) + ' cmds:' + str(tagValue)
            tagStr = ''
            if field != '':
                self.searchinCache[field] = tagValue
            cmds = tagValue.split(',')
            result = ''
            
            if unfoldSearchin:
                bkColor = '#f6f3e5'
                #if parentOfSearchin != '':
                #    bkColor = '#30dee5'
                result = self.doUnfoldSearchin(cmds, parentOfSearchin, bkColor=bkColor, editMode=editMode)
                #print 'doUnfoldSearchin returnCmdList:' + str(self.doUnfoldSearchin(cmds, parentOfSearchin, returnCmdList=True))
            else:
                for cmd in cmds:
                    cmd = cmd.strip()
                    showText = cmd[1:]
                    if cmd.startswith('&>') and self.getValueOrTextCheck(cmd):
                        showText = self.getValueOrText(cmd, returnType='text')
                        cmd = self.getValueOrText(cmd, returnType='value').replace('&', ' + ') + '/:'
                        showText = showText[2:]

                    if cmd.startswith('>') or cmd.startswith('&>') or cmd.startswith('#'):
                        result += '<a href="javascript:void(0);" onclick="typeKeyword(' + "'%" + cmd + "', '" + parentOfSearchin + "'" +')" style="color:#EC7063; font-size:9pt;">></a>'
                        #js = 'typeKeyword(' + "'" + cmd + "', '" + parentOfSearchin + "'" +');' + "chanageLinkColor(this, '#E9967A', '');"
                        
                        js = "showPopupContent(pageX, pageY, 550, 480, '#" + cmd + "/:');"

                        js2 = "lastHoveredUrl = '" + cmd + "'; lastHoveredText = '" + cmd[cmd.find('>') + 1 :].replace(' + >', '*').replace('/:', '') + "'; lastHoveredCMD = '" + cmd + "';"
                        if parentDivID != '':
                            js = 'typeKeywordEx(' + "'" + cmd + "/:', '" + parentOfSearchin + "', false, '" + parentDivID + "'" +');' + "chanageLinkColor(this, '#E9967A', '');"

                        
                        result += '<a href="javascript:void(0);" onclick="' + js + '" onmouseover="' + js2 + '" style="color: rgb(153, 153, 102); font-size:9pt;">' + showText + '</a> '

                        #if parentDivID != '':
                        #    style = 'style="padding-left:20px; padding-top: 10px;"'
                        #    result +=  self.processCommand(cmd + '/:', '', showDynamicNav=False, noFilterBox=True, style=style, isRecursion=True);

                    else:
                        result += '<a href="javascript:void(0);" onclick="typeKeyword(' + "'" + cmd + "', '" + parentOfSearchin + "'" +')" style="color: rgb(153, 153, 102); font-size:9pt;">' + cmd + '</a> '
                


                js = "typeKeyword('e" +  parentOfSearchin +"')"
                result += '<a href="javascript:void(0);" onClick="' + js + '">' + self.getIconHtml('edit') + '</a>'

            #if unfoldSearchin == False and tagValue.find(parentOfSearchin) == -1:
            #    result = '<a href="javascript:void(0);" onclick="typeKeyword(' + "'" + parentOfSearchin + "', '" + parentOfSearchin + "'" +')" style="color: rgb(153, 153, 102); font-size:9pt;">' + parentOfSearchin + '</a> ' + result

            if unfoldSearchin == False:
                #result = self.getIconHtml('searchin:') + ':' + result
                result = self.getIconHtml('searchin:') + ':'
                #result = ''
                #result = 'searchin:' + result

                #result += self.getIconHtml('searchin:') + ':<br>'
                #result += ""
                subSearchin = self.loadSubSearchin(">" + field, parentOfSearchin, 446, parentDivID=parentDivID)
                if subSearchin != "":
                    result += subSearchin 
                    if len(cmds) > 18:
                        result += "<br><br><br><br><br><br><br><br>"
                    elif len(cmds) > 12:
                        result += "<br><br><br><br><br><br>"
                    elif len(cmds) > 6:
                        result += "<br><br><br><br>"
                    else:
                        result += "<br><br><br>"
            #else:
            #    result += '<div align="center" style="border-radius:15px 15px 15px 15px; padding-left: 0; padding-top: 2px; width:' + str(divWidth/2) + 'px; height:' + str(maxHeight) + 'px; float:left;" onmouseout="normal(this);" onmouseover="hover(this);">'  
            #    
            #    result += '<a href="javascript:void(0);" onclick="">' + self.getIconHtml('', 'add', width=64, height=64) + '</a>'
            #    result += '</div>'                  

            html += result
        elif tagStr == 'alias:' or tagStr == 'category:':
            result = ''
            
            categoryGroup = {}

            for item in tagValue.split(','):
                item = item.strip()
                keyword = '?=>' + item
                if tagStr == 'category:':
                    if parentOfCategory != '' and item.find('#') == -1:
                        key = '#' + parentOfCategory
                        value = '->' + item + ':'
                        if categoryGroup.has_key(key):
                            categoryGroup[key].append(value)
                        else:
                            categoryGroup[key] = [value]
                    elif item.startswith('#') and item.find('->'):
                        key = item[0:item.find('->')]
                        value = item[item.find('->') : ].strip()
                        if categoryGroup.has_key(key):
                            categoryGroup[key].append(value)
                        else:
                            categoryGroup[key] = [value]
                else:
                    keyword = '=>' + item
                    js = "typeKeyword('" + keyword + "/:/:group-short " + item + "', '" + parentOfSearchin + "');chanageLinkColor(this, '#E9967A', '');"
                    js2 = "lastHoveredUrl = '" + self.toQueryUrl(self.getEnginUrl('google'), item) + "'; lastHoveredText = '" + item + "';"

                    if parentDivID != '':
                        js = "typeKeywordEx('" + keyword + "/:', '" + parentOfSearchin + "', false, '" + parentDivID + "');chanageLinkColor(this, '#E9967A', '');"

                    result += '<a href="javascript:void(0);" onclick="' + js + '" onmouseover="' + js2 + '" style="color: rgb(153, 153, 102); font-size:9pt;">' + item + '</a>'
                    
                    keyword = '?=>' + item
                    js = "typeKeyword('" + keyword + "/:/:group-short " + item + "', '" + parentOfSearchin + "');"
                    if parentDivID != '':
                        js = "typeKeywordEx('" + keyword + "/:', '" + parentOfSearchin + "', false, '" + parentDivID + "');"
                   

                    result += '<a href="javascript:void(0);" onclick="' + js + '" style="color: rgb(153, 153, 102); font-size:9pt;">' + self.getIconHtml('', 'clustering', width=12, height=10) + '</a> '
                    

                    js = "typeKeywordEx('??" + item + "', '" + parentOfSearchin + "', false, '" + parentDivID + "');"
                    result += '<a href="javascript:void(0);" onclick="' + js + '" style="color: rgb(153, 153, 102); font-size:9pt;">' + self.getIconHtml('', 'command', width=12, height=10) + '</a>'

                    result += self.genChatGPTLink(item)
                    if engine != '':
                        result += self.genDescEngineHtml(item, engine) 
                    result += ', '

            
            if tagStr == 'category:' and len(categoryGroup) > 0:
                print categoryGroup
                print 'categoryGroup'
                for item in categoryGroup.items():
                    if len(item[1]) > 1 or len(categoryGroup) > 1:
                        js = "typeKeyword('" + item[0] + "', '" + parentOfSearchin + "');"
                        if parentDivID != '':
                            js = "typeKeywordEx('" + item[0] + "/:', '" + parentOfSearchin + "', false, '" + parentDivID + "');"

                        result += '<a href="javascript:void(0);" onclick="' + js + '" style="color: rgb(153, 153, 102); font-size:9pt;">' + item[0] + '</a>'
                    count = 0
                    listItemCache = {}
                    for listItem in item[1]:
                        if listItemCache.has_key(listItem):
                            continue
                        cmd = item[0] + listItem
                        if count > 0:
                            listItem = listItem[listItem.find('->') + 2:]
                        listItemShow = listItem.replace(':', '')
                        if len(item[1]) == 1 and len(categoryGroup) == 1:
                            listItemShow = listItemShow.replace('->' , '')
                        js = "typeKeyword('" + cmd + "', '" + parentOfSearchin + "');chanageLinkColor(this, '#E9967A', '');"
                        if parentDivID != '':
                            js = "typeKeywordEx('" + cmd + "/:', '" + parentOfSearchin + "', false, '" + parentDivID + "');chanageLinkColor(this, '#E9967A', '');"

                        result += '<a href="javascript:void(0);" onclick="' + js + '" style="color: rgb(153, 153, 102); font-size:9pt;">' + listItemShow + '</a>'
                        js = "typeKeyword('" + cmd + "/:/:group-short " + cmd + "', '" + parentOfSearchin + "');"
                        result += '<a href="javascript:void(0);" onclick="' + js + '" style="color: rgb(153, 153, 102); font-size:9pt;">' + self.getIconHtml('', 'clustering') + '</a>'

                        count += 1
                        listItemCache[listItem] = listItem
                        if count < len(item[1]):
                            result += ' '
                    result += ', '

            if result.endswith(', '):
                result = result[0 : len(result) - 2]
            html += tagStr + result
            tagStr = ''
            
        elif tagStr == 'command:':
            result = ''

            for item in tagValue.split(','):
                text = item
                value = item
                if self.getValueOrTextCheck(item):
                    text = self.getValueOrText(item, returnType='text')
                    value = self.decodeCommand(self.getValueOrText(item, returnType='value'))

                js = "typeKeyword('" + self.decodeCommand(value) + "', '" + parentOfSearchin + "');chanageLinkColor(this, '#E9967A', '');"
                js2 = "lastHoveredUrl = '" + value + "'; lastHoveredText = '" + text + "';"

                style = "color: rgb(153, 153, 102); font-size:9pt;"
                if parentDivID != '':
                    cmd = self.decodeCommand(value)
                    if parentOfSearchin == '>Combine Result' or (cmd.startswith(">") and cmd.startswith(">>") == False and len(cmd.split("/")) == 2 and cmd.find("??") == -1 and cmd.find("+") == -1):
                        cmd += ' + :cmd '
                        style = "color: rgb(255,99,71); font-size:9pt;"
                    js = "typeKeywordEx('" + cmd  + "', '" + parentOfSearchin + "', false, '" + parentDivID + "');chanageLinkColor(this, '#E9967A', '');"

                result += '<a href="javascript:void(0);" onclick="' + js + '" onmouseover="' + js2 + '" style="' + style + '">' + text + '</a>'
                if parentDivID.find("combine-result") != -1:
                    js = "showPopupContent(pageX, pageY, 550, 480, '#>" + text + "/:');"
                else:
                    js = "showPopupContent(pageX, pageY, 550, 480, '" + value + "');"


                result += ' <a href="javascript:void(0);" onclick="' + js + '" >' + self.getIconHtml('', 'tabs', width=10, height=8) + '</a>'
                result += ", "

             
            if result.endswith(', '):
                result = result[0 : len(result) - 2]   
            #html += self.getIconHtml(tagStr) + ':' + result
            #tagStr = ''

            html += result

        elif tagStr == 'crossref:':
            result = ''

            for item in tagValue.split(','):
                key, url = self.getCrossrefUrl(item)
                result += self.enhancedLink(url, item[item.rfind('#') + 1 :], style='color: rgb(153, 153, 102); font-size:9pt;') + ', '

            if result.endswith(', '):
                result = result[0 : len(result) - 2]
            #html += self.getIconHtml(tagStr) + ':' + result
            #tagStr = ''
            
            html += result
        elif tagStr == 'class:':
            result = ''

            for item in tagValue.split(','):
                text = item
                url = item
                #class(test(extensions.code.code.Code))
                if self.getValueOrTextCheck(item):
                    text = self.getValueOrText(item, returnType='text')
                    url = self.getValueOrText(item, returnType='value')

                if url.startswith('extensions') == False:
                    url = 'extensions.code.' + url + '.' + url

                url = url[0 : url.rfind('.')]
                url = os.getcwd() + '/' + url.replace('.', '/') + '.py'
                if field != '':
                    url += " -i " + field
                result += self.enhancedLink(url, text, style='color: rgb(153, 153, 102); font-size:9pt;') + ''

                js = "exec('run','','" + url + "');"
                result += '<a href="javascript:void(0);" onclick="' + js + '">' + self.getIconHtml('', 'run') + '</a>'
                js = "exec('edit','','" + url + "');"
                result += '<a href="javascript:void(0);" onclick="' + js + '">' + self.getIconHtml('', 'alias') + '</a>, '

            if result.endswith(', '):
                result = result[0 : len(result) - 2]
            html += self.getIconHtml(tagStr) + ':' + result

            tagStr = ''
        else:
            if returnUrlDict:
                return urlDict
            else:
                return ' ' + tagStr + self.formatTitle(tagValue)

        if returnUrlDict:
            return urlDict
        else:
            if html == '':
                return ''            
            return ' ' + tagStr + html

    def doUnfoldSearchin(self, searchinList, parentOfSearchin, runCMD=True, returnCmdList=False, bkColor='#f6f3e5', editMode=False):
        #print 'doUnfoldSearchin:' + str(searchinList)
        layerList = []
        cmdList = []
        result = ''
        for cmd in searchinList:
            cmd = cmd.strip()
            if self.getValueOrTextCheck(cmd):
                layerList.append(cmd)
            else:
                cmdList.append(cmd)

        if returnCmdList:
            layerCmdList = []
            if len(layerList) > 0:
                for layer in layerList:
                    text = self.getValueOrText(layer, returnType='text')
                    value = self.getValueOrText(layer, returnType='value')
                    #print 'value:' + value
                    splitChar = '&'
                    if value.find('@>') != -1 and value.find('&>') == -1:
                        splitChar = '@'
                    layerCmdList += self.doUnfoldSearchin(value.split(splitChar), '', returnCmdList=True, bkColor=bkColor, editMode=editMode)

                    #print 'layerCmdList:' + str(layerCmdList)

            return cmdList + layerCmdList

        print 'layerList:'
        print layerList
        if len(layerList) > 0:
            for layer in layerList:
                html, layerHeight = self.loadSearchinGroup([layer], parentOfSearchin, runCMD=runCMD, bkColor=bkColor, editMode=editMode)
                result += html
        if len(cmdList) > 0:
            html, layerHeight = self.loadSearchin(cmdList, parentOfSearchin, runCMD=runCMD, bkColor=bkColor, editMode=editMode)
            result += html

        return result

    def loadSearchinGroup(self, layerList, parentOfSearchin, splitChar='&', hiddenDescHtml=False, layerNoBorder=True, isRecursion=False, runCMD=True, bkColor='#f6f3e5', editMode=False):
        result = ''
        totalLayerHeight = 0
        print 'loadSearchinGroup:' + str(layerList)
        for layer in layerList:
            print 'layer:' + layer
            text = self.getValueOrText(layer, returnType='text')
            value = self.getValueOrText(layer, returnType='value')
            print 'loadSearchinGroup:' + text + ' ' + value + ' ' + parentOfSearchin

            cmdList = value.split(splitChar)
            subLayerList = []
            subCmdList = []
            print 'cmdList:' + str(cmdList)
            for cmd in cmdList:
                if cmd.startswith('>') and self.getValueOrTextCheck(cmd):
                    subLayerList.append('&' + cmd)
                else:
                    subCmdList.append(cmd)
            layerHeight = 0

            htmlCache1 = ''
            htmlCache2 = ''
            layerName = ''
            if len(subLayerList) > 0:
                htmlCache2, layerHeight = self.loadSearchinGroup(subLayerList, parentOfSearchin, splitChar='@', hiddenDescHtml=True, layerNoBorder=False, isRecursion=True, runCMD=runCMD, bkColor=bkColor, editMode=editMode)
                totalLayerHeight += layerHeight
            if len(subCmdList) > 0:
                layerName = text[2:]
                if layerName.startswith('!'):
                    runCMD = False
                    layerName = layerName[1:]
                htmlCache1, layerHeight = self.loadSearchin(subCmdList, parentOfSearchin, layerName=layerName, layer=layer, hiddenDescHtml=hiddenDescHtml, layerNoBorder=layerNoBorder, runCMD=runCMD, bkColor=bkColor, editMode=editMode, loadSubSearchin=False)
                totalLayerHeight += layerHeight
            
            if htmlCache1 != '':
                result += htmlCache1
            if htmlCache2 != '':
                result += htmlCache2
            html = result
            if len(subLayerList) > 0 or isRecursion == False:
                divID = ''
                if layerName != "":
                    divID = layerName.lower().strip().replace(" ", "_")
                html = '<div id="' + divID + '" style="background-color:' + str(bkColor) + '; height:' + str(totalLayerHeight + 36) + 'px; width:100%; margin-top:10px; margin-bottom:10px; border-radius:15px 15px 15px 15px; border-style: groove;border-width: 2px;">'
                #insert layer arrow here 
                #html += '<a id="' + divID + "_name" + '"><font style="color:#8178e8; font-size:15pt;">' + layerName + '</font></a>'
                #html += '<a href="javascript:void(0);"  onclick=\"hiddenOrShowLayer(' + "'" + divID + "'" + ');\"><img src="https://cdn2.iconfinder.com/data/icons/duo-toolbar-signs/512/erase-512.png" width="18" height="16" style="border-radius:10px 10px 10px 10px; opacity:0.7;"><a>'; 

                #html += "subCmdList:" + str(subCmdList)
                #html+= "subLayerList:" + str(subLayerList)

                if len(subCmdList) == 0:
                    layerName = text[text.find('>') + 1 :]
                    if layerName.startswith('!'):
                        layerName = layerName[1:]
                    html += '<div style="width:100%" align="center"><font style="color:#8178e8; font-size:15pt;">' + layerName + '</font></div>'
                html += result

            if len(subLayerList) > 0 or isRecursion == False:
                html += '</div>'

            result = html

        return result, totalLayerHeight    

    def loadSearchin(self, cmdList, parentOfSearchin, layerName='', layer='', hiddenDescHtml=False, layerNoBorder=True, runCMD=True, bkColor='#f6f3e5', editMode=False, loadSubSearchin=True, parentDivID=''):

        result = ''
        searchResultDict = {}
        searchResultBRCountDict = {}
        divWidth = 446
        
        if layerName == '':
            #bkColor = '#CCCCCC'
            bkColor = ''


        layerHeight = 0
        divPaddingLeft = 0
        divMarginLeft = 0
        if layerName != '':
            divPaddingLeft = 18
            divMarginLeft = 3
        rListCache = {}
        editSearchinLinkArgsCache = {}
        for cmd in cmdList:
            cmd = cmd.strip()
            if cmd == '':
                continue
            if runCMD:
                searchResult = self.processCommand(cmd, '', noDiv=True, unfoldSearchin=False, noFilterBox=True, isRecursion=True, parentOfSearchin=parentOfSearchin, hiddenDescHtml=hiddenDescHtml)
            else:
                searchResult = '<div style="height:#heightpx; text-align:center;line-height:#heightpx;">' 
                keyword = cmd[cmd.find('>') + 1 :]
                url = cmd
                haveUrl = False
                if keyword.find('<http') != -1 and keyword.find('>') != -1:
                    url = keyword[keyword.find('<http') + 1 : keyword.find('>')].strip().replace(' ', '*')
                    keyword = keyword[0: keyword.find('<http')]
                    haveUrl = True

                js = "typeKeyword('>" + keyword + "', ''); chanageLinkColor(this, '#E9967A', '');"
                js2 = "lastHoveredUrl = '" + url + "'; lastHoveredText = '" + keyword + "'; lastHoveredCMD = '>" + keyword + "/'; search_box.value = '>" + keyword + "';"
                searchResult += '<a href="javascript:void(0);" onclick="' + js + '" onmouseover="' + js2 + '">' + cmd[cmd.find('>') + 1 :][cmd.find('#') + 1 :] + '</a>'
                if cmd.find('<http') != -1:
                    cmd = cmd[0 : cmd.find('<http')]

                js = "showPopupContent(pageX, pageY, 550, 480, '#" + cmd + "/:');"
                searchResult += '<a href="javascript:void(0);" onclick="' + js + '" >' + self.getIconHtml('', 'tabs', width=10, height=8) + '</a>'
                js = "showPopupContent(0, 20, 1444, 900, '" + cmd + "');"
                searchResult += '<a href="javascript:void(0);" onclick="' + js + '" >' + self.getIconHtml('', 'url', width=10, height=8) + '</a>'                
                if haveUrl:
                    if url.find('*') != -1:
                        js = ''
                        #for link in url.split('*'):
                        #    js += "window.open('" + link + "');"
                        js = "tabsPreview(this, '', '" + url + "', '')";
                        searchResult += '<a href="javascript:void(0);" onclick="' + js + '">'
                        searchResult += self.getIconHtml('tabs', width=10, height=8)
                        searchResult += '</a>'
                    else:
                        js = "window.open('" + url + "');"
                        searchResult += '<a href="javascript:void(0);" onclick="' + js + '">'
                        searchResult += self.getIconHtml('website', width=10, height=8)
                        searchResult += '</a>'
                #'''  Edit the link in searchin field
                if parentOfSearchin != '' and editMode:
                    rList = []
                    if rListCache.has_key(parentOfSearchin):
                        print 'rListCache hit'
                        rList = rListCache[parentOfSearchin]
                    else:
                        rList = self.processCommand(parentOfSearchin, '', returnMatchedDesc=True)
                        rListCache[parentOfSearchin] = rList
                    if len(rList) > 0 and len(rList[0]) > 0:
                        searchinR = None
                        library = ''
                        searchin = ''
                        descPart = ''
                        resourceType = ''
                        if editSearchinLinkArgsCache.has_key(parentOfSearchin):
                            argsList = editSearchinLinkArgsCache[parentOfSearchin]
                            searchinR = argsList[0]
                            library = argsList[1]
                            searchin = argsList[2]
                            descPart = argsList[3]
                            resourceType = argsList[4]
                            print 'editSearchinLinkArgsCache hit'
                        else:
                            searchinR = rList[0][5]
                            library = rList[0][3][rList[0][3].rfind('/') + 1 : rList[0][3].rfind('library') + 7]
                            tag = Tag()
                            searchinMatchedTextList, searchinDescList, searchinMatchedcategoryList = searchinR.get_desc_field3(self, parentOfSearchin[1:], tag.get_tag_list(library), toDesc=True, prefix=False)
                            print rList[0][0] 
                            print 'searchinMatchedcategoryList:' + str(searchinMatchedcategoryList)
                            #searchResult += str(searchinMatchedTextList) + str(searchinDescList)
                            tempR = Record(' | | | ' + searchinDescList[0])
                            searchin = self.reflection_call('record', 'WrapRecord', 'get_tag_content', tempR.line, {'tag' : 'searchin'})  
                            desc = searchinDescList[0]
                            descPart = ''
                            descDict = self.toDescDict(desc, 'ai-library')
                            count = 0
                            for k, v in descDict.items():
                                count += 1
                                if k == 'searchin':
                                    continue
                                else:
                                    if k == 'website':
                                        descPart +=  v
                                    else:
                                        descPart += k + '(' + v.replace(', ', '*') + ')'
                                    if count < len(descDict):
                                        descPart += ',newline' 
                            editSearchinLinkArgsCache[parentOfSearchin] = [searchinR, library, searchin, descPart, searchinMatchedcategoryList[0]]
                        print '-------' + searchinDescList[0] + '------'
                        print '-------' + searchin + '------'
                        print '-------' + library
                        searchinPart2 = ''
                        searchinPart3 = ''
                        searchinPart1 = searchin[0 : searchin.find(keyword)]
                        if haveUrl:
                            searchinPart2 = searchin[searchin.find(keyword) : searchin.find('>', searchin.find(keyword)) + 1]
                            searchinPart3 = searchin[searchin.find('>', searchin.find(keyword)) + 1 :]
                        else:
                            searchinPart2 = keyword + '<>'
                            searchinPart3 = searchin[searchin.find(keyword) + len(keyword.decode('utf-8')) :]
    
    
                        js = "editSearchinLink('" + searchinR.get_id().strip() + "', '" + rList[0][0] + "', '" + keyword + "', '" + searchinPart1 + "', '" + searchinPart2 + "', '" + searchinPart3 + "', '" + descPart + "', '" + library + "');"
                        searchResult += '<a href="javascript:void(0);" onclick="' + js + '">'
                        searchResult += self.getIconHtml('edit', width=10, height=8)
                        searchResult += '</a>'

                        js = "var postArgs = {'rID' : '" + searchinR.get_id().strip() + "', 'rTitle' : '" + searchinR.get_title().strip() + "', 'url' : '" + searchinR.get_url().strip() + "', 'title' : '" + keyword + "', 'searchinFieldTitle' : '" + keyword + "', 'resourceType' : '" + resourceType + "', 'library' : '" + library + "'};"
                        js += "$.post('/querySearchinField', postArgs, function(data) {"
                        js += "console.log('searchinFieldText', data);"
                        js += "editSearchinField('" + searchinR.get_id().strip() + "', '" + searchinR.get_title().strip() + "', '" + searchinR.get_url().strip() + "', '" + rList[0][0] + "', '" + keyword + "', '" + resourceType + "', '" + library + "', data);"
                        js += "})"
                        searchResult += '<a href="javascript:void(0);" onclick="' + js + '">'
                        searchResult += self.getIconHtml('edit2', width=10, height=8)
                        searchResult += '</a>'                
                #'''
                if layerName.startswith(':'):
                    engine = ''
                    if PrivateConfig.groupSearchDict.has_key(layerName):
                        engine = PrivateConfig.groupSearchDict[layerName]
                    else:
                        engine = layerName[1:].strip()
                    url = ''
                    urlList = []
                    if engine.startswith('d:'):
                        engineList = self.getTopEngin(engine, sort=True, number=5)
                        for e in engineList:
                            urlList.append(self.toQueryUrl(self.getEnginUrl(e), cmd[cmd.find('>') + 1 :]))   
                    else:
                        for e in engine.split(' '):
                            urlList.append(self.toQueryUrl(self.getEnginUrl(e), cmd[cmd.find('>') + 1 :]))
                    if len(urlList) < 3:
                        url = '*'.join(urlList)
                        searchResult += self.genPreviewLink('', cmd[cmd.find('>') + 1 :], url)
                    else:
                        url = ','.join(urlList)
                        js = "batchOpenUrls('" + url + "');"
                        searchResult += '<a href="javascript:void(0);" onclick="' + js + '">' + self.getIconHtml('', 'preview') + '</a>'


                searchResult += '<br><br><br></div>'
            
                #layerHeight = self.getDivHeight(self.clearHtmlTag(searchResult), 3, cmd, defaultHeight=60) - 20
                layerHeight = 40
                searchResult = searchResult.replace('#height', str(layerHeight))
            brCount = self.getBrCount(searchResult)
            if len(cmdList) >= 0:
                searchResultBRCountDict[cmd] = brCount
                searchResultDict[cmd] = searchResult 
                #result += '<div align="left" style="padding-left: 0; padding-top: 2px; width:455px; height:' + str(divHeight) + 'px; float:left;">'
            '''
            else:
                layerHeight = self.getDivHeight(self.clearHtmlTag(searchResult), brCount, cmd) - 100

                divPaddingLeft = divWidth

                if layerName != '':
                    divPaddingLeft = 20

                result += '<div align="left" style="margin-left:' + str(divMarginLeft)+ 'px; padding-left:' + str(divPaddingLeft) + 'px; padding-top: 2px; width:auto; ">'
                result += searchResult
                result += '</div>'
            '''
        if len(searchResultDict) > 0:
            count = 0
            divHeight = 455
            maxHeight = 0
            itemCache = []
            for item in sorted(searchResultBRCountDict.items(), key=lambda searchResultBRCountDict:int(searchResultBRCountDict[1]), reverse=True):
                count += 1
                print item
                cmd = item[0]
                brCount = item[1]
                brHeight = 20

                defaultHeight = 455
                if runCMD == False:
                    defaultHeight = 40
                divHeight = self.getDivHeight(self.clearHtmlTag(searchResultDict[item[0]]), brCount, cmd, defaultHeight=defaultHeight)


                #print 'cmd:' + cmd + ' brCount=' + str(brCount) + ' divHeight=' + str(divHeight) + ' lenght=' + str(lenght)

                if divHeight > maxHeight:
                    maxHeight = divHeight
                if runCMD == False and maxHeight > defaultHeight:
                    maxHeight = defaultHeight

                if count == 3:
                    itemCache.append(item)
                    layerHeight += maxHeight
                    for i in itemCache:
                        subSearchin = ''
                        borderStyle = ''
                        if layerName != '':
                            if runCMD and loadSubSearchin:
                                subSearchin = self.loadSubSearchin(i[0], i[0], divWidth, bkColor=bkColor, parentDivID=parentDivID)
                            borderStyle = 'border-style: groove;border-width: 2px;'

                        result += '<div align="left" style="border-radius:15px 15px 15px 15px; margin-left:' + str(divMarginLeft)+ 'px; padding-left: ' + str(divPaddingLeft) + 'px; padding-top: 2px; margin-bottom:2px; width:' + str(divWidth) + 'px; height:' + str(maxHeight + 5) + 'px; float:left; ' + borderStyle + '" onmouseout="normalColor(this, ' + "'" + bkColor + "'"+ ');" onmouseover="hover(this);" >'  
                        result += searchResultDict[i[0]]
                        result += subSearchin
                        result += '</div>'
                    itemCache = []
                    maxHeight = 0
                    count = 0
                else:
                    itemCache.append(item)

            if len(itemCache) > 0:
                layerHeight += maxHeight
                spaceSize = 3 - len(itemCache)
                for i in itemCache:
                    subSearchin = ''
                    borderStyle = ''

                    if layerName != '':
                        if runCMD and loadSubSearchin:
                            subSearchin = self.loadSubSearchin(i[0], i[0], divWidth, parentDivID=parentDivID)
                        borderStyle = 'border-style: groove;border-width: 2px;'
                    result += '<div align="left" style="border-radius:15px 15px 15px 15px; margin-left:' + str(divMarginLeft)+ 'px; padding-left: ' + str(divPaddingLeft) + 'px; padding-top: 2px; width:' + str(divWidth) + 'px; margin-bottom:2px; height:' + str(maxHeight + 5) + 'px; float:left; ' + borderStyle + '" onmouseout="normalColor(this, ' + "'" + bkColor + "'"+ ');" onmouseover="hover(this);">'  
                    result += searchResultDict[i[0]]
                    result += subSearchin
                    result += '</div>'
                if runCMD and layerName == '': 
                    for i in range(0, spaceSize):
                        result += '<div align="left" style="border-radius:15px 15px 15px 15px; margin-left:' + str(divMarginLeft)+ 'px; padding-left: ' + str(divPaddingLeft) + 'px; padding-top: 2px; width:' + str(divWidth) + 'px; margin-bottom:2px; height:' + str(maxHeight + 5) + 'px; float:left; ' + borderStyle + '" >'  
                        result += '</div>'

        totalLayerHeight = 0  
        marginBottom = 10                  
        if layerName != '':
            totalLayerHeight = layerHeight + 35
            borderStyle = ''
            borderWidth = 0
            if layerNoBorder == False:
                borderWidth = 2
            layerHtml = '<div align="left" style="background-color: ' + bkColor + '; margin-bottom:' + str(marginBottom) + 'px; padding-bottom: 15px;  border-radius:15px 15px 15px 15px; border-style: groove; border-width: ' + str(borderWidth) + 'px; padding-left: 0px; padding-right: 0px; padding-top: 2px; width:100%; height:' + str(totalLayerHeight) + 'px; float:left;">'  
            layerHtml += '<div align="center" style="border-style: groove; border-width: 0px; margin-left:5px; margin-right:8px; margin-bottom:2px; border-radius:10px 10px 10px 10px;">'
            if layer != '':
                if self.getValueOrTextCheck(layer):
                    layer = self.getValueOrText(layer, returnType='value').replace('&', '+').replace('@', '+')
                    layerList = self.layerText2LayerList(layer)
                    layer = ' + '.join(layerList) + '/:'

                #js = "typeKeyword('" + layer + "', '');"
                #js = "window.scrollTo(0, 0);var searchBox = document.getElementById('search_txt');searchBox.focus();setCaretPosition(searchBox, searchBox.value.length - 10);"
                js = "var searchBox = document.getElementById('search_txt');chanageLinkColor(this, '#E9967A', '');"
                layerText = layer
                if layerText.find('<http:') != -1 and layerText.find('>') != -1:
                    layerText = re.sub(r"<.*?>", "", layerText)
                layerHtml += '<a href="javascript:void(0);" onclick="' + js + '" style="color: rgb(153, 153, 102); font-size:9pt;" onmouseover="search_box.value=' + "'" + layerText + "';var searchBox = document.getElementById('search_txt'); lastHoveredUrl = '" + layer + "'; lastHoveredText = '" + layer.replace('/:', '').replace(' + >', '*').replace('>', '') + "'; lastHoveredCMD = '" + layerText + "'" + ';">'
            layerHtml += '<font style="color:#8178e8; font-size:15pt;">' + layerName + '</font>'

            layerjs = "showPopupContent(0, 20, 1440, 900, '" + layerText.replace('>', '#>').replace(' + ', '/: + ') + "');"
            layerHtml += '<a href="javascript:void(0);" onclick="' + layerjs + '" >' + self.getIconHtml('', 'url', width=10, height=8) + '</a>'

            if layer != '':
                layerHtml += '</a>'
            layerHtml += ':'
            #insert sublayer arrow here
            layerHtml += '</div>'
            layerHtml += result
            layerHtml += '</div>'

            result = layerHtml

        return result, totalLayerHeight + (marginBottom * 2)

    def layerText2LayerList(self, layer):
        layer = layer.replace('&', '+').replace('@', '+')
        layerList = []
        if layer.find('+') != -1:
            for item in layer.split('+'):
                if item.startswith('>!'):
                    item = item[item.find('(') + 1 :]
                if item.endswith(')'):
                    item = item[0 : len(item) - 1]
                layerList.append(item.strip())
        else:
            layerList.append(layer)
        return layerList

    def loadSubSearchin(self, cmd, parentOfSearchin, divWidth, bkColor='yellow', parentDivID=''):
        html = ''
        subSearchin = ''
 
        if self.searchinCache.has_key(cmd[1:]):
            subSearchin = self.searchinCache[cmd[1:]]
            print 'found:' + cmd[1:] + ' subSearchin:'+ subSearchin

        if subSearchin == '':
            return ''
        html += '<div width="' + str(divWidth)+ 'px" height="100px" align="center" style="background-color:' + bkColor + ';">'

        cmdList = subSearchin.split(',')
        if len(cmdList) == 3:
            cmdList.append('')
        for cmd in cmdList:
            cmd = cmd.strip()
            subDivWidth = divWidth / 3  - 15
            subDivHeight = 20
            if len(cmdList) > 3:
                subDivHeight = 70
                subDivWidth = divWidth / 3  - 15
                if len(cmdList) < 6:
                    subDivHeight = subDivHeight / (len(cmdList) / 3)
                else:
                    subDivHeight = subDivHeight / (len(cmdList) / 3)
                    subDivHeight = (subDivHeight * (len(cmdList) / 3)) / 3
 
            elif len(cmdList) == 3:
                subDivHeight = 30
                subDivWidth = divWidth   - 15
            elif len(cmdList) == 2:
                subDivWidth = divWidth / 2  - 15
                subDivHeight = 30
            else:
                subDivWidth = divWidth  - 15
                subDivHeight = 60
            bkColor = '#EEFFEE'
            if cmd != '':
                html += '<div align="center"  style="width:' + str(subDivWidth) + 'px; height:' + str(subDivHeight) + 'px; background-color:' + bkColor + '; border-style: groove; border-width: 1px;text-align:center;line-height:' + str(subDivHeight) +'px;float:left; border-style: solid; margin-bottom:5px; margin-right:5px;" onmouseout="normalColor(this, ' + "'" + bkColor + "'"+ ');" onmouseover="hover(this);">'
            else:
                html += '<div align="center"  style="width:' + str(subDivWidth) + 'px; height:' + str(subDivHeight) + 'px; background-color:white; visibility:hidden; border-style: groove; border-width: 1px;text-align:center;line-height:' + str(subDivHeight) +'px;float:left; border-style: solid; margin-bottom:5px; margin-right:5px;" onmouseout="normalColor(this, ' + "'" + bkColor + "'"+ ');" onmouseover="hover(this);">'

            #js = "typeKeyword('" + cmd + "', '" + parentOfSearchin + "');"
            #js = "showPopupContent(0, 200, 1444, 800, '" + cmd + "'); window.scrollTo(0, 200); "
            

            js = "showPopupContent(pageX, pageY, 550, 480, '#" + cmd + "/:');"
            js2 = "lastHoveredUrl = '" + cmd + "'; lastHoveredText = '" + cmd[cmd.find('>') + 1 :] + "'; search_box.value='" + cmd + "/:';"
            
            showText = cmd[1:]
            layerList = []
            if cmd.startswith('&>!'):
                showText = self.getValueOrText(cmd, returnType='text')[3:]
                newCMD = self.getValueOrText(cmd, returnType='value').strip()

                layerList = self.layerText2LayerList(newCMD)
                if len(layerList) < 7:
                    newCMD = ' + '.join(layerList) + '/:/:group ' + showText
                else:
                    newCMD = ' + '.join(layerList) + '/:/:group-short ' + showText

                js = "showPopupContent(0, 200, 1444, 800, '" + newCMD + "'); window.scrollTo(0, 200); "
                js2 = "lastHoveredUrl = '" + newCMD + "'; lastHoveredText = '" + self.getValueOrText(cmd, returnType='value').replace('&>', '*').replace('>', '') + "'; lastHoveredCMD = '" + newCMD + "'; search_box.value='" + newCMD + "';"

            elif cmd.startswith('&>'):
                showText = self.getValueOrText(cmd, returnType='text')[2:]
            if showText.startswith('!'):
                showText = showText[1:]
            #if parentDivID != "":
                
                #js = "typeKeywordEx('>" + showText + "/:','" + parentOfSearchin + "', false, '" + parentDivID + "');"
                #html += '<a href="javascript:void(0);" onclick="' + cmdjs + '" style="color:131c0c;">' + self.getIconHtml('', 'command', width=10, height=8) + '</a>'
            html += '<a href="javascript:void(0);" onclick="' + js + '" onmouseover="' + js2 + '" style="color:131c0c;">' + showText + '</a>'

            if len(layerList) > 0:
                if parentDivID == "":
                    parentDivID = "filter-div-" + parentOfSearchin.strip().lower().replace(" ", "-").replace(">", "") + "-0" 
                cmd =  ' + '.join(layerList) + '/:'
                js = "typeKeywordEx('" + cmd  + "','" + parentOfSearchin + "', false, '" + parentDivID + "');"
                icon = self.getIconHtml('', 'group', width=10, height=8) 
                html += '<a href="javascript:void(0);" onclick="' + js+ '" style="color:131c0c;">' + icon + '</a>'
            #if len(layerList) > 0:

            #js3 = "showPopupContent(pageX, pageY, 550, 480, '#" + cmd + "/:');"
            #html += '<a href="javascript:void(0);" onclick="' + js3 + '" >' + self.getIconHtml('', 'tabs', width=10, height=8) + '</a>'
            html += '</div>'
        html +='</div>'
        return html


    def getBrCount(self, html):
        brCount = 0
        brIndex = 0
        while True:
            brIndex = html.find('<br>', brIndex)
            if brIndex != -1:
                brIndex += 5
                brCount += 1
            else:
                break

        return brCount

    def getDivHeight(self, text, brCount, cmd, defaultHeight=455):
        brHeight = 20
        divHeight = defaultHeight
        lenght = len(self.clearHtmlTag(text))

        if lenght > 1200:
            brHeight = 36
        elif lenght > 600:
            brHeight = 33
        if brCount > 0:
            divHeight = brCount * brHeight

        if cmd != '':
            if cmd.find('>') != -1:
                cmd = cmd[cmd.find('>') + 1:]
            if self.searchinCache.has_key(cmd):
                cmdSearchinList = self.searchinCache[cmd].split(',') 
                if len(cmdSearchinList) == 1:
                    divHeight += 75
                else:
                    divHeight += ((len(cmdSearchinList) / 3) + 1) * 30
        return divHeight
    def genCrossrefHtml(self, rid, aid, tag, content, library, split_char=','):
        html = ''
        if content.find('#') != -1:           
            result = self.getCrossrefUrls(content).items()
            for ft, link in result:
                text = '<font style="font-size:10pt;">' + ft + '</font>'
                db = content[0 : content.rfind('/') + 1].strip()
                if db.find('library/') != -1:
                    text = '<font style="font-size:10pt; color="red">' + ft[0:1] + '</font>' + '<font style="font-size:10pt;">' + ft[1:] + '</font>'
                html += self.enhancedLink(link, text, module='main', library=library, rid=rid, resourceType=tag, urlFromServer=False, dialogMode=False, aid=aid)
                if ft != result[len(result) -1][0]:
                    html += split_char + '&nbsp;'
                #if ft != filters[len(filters) -1]:
                #    html += '<br>'
        else:
            key, url = self.getCrossrefUrl(content) 

            html += self.enhancedLink(url, '<font style="font-size:10pt;">' + key + '</font>', module='main', library=library, rid=rid, resourceType=tag, urlFromServer=False, dialogMode=False, aid=aid) 

        return html 

    def getCrossrefUrls(self, content):
        data = content.strip().split('#')
        result = {}
        if len(data) < 2:
            return result
        filters = []
        if data[1].find('+') != -1:
            filters = data[1].split('+')
        else:
            filters = [data[1]]

        db = data[0][0 : data[0].rfind('/') + 1].strip()
        key = data[0][data[0].rfind('/') + 1 :].strip()
        for ft in filters:
            #print ft + '<br>'
            link = 'http://' + Config.ip_adress + '/?db=' + db + '&key=' + key + '&filter=' + ft
            result[ft] = link

        return result     

    def getCrossrefUrl(self, content):
        db = content[0 : content.rfind('/') + 1].strip()
        key = content[content.rfind('/') + 1 :].strip()
        if key.find('#') != -1:
            key = key.replace('#', '&filter=')
        link = 'http://' + Config.ip_adress + '/?db=' + db + '&key=' + key 
        return key, link

    def next_pos(self, text, start, titleLen, keywordList, htmlStyle=True, library='', shortPos=True):
        min_end = len(text)
        c_len = titleLen
        if htmlStyle:
            c_len = titleLen + 10
        for k in keywordList:
            end = text.find(' ' + k, start + 2)
            if text.find(' ' + k + ' ', end) != -1:
                continue
            if end != -1 and end + 1 < min_end:
                end += 1
                min_end = end

        if min_end == len(text) or shortPos:
            return min_end


        if min_end < len(text):
            startTag = text[start : text.find(':', start) + 1]
            smart_link_str = ' '.join(self.tag.get_list_smart_link(library))
            account_str = ' '.join(self.tag.tag_list_account.keys())

            if smart_link_str.find(startTag) != -1 or account_str.find(startTag) != -1:
                return min_end -1

            min_end -= 1
            if min_end - start > c_len:
                ret_end = start + c_len
                return self.space_end(text, start, ret_end, c_len, htmlStyle=htmlStyle)
            else:
                return min_end 

        if (len(text) - start) < c_len:
            return start + len(text) - start
        else:
            ret_end = start + c_len
            return self.space_end(text, start, ret_end, c_len, htmlStyle=htmlStyle)
           
    def space_end(self, text, start, end, c_len, htmlStyle=True): 
        if htmlStyle == False:
            return end

        ret_end1 = end
        ret_end2 = end
        while ret_end1 >= 0 and ret_end1 < len(text) and text[ret_end1] != ' ':
            ret_end1 -= 1
        if ret_end1 < 0:
            return 0
        while ret_end2 >= 0 and ret_end2 < len(text) and text[ret_end2] != ' ':
            ret_end2 += 1
        if ret_end2 >= len(text):
            return len(text)
        
        if (end - ret_end1) > (ret_end2 - end):
            return ret_end2
        if (ret_end2 - start) <= c_len:
            return ret_end2
        else:
            return ret_end1


    def icon_keyword(self, text, keywordList, isTag=True, color="#66CCFF", rawText='', parentOfSearchin='', title='', parentDivID=''):
        result = text
        #print len(keywordList)
        
        for k in keywordList:
            if isTag:
                k = ' ' + k
                if result.find(k + ' ') != -1:
                    continue
            if result.find(k) == -1:
                continue
            k = k.strip()

            print "isTag:" + str(isTag)
            print "k:" + k
            #print  "text:" + text

            if Config.website_icons.has_key(k.replace(':', '')):
                script = ''
                if rawText != '':
                    tagStr = rawText[0 : rawText.find(':') + 1].strip()
                    tagValue = rawText[rawText.find(':') + 1 : ]
                    valueList = tagValue.split(',')
                    #print tagStr
                    if len(valueList) > 1 and len(valueList) < 6 and tagStr == 'website:':
                        #if tagStr == 'website:':
                        urlList = []
                        textList = []
                        for item in valueList:
                            item = item.strip()
                            if self.getValueOrTextCheck(item):
                                url = self.getValueOrText(item, returnType='value')
                                textList.append(self.getValueOrText(item, returnType='text'))
                            else:
                                url = self.toQueryUrl(self.getEnginUrl('glucky'), item)
                                textList.append(item)
                            urlList.append(url)
                        script = ''
                        if False and Config.open_all_link_in_one_page:
                            script = "openAllOnePage('" + ','.join(textList) + "', '" + ','.join(urlList) + "', 'searchbox');"
                        else:
                            script = "batchOpenUrls('" + ','.join(urlList) + "');"
                    else:
                        if parentOfSearchin != '':
                            if title == '':
                                title = parentOfSearchin
                            tagStrKeyword = tagStr[0 : tagStr.find(":")]
                            if parentOfSearchin.startswith(">") or parentOfSearchin.startswith("#>"):
                                #if parentDivID != "":
                                script = "typeKeywordEx('>" + title + "/" + tagStr + " + " + tagStrKeyword + "','" + parentOfSearchin + "', false, '" + parentDivID + "');"
                                #else:
                                #    script = "typeKeywordEx('>" + title + "/" + tagStr + " + " + tagStrKeyword + "','" + parentOfSearchin + "');"
                            else:
                                script = "typeKeyword('>" + title + "/" + tagStr + " + " + tagStrKeyword + "','" + parentOfSearchin + "');"

                image = "<img src=" + Config.website_icons[k.replace(':', '')] + ' width="14" height="12" style="border-radius:10px 10px 10px 10px; opacity:0.7;">'
                
                if script != '':
                    lastHoveredText = ''
                    lastHoveredUrl = ''
                    for v in valueList:
                        v = v.strip()
                        if self.getValueOrTextCheck(v):
                            lastHoveredText += self.getValueOrText(v, returnType='text').strip()
                        else:
                            lastHoveredText += v.strip()


                        if self.isAccountTag(k, self.tag.tag_list_account):
                            accountUrl = self.tag.tag_list_account[k]
                            newV = v
                            if self.getValueOrTextCheck(v):
                                newV = self.getValueOrText(v, returnType='value').strip()
                            url = self.toQueryUrl(accountUrl, newV)
                            lastHoveredUrl += url
                        elif k == 'website:':
                            lastHoveredUrl += self.getValueOrText(v, returnType='value').strip()

                        if v != valueList[len(valueList) - 1]:
                            lastHoveredText += '*'
                            if lastHoveredUrl.strip() != '':
                                lastHoveredUrl += '*'
                    if lastHoveredText.endswith('*'):
                        lastHoveredText = lastHoveredText[0 : len(lastHoveredText) - 1]
                    if lastHoveredUrl.endswith('*'):
                        lastHoveredUrl = lastHoveredUrl[0 : len(lastHoveredUrl) - 1]
                    onmouseover = "lastHoveredText = '" + lastHoveredText + "'; lastHoveredUrl = '" + lastHoveredUrl+ "'; lastHoveredCMD = '" + parentOfSearchin + "/" + tagStr + "/';"
                    image = '<a href="javascript:void(0);" onclick="' + script + '" onmouseover="' + onmouseover + '">' + image + '</a>'
                result = self.replacekeyword(result, k, image + ':')

            else:

                result = self.replacekeyword(result, k, '<font color="' + color + '">' + k + '</font>')
        #print result
        return result.encode('utf-8')

   
    def color_keyword(self, text, keywordList, color_index=0, html_style=True, isTag=True, color1="#33EE22", color2="#66CCFF"):
        result = text
        for k in keywordList:
            if isTag:
                k = ' ' + k
                if result.find(k + ' ') != -1:
                    continue
            if result.find(k) == -1:
                continue
            k = k.strip()
            if (color_index - 1) % 2 == 0:
                if html_style == True:
                    result = self.replacekeyword(result, k, '<font color="' + color1 + '">' + k + '</font>')
                else:
                    result = result.replace(k, self.getColorStr('brown', k))
            else:
                if html_style == True:
                    result = self.replacekeyword(result, k, '<font color="' + color2 + '">' + k + '</font>')
                else:
                    result = result.replace(k, self.getColorStr('darkcyan', k))

        return result.encode('utf-8')

    def replacekeyword(self, data, k, colorKeyword):
        data = data.replace(' ' + k, ' ' + colorKeyword)
        data = data.replace(' ' + k[0 : 1].upper() + k[1:] + ' ', ' ' + colorKeyword)
        data = data.replace(' ' + k[0 : 1].upper() + k[1:], ' ' + colorKeyword)
        data = data.replace(' ' + k.upper(), ' ' + colorKeyword)
        return data

    def find_file_by_pattern(self, pattern='.*', base=".", circle=True):
        re_file = re.compile(pattern, re.I)
        #print pattern
        if base == ".":
            base = os.getcwd()
    
        final_file_list = []
        #print base  
        cur_list = []
        if os.path.isdir(base):
            cur_list = os.listdir(base)
        #print cur_list
        for item in cur_list:
            if item == ".svn" or item == ".git" or item == ".DS_Store":
                continue
    
            full_path = os.path.join(base, item)
            #print full_path
            if os.path.isfile(full_path) and full_path.find('db/') != -1:
                #print full_path
                '''
                with open(full_path, 'r+') as f:
                    try:
                        data = mmap.mmap(f.fileno(), 0)
                        if re_file.search(data):
                            final_file_list.append(full_path)
                    except Exception as e:
                        print str(e) + full_path
                '''
                p = self.find_file_by_pattern_path(re_file, full_path)
                if p != '':
                    final_file_list.append(p)

            else:
                final_file_list += self.find_file_by_pattern(pattern, full_path)
        return final_file_list

    def find_file_by_pattern_path(self, re, path):
        print path
        if os.path.exists(path) == False:
            return ''
        with open(path, 'r+') as f:
            try:
                data = mmap.mmap(f.fileno(), 0)
                if re.search(data):
                    return path
            except Exception as e:
                print str(e) + path
        return ''

    def sortLines(self, lines):
        if len(lines) > 0:
            record_list = []
            for line in lines:
                record_list.append(PaperRecord(line))
            if lines[0].find('published:') != -1:
                self.quickSort(record_list)
            else:
                 self.quickSort(record_list, 'id')
            ret_lines = []
            for r in record_list:
                ret_lines.append(r.line)

            return ret_lines
        else:
            return lines

    def sortRecords(self, records, sortType=''):
        return self.quickSort(records)

    def largeoreq(self, item1, item2, sortType):
        if sortType == "published":
            return item1.get_published().strip() >= item2.get_published().strip()
        #elif sortType == "title":
        #    t1 = item1.get_title().strip()[0 : 1].lower()
        #    t2 = item2.get_title().strip()[0 : 1].lower()
        #    return t1 >= t2

        else:
            return item1.get_id().strip() >= item2.get_id().strip()

    def lessoreq(self, item1, item2, sortType):
        if sortType == "published":
            return item1.get_published().strip() <= item2.get_published().strip()
        #elif sortType == "title":
        #    t1 = item1.get_title().strip()[0 : 1].lower()
        #    t2 = item2.get_title().strip()[0 : 1].lower()
        #    return t1 <= t2
        else:
            return item1.get_id().strip() <= item2.get_id().strip()

    def quickSort(self, alist, sortType="published"):
        self.quickSortHelper(alist,0,len(alist)-1, sortType)

    def quickSortHelper(self, alist,first,last, sortType):
        if first<last:

            splitpoint = self.partition(alist,first,last, sortType)

            self.quickSortHelper(alist,first,splitpoint-1, sortType)
            self.quickSortHelper(alist,splitpoint+1,last, sortType)

    def getIconHtml(self, url, title='', desc='', parentDesc='', width=14, height=12, radius=True, convertableCheek=False, highLightText='', filterText='', parentOfSearchin=''):
        #url = url.lower()
        if url.find('*') != -1:
            urls = url.split("*")
            count = len(urls)
            if (urls[count -1] == ""):
                count -= 1
            if highLightText.find("+") != -1:
                highLightTextTemp = ''
                for item in highLightText.split("+"):
                    if item.find(":") != -1:
                        continue
                    highLightTextTemp += item.strip().lower() + "+"
                if highLightTextTemp != '':
                    highLightText = highLightTextTemp
            clickJS = ''
            html = ''
            if filterText != '' and parentOfSearchin != '':
                clickJS = "tabsPreviewEx(this, '', '" + url.replace("www.", '') + "', '" + highLightText + "', '" + filterText + "', '" + parentOfSearchin + "');"
                html = '<a href="javascript:void(0);" onclick="' + clickJS + '">' + self.genIconHtml(Config.website_icons['tabs'], 0, width, height) + '</a> <font style="font-size:7pt; font-family:San Francisco;">' + str(count) + '</font>'
                if url.endswith("*"):
                    parentDivID = 'filter-div-' + parentOfSearchin.strip().lower().replace(" ", '-') + "-0"
                    if highLightText == parentOfSearchin:
                        parentDivID = 'filter-div-combine-result-0'
                    html += '<a href="javascript:void(0);" onclick="' + "typeKeywordEx('??" + title + "','', false, '" + parentDivID + "');" + '">' + self.getIconHtml('', 'command', width=11, height=9) + '</a>'
                
            else:
                clickJS = "tabsPreview(this, '', '" + url.replace("www.", '') + "', '" + highLightText + "');"
                html = '<a href="javascript:void(0);" onclick="' + clickJS + '">' + self.genIconHtml(Config.website_icons['tabs'], 0, width, height) + '</a> <font style="font-size:7pt; font-family:San Francisco;">' + str(count) + '</font>'
            return html
        #print 'getIconHtml:' + url
        originUrl = url
        if Config.enable_website_icon == False:
            return ''
        if os.path.isdir(url):
            url += '.dir'
            radius = False
            #print url

        if url.startswith('http') == False and parentDesc != '' and title != '':
            #print desc + '--->'
            #print parentDesc + '-->'
            #print title
            if parentDesc.lower().find(' ' + title.lower().strip() + '(') != -1:
                return self.genIconHtml(Config.website_icons['idea'], radius, width, height)
        src = ''
        if url.startswith('http') and url.endswith('btnI=1') == False:
            url = url[0 : url.find('/', url.find('//') + 2)]

        if url != '' and Config.website_icons.has_key(url):
            return self.genIconHtml(Config.website_icons[url], radius, width, height)
        elif title != '' and Config.website_icons.has_key(title):
            return self.genIconHtml(Config.website_icons[title], radius, width, height)
        else:

            if self.isShortUrl(url) and title != '':
                url = title
            for k, v in Config.website_icons.items():
                if url.lower().find(k.lower()) != -1:
                    src = v
                    break
            if url != '':
                if convertableCheek and self.urlConvertable(url, originUrl=originUrl) and url.find(Config.ip_adress) == -1:
                    html = ''
                    if src != '':
                        html = self.genIconHtml(src, radius, width, height)
                    js = "exclusiveEx('exclusive', '" + title + '(' + originUrl + ')' + "', '', true, '', '', '', '', false, 'convert');"
                    html += '<a href="javascript:void(0);" onclick="' + js + '">' + self.genIconHtml(Config.website_icons['data'], radius, width, height) + '</a>'
                    return html

                

            return self.genIconHtml(src, radius, width, height)


    def urlSearchable(self, url):
        #print 'urlSearchable:' + url

        for engine, engineUrl in self.search_engin_url_dict.items():
            if url.find(engine) != -1:
                return engineUrl
        return ''

    def urlConvertable(self, url, originUrl=''):
        #print 'urlConvertable:' + url

        for item in PrivateConfig.convert_dict.items():

            if item[0].find('/') != -1 and originUrl != '':
                if originUrl.find(item[0]) != -1:
                    return True
            elif url.find(item[0]) != -1:
                return True
        '''
        for key in urlPart.split('.'):
            if key == 'www' or key == 'com' or key == 'net' or key == 'org':
                continue
            if PrivateConfig.convert_dict.has_key(key):       
                return True
        '''

        return False

    def urlCrawler(self, url, sort=True):
        if url.find("github.com") != -1 or url.find("hellogithub.com") != -1:
            readmeUrl = url
            if url.find("github.com") != -1 and url.find("hellogithub.com") == -1:
                repo = url[url.find("com/") + 4 :]
                readmeUrl = "https://raw.githubusercontent.com/" + repo + "/master/README.md"

            print readmeUrl

            r = requests.get(readmeUrl)
            #print r.text

            pattern = ''
            if url.find("hellogithub.com") != -1:
                pattern = re.compile(r'"https://github.com/.*?/.*?"')   # 查找数字
            else:    
                pattern = re.compile(r'\(https://github.com/.*?/.*?\)')   # 查找数字
            result = pattern.findall(r.text)
            repoDict = {}
            repoList = []
            for url in result:
                print url
                if url.find("https://", url.find("https://") + 8) != -1 or url.find("http://", url.find("https://") + 8) != -1:
                    continue
                if url.find("sponsors/") != -1 or url.find("topics/") != -1:
                    continue
                url = url[1 : len(url) - 1]
                repo = url[url.find("com/") + 4 :]
                if repo.find("//") != -1:
                    repo = repo.replace("//", "/")
                if repo.endswith("/"):
                    repo = repo[0 : len(repo) - 1]
                if repo.find("/") != -1:
                    if repo.find("/", repo.find("/") + 1) != -1:
                        repo = repo[0 : repo.find("/", repo.find("/") + 1)]
                else:
                    continue
                if repoDict.has_key(repo) == False:
                    repoDict[repo] = repo
                    repoList.append(repo)
                else:
                    continue
            if sort and len(repoList) > 0:
                repoList = self.sortReposByStar(repoList)


            return repoList
        return []

    def sortReposByStar(self, repoList):
        url = "https://ungh.unjs.io/stars/" + "+".join(repoList).replace(" ", '')
        print url
        r = requests.get(url)
        jobj = None
        try:
            jobj = json.loads(r.text)
        except:
            return repoList

        repoDict = {}
        if jobj.has_key("stars") == False:
            return repoList
        for k, v in jobj['stars'].items():
            repoDict[k] = v

        print repoDict
        if len(repoDict) > 0:
            repoList = []
            for item in sorted(repoDict.items(), key=lambda repoDict:int(repoDict[1]), reverse=True):
                repoList.append(item[0])
        return repoList


    def getUrlDomain(self, url):
        domain = url
        if url.find(":") != -1:
            domain = url[url.find(":") + 3 :]
        if domain.find("/") != -1:
            domain = domain[0 : domain.find("/")]

        if domain.startswith('www.'):
            domain = domain[4:]
        return domain


    def genFilterUrlHtml(self, urls, urlFilter):
        print(urls)
        print("urlFilter:" + urlFilter)

        if urlFilter == "":
            return ''
        if urlFilter.find("-") != -1:
            parts = urlFilter.split("-")
            if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                start = int(parts[0])
                end = int(parts[1])
                if start > end or start > len(urls) or end > len(urls):
                    return ""
                else:
                    return "*".join(urls[start - 1 : end])


        result = []
        filters = []
        if urlFilter.find("+") != -1:
            filters = urlFilter.split("+")
        else:
            filters = [urlFilter]
        for url in urls:
            url = url.strip()
            for ft in filters:
                ft = ft.strip()
                if url.lower().find(ft.lower()) != -1:
                    result.append(url)
                    break;

        return "*".join(result)

    def genKeywordsInfoHtml(self, urls, urlFilter='', parent=''):
        print(urls)
        html = ''

        keywordsDict = {}
        for url in urls:
            url = url.replace("http://", '').replace("https://", '').replace("www.", '').replace(".com", '').strip()
            keywords = url.split("/")
            for key in keywords:
                key = key.strip()
                if key == "" or len(key) < 4 or (len(key) > 20 and key.find("-") == -1 and key.find(".") == -1):
                    continue
                if keywordsDict.has_key(key) == False:
                    keywordsDict[key] = url
        html = '<div align="center">'
        for key in keywordsDict.keys():
            if parent != '':
                cmd = '>' + parent + "/" + key
                if self.isAccountTag(key + ":", self.tag.tag_list_account):
                    cmd = '>' + parent + "/" + key[0 : len(key) - 1] + " %2B " + key + " ; " + '>' + parent + "/" + key + ":"
                js = "showPopupContent(pageX, pageY, 600, 480, '" + cmd.replace('%2B', '+') + "');"
                js2 = "onHover('-website-26', '" + key + "', '" + key + "', '', 'searchbox', '', 'false');"
                html += '<a href="javascript:void(0);" onclick="' + js + '"; onmouseover="' + js2 + '">' + '<font style="color: rgb(0, 0, 0); font-size:9pt;">' + key + '</font>' + '</a> '
                html += '<a href="javascript:void(0);" onclick="' + "window.open('" + "http://" + Config.ip_adress + "/getPluginInfo?cmd=" + cmd + "');" + '"><img src="https://cdn3.iconfinder.com/data/icons/iconano-web-stuff/512/109-External-512.png" width="12" height="10" style="border-radius:10px 10px 10px 10px; opacity:0.7;"></a> '
                html += '<a href="javascript:void(0);" onclick="' + "window.open('" + "http://" + Config.ip_adress + "/getPluginInfo?cmd=??" + key + "');" + '"><img src="https://cdn3.iconfinder.com/data/icons/iconano-web-stuff/512/109-External-512.png" width="12" height="10" style="border-radius:10px 10px 10px 10px; opacity:0.7;"></a>'
                if key.find(".") != -1 or key.find("-") != -1:
                    items = []
                    if key.find(".") != -1:
                        items = key.split(".")
                    elif key.find("-") != -1:
                        items = key.split("-")
                    html += '('
                    for key in items:
                        cmd = '>' + parent + "/" + key
                        if self.isAccountTag(key + ":", self.tag.tag_list_account):
                            cmd = '>' + parent + "/" + key[0 : len(key) - 1] + " %2B " + key + " ; " + '>' + parent + "/" + key + ":"
                        js = "showPopupContent(pageX, pageY, 600, 480, '" + cmd.replace('%2B', '+') + "');"
                        js2 = "onHover('-website-26', '" + key + "', '" + key + "', '', 'searchbox', '', 'false');"
                        html += ' <a href="javascript:void(0);" onclick="' + js + '"; onmouseover="' + js2 + '">' + '<font style="color: rgb(0, 0, 0); font-size:9pt;">' + key + '</font>' + '</a> '
                        html += '<a href="javascript:void(0);" onclick="' + "window.open('" + "http://" + Config.ip_adress + "/getPluginInfo?cmd=" + cmd + "');" + '"><img src="https://cdn3.iconfinder.com/data/icons/iconano-web-stuff/512/109-External-512.png" width="12" height="10" style="border-radius:10px 10px 10px 10px; opacity:0.7;"></a> '
                        html += '<a href="javascript:void(0);" onclick="' + "window.open('" + "http://" + Config.ip_adress + "/getPluginInfo?cmd=??" + key + "');" + '"><img src="https://cdn3.iconfinder.com/data/icons/iconano-web-stuff/512/109-External-512.png" width="12" height="10" style="border-radius:10px 10px 10px 10px; opacity:0.7;"></a>'
                    html += ")"
                html += "  "
        return html + '</div>'

    def sortUrls(self, urls, fter='', parent=''):

        urls = sorted(urls)

        return "*".join(urls)


    def genGroupInfoHtml(self, urls, urlFilter='', parent='', fter=''):
        print(urls)
        print("urlFilter:" + urlFilter)
        urls = sorted(urls)
        domainFilter = ''
        if urlFilter != '':
            domainFilter = self.getUrlDomain(urlFilter)

        domainDict = {}
        for url in urls:
            domain = self.getUrlDomain(url)
            if domainDict.has_key(domain):

                domainDict[domain].append(url)
            else:
                domainDict[domain] = [url]

        print(domainDict)
        print('domainFilter:' + domainFilter)

        html = '<div align="center">'
        #if len(domainDict.keys()) == 1:
        #    return ''
        if fter != '' and parent != '':
            key = fter
            cmd = '>' + parent + "/" + key
            js = "showPopupContent(pageX, pageY, 600, 480, '" + cmd + "');"
            js2 = "onHover('-website-26', '" + key + "', '" + key + "', '', 'searchbox', '', 'false');"
            html += '<a href="javascript:void(0);" onclick="' + js + '"; onmouseover="' + js2 + '">' + '<font style="color: rgb(0, 0, 0); font-size:9pt;">' + key + '</font>' + '</a> '
            html += '<a href="javascript:void(0);" onclick="' + "window.open('" + "http://" + Config.ip_adress + "/getPluginInfo?cmd=>" + parent + '/' + key + "');" + '"><img src="https://cdn3.iconfinder.com/data/icons/iconano-web-stuff/512/109-External-512.png" width="12" height="10" style="border-radius:10px 10px 10px 10px; opacity:0.7;"></a> '
            html += '<a href="javascript:void(0);" onclick="' + "window.open('" + "http://" + Config.ip_adress + "/getPluginInfo?cmd=??" + key + "');" + '"><img src="https://cdn3.iconfinder.com/data/icons/iconano-web-stuff/512/109-External-512.png" width="12" height="10" style="border-radius:10px 10px 10px 10px; opacity:0.7;"></a>'
            if key.find("/") != -1:
                items = key.split("/")
                html += '('
                for key in items:
                    cmd = '>' + parent + "/" + key
                    if self.isAccountTag(key + ":", self.tag.tag_list_account):
                        cmd = '>' + parent + "/" + key[0 : len(key) - 1] + " %2B " + key + " ; " + '>' + parent + "/" + key + ":"
                    js = "showPopupContent(pageX, pageY, 600, 480, '" + cmd.replace('%2B', '+') + "');"
                    js2 = "onHover('-website-26', '" + key + "', '" + key + "', '', 'searchbox', '', 'false');"
                    html += ' <a href="javascript:void(0);" onclick="' + js + '"; onmouseover="' + js2 + '">' + '<font style="color: rgb(0, 0, 0); font-size:9pt;">' + key + '</font>' + '</a> '
                    html += '<a href="javascript:void(0);" onclick="' + "window.open('" + "http://" + Config.ip_adress + "/getPluginInfo?cmd=" + cmd + "');" + '"><img src="https://cdn3.iconfinder.com/data/icons/iconano-web-stuff/512/109-External-512.png" width="12" height="10" style="border-radius:10px 10px 10px 10px; opacity:0.7;"></a> '                        
                    html += '<a href="javascript:void(0);" onclick="' + "window.open('" + "http://" + Config.ip_adress + "/getPluginInfo?cmd=??" + key + "');" + '"><img src="https://cdn3.iconfinder.com/data/icons/iconano-web-stuff/512/109-External-512.png" width="12" height="10" style="border-radius:10px 10px 10px 10px; opacity:0.7;"></a>'
                html += ")"
            html += "<br>"

        for item in sorted(domainDict.items(), key=lambda domainDict:len(domainDict[1]), reverse=True):
            k = item[0].strip()
            v = item[1]
            if k == '':
                continue

            if domainFilter != '':
                if domainFilter.lower() != k.lower():
                    continue
                else:
                    return "*".join(v)

            if domainFilter == '':
                #'''
                if parent != '':
                    cmd = '>' + parent + "/" + k
                    if k.find(".") != -1 and self.isAccountTag(k[0 : k.find(".")], self.tag.tag_list_account):
                            cmd += '; >' + parent + '/' + k[0 : k.find(".")] + ':'
                    #js = "typeKeywordEx('" + cmd + "', '>" + parent + "', false, '');";
                    js = "showPopupContent(pageX, pageY, 600, 480, '" + cmd + "');"
                    html += '<a href="javascript:void(0);" onclick="' + js + '">' + '<font style="color: rgb(0, 0, 0); font-size:9pt;">' + k + '</font>' + '</a>'
                else:
                    html += '<font style="color: rgb(0, 0, 0); font-size:9pt;">' + k + '</font>'
                #'''
                #html += '<font style="color: rgb(0, 0, 0); font-size:9pt;">' + k + '</font>'
            js = "tabsPreviewEx(this, '', '" + "*".join(v) + "', '', 'urlFilter', '" + parent + "');"
            html += self.genJsIconLinkHtml(js, Config.website_icons["tabs"]) + ' <font style="font-size:7pt; font-family:San Francisco;">' + str(len(v)) + '</font>'

            js2 = ''
            #for domain process
            if k == "github.com":
                js = ''
                repos = []
                for url in v:
                    url = url.strip()
                    if url.find("://") != -1:
                        url = url[url.find("://") + 3 :]
                    if url.endswith("/"):
                        url = url[0 : len(url) -1]
                    print("xx " + url)
                    if len(url.split("/")) == 3:
                        js += "window.open('https://" + url + '/releases' + "');"
                        repos.append(url[url.find(".com/") + 5 :])

                if js != '':
                    js += "hiddenPopup();";
                    html += ' <a href="javascript:void(0);" onclick="' + js + '"><img src="https://cdn2.iconfinder.com/data/icons/agile-methodology-14/64/release-icon-512.png" width="12" height="10" style="border-radius:10px 10px 10px 10px; opacity:0.7;"></a>'
                    js = "onRepoPreview('" + '*'.join(repos) + "');"
                    html += self.genJsIconLinkHtml(js, Config.website_icons["crawler"])

            for url in v:
                js2 += "window.open('" + url.strip() + '' + "');"
            if js2 != '':
                html += ' <a href="javascript:void(0);" onclick="' + js2 + '">' + self.getIconHtml('', 'url', width=12, height=10) + '</a>'

            html += ' '
        return html + '</div>'


    def genRepoHtml(self, repoList, sort=True):
        html = ""
        if len(repoList) > 0:
            html += '<div align="left">'
            html += '<img src="https://cdn2.iconfinder.com/data/icons/black-white-social-media/64/social_media_logo_github-128.png" width="14" height="12" style="border-radius:10px 10px 10px 10px; opacity:0.7;">:'
            if sort:
                repoList = self.sortReposByStar(repoList)
        for repo in repoList:
            repo = repo.strip()
            showText = self.getLinkShowText(True, repo, "github", len(repoList), fontScala=-3)
            html += self.enhancedLink("https://github.com/" + repo, repo, showText=showText)
            html += self.genPreviewLink('', repo, self.getPreviewUrl("github", "https://github.com/" + repo))
            html += self.genCrawlerPreviewLink('', repo, "https://github.com/" + repo, '')
            html += self.genDoexclusiveLink('github', repo, "https://github.com/" + repo[0 : repo.find("/")], "")
            html += self.extensionManager.getExtensionHtml('github', repo, "https://github.com/" + repo, True, '')
            html += ' <img src="https://flat.badgen.net/github/stars/' + repo + '" style="max-width: 100%;"/>, '

        if len(repoList) > 0:
            html += self.genRepoBottomHtml(repoList)
            html += '</div>'
        return html

    def genRepoBottomHtml(self, repoList):
        if len(repoList) == 0:
            return ''
        html = '' 
        openAllJS = ''
        previewUrl = ""
        editReposJS = ''

        for repo in repoList:
            repo = repo.strip()
            url = "https://github.com/" + repo
            openAllJS += "window.open('" + url + "');"
            if len(repoList) > 5:

                if repo.find("/") > 0 and len(repo.split("/")) > 1 and repo.split("/")[1] != "":
                    previewUrl += "https://socialify.git.ci/" + repo + "/image?description=1&font=Rokkitt&forks=1&issues=1&language=1&name=1&owner=1&pattern=Formal Invitation&pulls=1&stargazers=1&theme=Dark";
                else:
                    previewUrl += "https://svg.bookmark.style/api?url=" + url + "&mode=Light"
            else:
                previewUrl += "https://svg.bookmark.style/api?url=" + url + "&mode=Light"
            if repo != repoList[len(repoList) - 1]:
                previewUrl += "*"

        if len(repoList) > 0:
            editReposJS = "editRepos('github:" + ', '.join(repoList) + "');"

            openAllJS += "hiddenPopup();";
            previewJS = "onHoverPreview('-github-1', 'easychen/<i><strong>rssp</strong></i>ush', '" + previewUrl + "', 'searchbox', true);"
            dataJS = "getWebsiteData('github', '" + '*'.join(repoList) + "');"
            datahtml = self.genJsIconLinkHtml(dataJS, Config.website_icons["data"], width=18, height=16)


            html += '<div align="right" style="margin-top: 5px; margin-bottom: 5px; margin-right: 10px;"><a href="javascript:void(0);" onclick="' + previewJS + '"><img src="https://cdn0.iconfinder.com/data/icons/beauty-and-spa-3/512/120-512.png" width="18" height="16" style="border-radius:10px 10px 10px 10px; opacity:0.7;"></a> ' + datahtml + ' <a href="javascript:void(0);" onclick="' + editReposJS + '"><img src="http://www.mystipendium.de/sites/all/themes/sti/images/coq/editxl.png" width="18" height="16" style="border-radius:10px 10px 10px 10px; opacity:0.7;"></a> <a href="javascript:void(0);" onclick="' + openAllJS + '"><img src="https://cdn3.iconfinder.com/data/icons/iconano-web-stuff/512/109-External-512.png" width="18" height="16" style="border-radius:10px 10px 10px 10px; opacity:0.7;"></a><a>  </a></div>'

            return html

    def genIconHtml(self, src, radius, width, height):
        if src != '':
            if radius:
                return ' <img src="' + src + '" width="' + str(width) + '" height="' + str(height) + '" style="border-radius:10px 10px 10px 10px; opacity:0.7;">'
            else:
                return ' <img src="' + src + '" width="' + str(width) + '" height="' + str(height) + '">'
        return ''      

    def partition(self, alist,first,last, sortType):
        pivotvalue = alist[first]

        leftmark = first+1
        rightmark = last

        done = False
        while not done:

            while leftmark <= rightmark and self.largeoreq(alist[leftmark], pivotvalue, sortType):
                leftmark = leftmark + 1

            while self.lessoreq(alist[rightmark], pivotvalue, sortType) and rightmark >= leftmark:
                rightmark = rightmark -1

            if rightmark < leftmark:
                done = True
            else:
                temp = alist[leftmark]
                alist[leftmark] = alist[rightmark]
                alist[rightmark] = temp

        temp = alist[first]
        alist[first] = alist[rightmark]
        alist[rightmark] = temp


        return rightmark

    
    def getColorStr(self, color, t):
        return '\033[' + self.cc_map[color] + 'm{0}\033[0m'.format(t)

    def print_inx(self, foreground, newline, *kw):    
        if foreground in self.cc_map:
            for t in kw:
                print '\033[' + self.cc_map[foreground] + 'm{0}\033[0m'.format(t),
        else:
            for t in kw: print t,
        
        if newline: print
       
    def print_colorful(self, foreground, newline, *kw):    
        try:
            if foreground == 'darkyellow':
                foreground = 'brown'
      
            if os.name == 'nt':
                self.print_nt(foreground, newline, *kw)
            else:
                self.print_inx(foreground, newline, *kw)
        except:
            for t in kw: print t,
            if newline: print

    def to_unicode(self, value):
        if not isinstance(value, basestring):
            value = str(value)
        if not isinstance(value, unicode):
            value = unicode(value, "UTF-8", "strict")
        return value

    def char_block_width(self, char):
        # Basic Latin, which is probably the most common case
        #if char in xrange(0x0021, 0x007e):
        #if char >= 0x0021 and char <= 0x007e:
        if 0x0021 <= char <= 0x007e:
            return 1
        # Chinese, Japanese, Korean (common)
        if 0x4e00 <= char <= 0x9fff:
            return 2
        # Hangul
        if 0xac00 <= char <= 0xd7af:
            return 2
        # Combining?
        if unicodedata.combining(uni_chr(char)):
            return 0
        # Hiragana and Katakana
        if 0x3040 <= char <= 0x309f or 0x30a0 <= char <= 0x30ff:
            return 2
        # Full-width Latin characters
        if 0xff01 <= char <= 0xff60:
            return 2
        # CJK punctuation
        if 0x3000 <= char <= 0x303e:
            return 2
        # Backspace and delete
        if char in (0x0008, 0x007f):
            return -1
        # Other control characters
        elif char in (0x0000, 0x001f):
            return 0
        # Take a guess
        return 1

    def str_block_width(self, val):
        return sum(itermap(self.char_block_width, itermap(ord, regex.sub("", val))))

    '''
    def clearHtmlTag(self, html):
        while(html.find('<') != -1 and html.find('>') != -1):
            start = html.find('<')
            end = html.find('>')
            if start > end:
                break
            html = html.replace(html[html.find('<') : html.find('>') + 1], '')
        return html
    '''

    def encode_feedparser_dict(self, d):
        """
        helper function to get rid of feedparser bs with a deep copy.
        I hate when libs wrap simple things in their own classes.
        """
        if isinstance(d, feedparser.FeedParserDict) or isinstance(d, dict):
          j = {}
          for k in d.keys():
            j[k] = self.encode_feedparser_dict(d[k])
          return j
        elif isinstance(d, list):
          l = []
          for k in d:
            l.append(self.encode_feedparser_dict(k))
          return l
        else:
          return d

    def get_arxiv_entries(self, query):
        query_url = 'http://export.arxiv.org/api/query?search_query=' + query
        response = None
        try:
            response = urllib.urlopen(query_url).read()
        except Exception as e:
            exception = True
        #response = self.requestWithProxy(base_url+query).text
        if response != None:
            parse = feedparser.parse(response)
            return parse.entries
        return None

    def get_last_arxiv_version(self, query):
        for e in self.get_arxiv_entries(query):
            j = self.encode_feedparser_dict(e)
            return j['id'][j['id'].rfind('v') :]
        return 'v1'


    def gen_plugin_content(self, selection, url, search_box=True):
        '''
        f = open("web_content/chrome/input", 'w');
        f.write(' | ' + selection.replace('"', ' ').replace("'", " ").replace('\n', '').strip() + '| | ')
        f.close()
        cmd = "./list.py -i web_content/chrome/input -b 4  -c 1  -p -e 'd:star' -n -d "
        '''

        #selection = '#>' + selection

        html = ''
        title = selection.replace('"', ' ').replace("'", " ").replace('\n', '').strip()
        if title != '':
            print str(datetime.datetime.now())

            cmd = "./list.py -i ' | " + title + " | " + url + " | ' -b 4  -c 1  -p -e 'd:star' -n -d "
            if search_box == False:
                cmd += ' -x '
            
            cmd += " > web_content/chrome/output.html"
            html = subprocess.check_output(cmd, shell=True)
            print str(datetime.datetime.now())
            #print data
            #data = "ddd"
            #f = open('web_content/chrome/output.html', 'w')
            #f.write(html)
            #f.close()

            print selection
        html = '<head>'
        script = ""
        html += '<script>' + script + '</script>'
        html += '<head><body>'
        if search_box:
            html = '<iframe  id="iFrameLink" width="600" height="300" frameborder="0"  src="http://' + Config.ip_adress + '/web_content/chrome/test.html"></iframe>'
        else:
            html = '<iframe  id="iFrameLink" width="600" height="210" frameborder="0"  src="http://' + Config.ip_adress + '/web_content/chrome/test.html"></iframe>'
        

        html += '<div id="info"></div></body>'

        return html
        #return '{"firstAccess" : "' + data + '"}'

    def suportFrame(self, url, sec):
        output = ''

        key = url.replace('https://', '').replace('http://', '').replace('www.', '')
        if key.find('/') != -1:
            key = key[ 0 : key.find('/')].strip()

        print 'suportFrame:'
        print 'url:' + url + ' key:' + key

        if key.startswith(Config.ip_adress):
            return True
        if self.suportFrameCache.has_key(key):
            return self.suportFrameCache[key]

        try:
            output = subprocess.check_output("curl --max-time " + str(sec) + " --head " + url, shell=True)
            print output
        except Exception as e:
            output = ''

        if output != '' and output.find('X-Frame-Options:') < 0:

            self.suportFrameCache[key] = True
            #print '\n'.join(self.suportFrameCache.keys())
            return True

        self.suportFrameCache[key] = False
        #print '\n'.join(self.suportFrameCache.keys())
        return False

    def websiteNotWorking(self, url, sec):
        output = ''
        try:
            cmd = "curl --max-time " + str(sec) + " --head " + url
            print cmd
            output = subprocess.check_output(cmd, shell=True)
            print output
        except Exception as e:
            output = ''
        if output.find('200 OK') == -1:
            return True
        return False

    def slack_message(self, message, channel='general'):
        token = '-'.join(Config.slack_token)
        sc = SlackClient(token)
        #print token
        sc.api_call('chat.postMessage', channel=channel, 
                    text=message, username='My Sweet Bot',
                    icon_emoji=':robot_face:')

    def toListHtml(self, titleList, urlList, htmlList, descHtmlList=None, splitNumber=0, moreHtml=True, showWebsiteIcon=True, rid='', aidList=[], refreshIDList=[], orginFilename=''):
        html = ''
        start = False 
        
        if splitNumber == 0:
          html = '<div class="ref"><ol>'
          start = True
        count = 0

        for i in range(0, len(titleList)):
          title = titleList[i]
          if title == '':
              continue
          count += 1
          if splitNumber > 0 and (count == 1 or count > splitNumber):
              if start:
                  html += '</ol></div>'
                  count = 1
                
              html += '<div style="float:left;"><ol>'
              start = True

          url = urlList[i]
          html += '<li><span>' + str(i + 1) + '.</span>'
          if url != '':
              html += '<p>'

              html += self.enhancedLink(url, title, module='history', library=orginFilename, aid=aidList[i], refreshID=refreshIDList[i])
              #'<a href="' + url + '">' + title + '</a>'
          else:
              html += '<p>' + self.utils.toSmartLink(title, Config.smart_link_br_len)

          if showWebsiteIcon:
              html += self.getIconHtml(urlList[i])

          if htmlList != None and len(htmlList) > 0:
              html += htmlList[i]
          if moreHtml:
              divID = 'div-' + aidList[i].replace('a-', '')
              linkID = aidList[i] + '-more'
              appendID = str(i + 1)
              script = self.genMoreEnginScript(linkID, divID, "loop-" + str(appendID), title, url, '-', hidenEnginSection=True)
              descHtml = ''
              if descHtmlList != None:
                descHtml = descHtmlList[i]
              html += self.genMoreEnginHtml(linkID, script.replace("'", '"'), '...', divID, '', False, descHtml=descHtml);


          html += '</p></li>'

        if start:
          html += '</ol></div>'
        return html

    def replaceEx(self, text, originStr, replaceStr, ignoreCase=True):
        if ignoreCase:

          reTool = re.compile(re.escape(originStr), re.IGNORECASE)
          #print 'before:' + text
          result = text
          try:
              result = reTool.sub(replaceStr, text)
          except Exception as e:
              return result
          
          #print 'after:' + result
          return result
        else:
            return text.replace(originStr, replaceStr)


    def clearHtmlTag(self, htmlstr):
        if htmlstr.find('<') == -1:
            return htmlstr
            
        re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I)
        re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)
        re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)
        re_br=re.compile('<br\s*?/?>')
        re_h=re.compile('</?\w+[^>]*>')
        re_comment=re.compile('<!--[^>]*-->')
        s=re_cdata.sub('',htmlstr)
        s=re_script.sub('',s) 
        s=re_style.sub('',s)
        s=re_br.sub('\n',s)
        s=re_h.sub('',s) 
        s=re_comment.sub('',s)
        blank_line=re.compile('\n+')
        s=blank_line.sub('\n',s)
        s=self.replaceCharEntity(s)
        return s.strip()

    def replaceCharEntity(self, htmlstr):
        CHAR_ENTITIES={'nbsp':' ','160':' ',
                    'lt':'<','60':'<',
                    'gt':'>','62':'>',
                    'amp':'&','38':'&',
                    'quot':'"','34':'"',}
        
        re_charEntity=re.compile(r'&#?(?P<name>\w+);')
        sz=re_charEntity.search(htmlstr)
        while sz:
            entity=sz.group()
            key=sz.group('name')
            try:
                htmlstr=re_charEntity.sub(CHAR_ENTITIES[key],htmlstr,1)
                sz=re_charEntity.search(htmlstr)
            except KeyError:
                htmlstr=re_charEntity.sub('',htmlstr,1)
                sz=re_charEntity.search(htmlstr)
        return htmlstr

    def repalce(self, s,re_exp,repl_string):
        return re_exp.sub(repl_string,s)


    def shortUrl2Url(self, url):
        resp = requests.get('https://unshorten.me/s/' + url.replace('http://','').replace('https://', ''))
        
        return resp.text

    def reflection_call(self, module, cls, method, cls_arg=None, method_arg=None):
        __import__(module)
        m = sys.modules[module]
        for str in dir(m):
            if str == cls:
                att=getattr(m,str)
                obj = None
                if cls_arg != None:
                    obj = att(cls_arg)
                else:
                    obj = att()
                for att2 in dir(att):
                    if att2 == method:
                        func = getattr(obj, att2)
                        if method_arg != None:
                            return apply(func, (), method_arg)    
                        else:
                            return apply(func)

    def check_contain_chinese(self, check_str):
        for ch in check_str.decode('utf-8'):
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False
