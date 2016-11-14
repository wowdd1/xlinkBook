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
import sys
from bs4 import BeautifulSoup;
from record import Record
from record import PriorityRecord
from record import CourseRecord
from record import ReferenceRecord
from record import PaperRecord
from record import ContentRecord
from record import EnginRecord
import time, datetime
import feedparser
import urllib
import subprocess
from config import Config
reload(sys)
sys.setdefaultencoding('utf8')


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

    def setEnginMode(self, engin):
        if engin.find(':duckduckgo') != -1:
            self.ddg_mode = True 
            return True
        return False

    def getExtensions(self):
        extensions = []
        if os.path.exists('db/metadata/engin_extension'):
            f = open('db/metadata/engin_extension', 'rU')
            for line in f.readlines():
                if line.strip() != '':
                    extensions.append(line.strip())
        return extensions

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
        if len(self.search_engin_dict) == 0 and os.path.exists('db/metadata/engin_list'):
            f = open('db/metadata/engin_list','rU')
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
        if len(self.search_engin_type) == 0 and os.path.exists('db/metadata/engin_type'):
            f = open('db/metadata/engin_type','rU')
            all_lines = f.readlines()
            for line in all_lines:
                if line.startswith('#'):
                    continue
                if line.strip() != '':
                    self.search_engin_type.append(line.strip().strip())
        if len(self.engin_extension) == 0 and os.path.exists('db/metadata/engin_extension'):
            f = open('db/metadata/engin_extension','rU')
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
        for page in range(0, totalPage):
            if page + 1 == currentPage:
                html += '<a href="javascript:toPage(' + str(page + 1) + ", '" + libraryUrl.replace("'", '"') +"');" + '"><font size="5" color="#00BFFF"><b>' + str(page + 1) +'</b></font></a>&nbsp;'
            else:
                html += '<a href="javascript:toPage(' + str(page + 1) + ", '" + libraryUrl.replace("'", '"') + "');" +'">' + str(page + 1) +'</a>&nbsp;'
        html += '<div style="height: 11px; width: 100px"></div></div>'
        return html

    def gen_menu(self, source):
        db_root = '<a target="_blank" href="http://' + Config.ip_adress + '/?db=?" style="margin-right:6px">Home</a>'
        html = '<div style="margin-left:auto; text-align:center;margin-top:2px; margin-right:auto;">' + db_root
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
        #    db_root = '<a target="_blank" href="http://' + Config.ip_adress + '/?db=?" style="margin-right:6px">Home</a>'
        if user_name != None and user_name != '':
            lines = 0
            if os.path.exists('db/library/' + user_name + '-library'):
                f = open('db/library/' + user_name + '-library')
                lines = len(f.readlines())
                f.close()
            html = '<div style="float:right; margin-top:2px; margin-right:10px">' + db_root
            '''
	    for link_dict in Config.fav_links.items():
		html += '<a target="_blank" href="http://' + link_dict[1] + '" style="margin-right:6px">' + link_dict[0] + "</a>"
            '''
            if user_image != '':
                html += '<img src="' + user_image + '" width="20" height="20" style="border-radius: 50%;"/>'
            content = user_name

            if Config.display_all_library:
                html += self.gen_libary2(user_name, source)
            else:
                html += self.enhancedLink("http://' + Config.ip_adress + '/?db=library/&key=?", 'library', library=source, module='main') + '&nbsp;'

            html +=  self.enhancedLink('http://' + Config.ip_adress + '/?db=library/&key=' + user_name + '-library&column=3&width=' + Config.default_width, content + '<font size="2">(</font><font size="2" color="#999966">' + str(lines) + '</font><font size="2">)</font>', library=source, module='main') + '</div>'
        else:
            html = '<div style="float:right; margin-top:2px; margin-right:10px">' + db_root + self.enhancedLink("http://' + Config.ip_adress + '/login", 'Login', library=source, module='main') + '</div>'
        html += '<div style="height: 21px; width: 100px"></div>'

        return html

    def gen_libary2(self, user, source):
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
            count += 1
            f = open('db/library/' + item)
            lines = len(f.readlines())
            f.close()
            html += self.enhancedLink('http://' + Config.ip_adress + '/?db=library/&key=' + item + '&column=3&width=' + Config.default_width,  item.replace('-library', '') + '<font size="2">(</font><font size="2" color="#999966">' + str(lines) + '</font><font size="2">)</font>', library=source, module='main') + '&nbsp;'
 
            if count > 5 :
                count = 0
                #html += '<br/>' #need adjust config content_margin_top
        return html
        

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
        text = text.replace('\n','')
        while (text.find('  ') != -1):
            text = text.replace('  ', ' ')
        return text

    def validEngin(self, engin):
        records = self.search_engin_dict.keys()
        if self.ddg_mode:
            records = self.ddg_search_engin_dict.keys()
        for item in records:
            if item.lower().find(engin.lower()) != -1:
                return True
        print "invalided search engin: " + engin
        return False

    def caseLine(self, line):
        if line.isupper() == False:
            return line
        if self.check_contain_chinese(line):
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

    def getRecord(self, keyword, use_subject='', path='', return_all=False, log=False, use_cache=True):
        if self.cache_records.has_key(keyword) and use_cache:
            if log:
                print 'return cached record for ' + keyword
            if return_all:
                return self.cache_records[keyword]
            else:
                return self.cache_records[keyword][0]
        subject = default_subject;
        if use_subject != "":
            subject = use_subject
        if path == '':
            path = self.getPath(subject)
        if log:
            print 'searching %s'%keyword + " in " + subject
        record_list = []
        if log:
            print keyword
            print path
        files = ''
        if os.path.isfile(path):
            files = [path]
        else:
            files = self.find_file_by_pattern(keyword, path)
        for file_name in files:
            if os.path.isfile(file_name) == False:
                continue
            f = open(file_name)
            for line in f.readlines():
                record = Record(line)
                record.set_path(file_name)
                if record.get_id().lower().strip() == keyword.lower().strip():
                    if log:
                        print "found " + record.get_id() + ' ' + record.get_title() + ' ' + record.get_url() + ' in ' + self.shortFileName(file_name)
                    if return_all:
                        record_list.append(record)
                    else:
                        self.cache_records[keyword] = [record]
                        return record
        if return_all:
            if len(record_list) > 0:
                self.cache_records[keyword] = record_list
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
        if engin != '':
            url = self.getEnginUrl(engin)
            if url.find('%s') != -1:
                url = url.replace("%s", keyword.strip())
            else:
                url += keyword.strip()
        if engin == "crunchbase" and query.find(':') != -1:
            url = self.getEnginUrl(engin) + keyword.strip().replace(' ', '-')
            query = query[query.find(':') + 1 :].strip()
            if query == 'star':
                query = 'organization'
            url = url.replace('%s', query)

        return url
    
    def getEnginHtmlLink(self, engin, keyword, color=''):
        if color != '':
            return ' <a href="' + self.getEnginUrlEx(engin, keyword) + '" target="_blank"> <font size="2" color="' + color + '">' + engin + '</font></a>'
        else:
            return ' <a href="' + self.getEnginUrlEx(engin, keyword) + '" target="_blank"> <font size="2" color="#999966">' + engin + '</font></a>'

    def getRecommendType(self, fileName):
        if os.path.exists('db/metadata/engin_type'):
            f = open('db/metadata/engin_type', 'rU')
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

    def getTopEngin(self, tag):
        engins = self.getEnginList('d:' + tag.strip())
        if len(engins) > 0:
            return engins[0]
        else:
            return ''


    def getEnginList(self, engins, folder='', sort=False):
        if engins.startswith('description:') or engins.startswith('d:'):
            key = engins[engins.find(':') + 1 :].strip()
            engin_list = []
            tags = engins[engins.find(':') + 1 :].strip().split(' ')
            cachedEngins = []
            tags2 = []
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
            if Config.recommend_engin and tags[0] == 'star' and folder != '':
                self.search_engin_type_2_engin_title_dict[key] = self.recommendEngins(folder)
            else:
                self.search_engin_type_2_engin_title_dict[key] = self.realGetEnginList(tags, self.search_engin_dict.values())

            if len(cachedEngins) > 0:
                self.search_engin_type_2_engin_title_dict[key] = cachedEngins + self.search_engin_type_2_engin_title_dict[key]
                if sort:
                    self.search_engin_type_2_engin_title_dict[key] = self.sortEnginList(self.search_engin_type_2_engin_title_dict[key])
            return self.search_engin_type_2_engin_title_dict[key] 
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
        else:
            return engin_list

    def sortEnginList(self, engin_list):
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

    def getEnginListLinks(self, engins, topic, id='', query = '', color="#999966", fontSize=11, i=0, j=0, useQuote=False, module='', library='', pluginsMode=False):
        if self.ddg_mode:
            return self.getDDGEnginListLinks(engins, topic, id, query, color, fontSize)
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
                keyword = id.strip()
            else:
                keyword = topic.strip()
            if Config.hiden_content_after_search and pluginsMode == False:
                script = "var pid = this.parentNode.parentNode.id; hidenMoreContent(pid, 1);"
                style = "color:'" + color + '; font-size: ' + str(fontSize) + "'pt;"
                result[engin] = self.enhancedLink(self.getEnginUrlEx(engin, keyword, query), self.formatEnginTitle(engin_display), style=style, script=script, useQuote=useQuote, module=module, library=library, searchText=keyword, rid='#rid')
            else:
                style = "color:'" + color + '; font-size:' + str(fontSize) + "'pt;"
                result[engin] = self.enhancedLink(self.getEnginUrlEx(engin, keyword, query), self.formatEnginTitle(engin_display), style=style, useQuote=useQuote, module=module, library=library, searchText=keyword, rid='#rid')
            result[engin] += '&nbsp;'
        return result

    def formatEnginTitle(self, engin):
        if engin == 'search.mit':
            engin = 'mit'

        record = self.search_engin_dict[engin]
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

    def getDescDivs(self, divid, enginType, keyword, links_per_row, scrip, color, color2, fontSize):
        result = '<div id="' + divid + '" style="display: none;">'
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
        result += '<div id="' + divid + '-data" style="border-radius: 10px 10px 10px 10px;"></div>'
        
        return result


    def output2Disk(self, records, module, fileName, outputFormat=''):
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
            if outputFormat == 'markdown':
                if record.line.find(' parentid:') != -1 and record.get_parentid().strip() != '':
                    data += '    '
                data += '- [ ] [' + record.get_title().strip() + '](' + record.get_url().strip() + ')\n'
            else:
                data += record.get_id().strip() + '-' + str(count) + ' | ' + record.get_title().strip() + ' | ' + record.get_url().strip() + ' | ' + '\n'
        outputDir = Config.output_data_to_new_tab_path + module + '/'
        if outputFormat != '':
            outputDir += outputFormat + '/'
        if os.path.exists(outputDir) == False:
            os.makedirs(outputDir)

        f = open(outputDir + fileName, 'w')
        f.write(data)
        f.close()

        url = ''
        if outputFormat.strip() != '':
            url += 'edit ' + os.getcwd() + '/' + outputDir + fileName
            return url

        url += 'http://' + Config.ip_adress + '/?db=' + Config.output_data_to_new_tab_path.replace('db/', '')
        url += module
        if outputFormat.strip() != '':
            url += '/' + outputFormat + '/'
        
        url += '&key=' + fileName
        return url

    def bestMatchEngin(self, text, resourceType=''):
        #TODO get best engin by resourceType
        #print resourceType
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
            if isinstance(Config.smart_engin_for_tag[resourceType.strip()], str):
                engin = Config.smart_engin_for_tag[resourceType.strip()]
                result[engin.strip()] = self.toQueryUrl(self.getEnginUrl(engin), text)
            else:
                for u in Config.smart_engin_for_tag[resourceType.strip()]:
                    result[u.strip()] = self.toQueryUrl(self.getEnginUrl(u), text)

        if module != '' and Config.smart_engin_for_extension.has_key(module.strip()):
            result = {}
            if isinstance(Config.smart_engin_for_extension[module.strip()], str):
                engin = Config.smart_engin_for_extension[module.strip()]
                result[engin.strip()] = self.toQueryUrl(self.getEnginUrl(engin), text)
            else:
                for u in Config.smart_engin_for_extension[module.strip()]:
                    result[u.strip()] = self.toQueryUrl(self.getEnginUrl(u), text)  
        return result

    dialog_engin_cache = None
    def clientQueryEnginUrl2(self, text, resourceType=''):
        result = {}
        engins = []
        if resourceType != '' and Config.smart_engin_for_tag.has_key(resourceType):
            engins = Config.smart_engin_for_tag[resourceType]
        elif len(Config.smart_engin_for_dialog) > 0:
            engins = Config.smart_engin_for_dialog
        elif self.dialog_engin_cache != None:
            engins = self.dialog_engin_cache
        else:
            if Config.recommend_engin_type_for_dialog != '':
                engins = self.getEnginList('d:' + Config.recommend_engin_type_for_dialog, sort=True)
            else:
                engins = self.getEnginList('d:star', sort=True)
            self.dialog_engin_cache = engins.append('glucky');

        for engin in engins:
            result[engin] = self.toQueryUrl(self.getEnginUrl(engin), text)

        return result

    def accountMode(self, tag_list_account, tag_list_account_mode, engin, resourceType):
        if Config.smart_engin_lucky_mode_for_account:
            accountTags = ' '.join(tag_list_account)
            accountModeTags = ' '.join(tag_list_account_mode)
            return accountTags.find(engin + ':') != -1 and accountModeTags.find(resourceType + ':') != -1
        return False

    def toQueryUrl(self, url, text):
        query_text = text.replace('"', ' ').replace("'", ' ').replace(' ', "%20") 
        if url == '':
            return self.bestMatchEnginUrl(text)
        if url.find('%s') != -1:
            url = url.replace('%s', query_text)
        else:
            url += query_text
        return url

    #hook user usage data

    def enhancedLink(self, url, text, aid='', style='', script='', showText='', useQuote=False, module='', library='', img='', rid='', newTab=True, searchText='', resourceType='', urlFromServer=False, dialogMode=False, ignoreUrl=False):
        url = url.strip()
        user_log_js = ''
        query_url_js = ''
        chanage_color_js = ''
        rid = rid.strip()
        text = text.replace('"', '').replace("'", '')
        #text = self.clearHtmlTag(text).replace('\n', '')
        send_text = self.clearHtmlTag(text).replace('\n', '')
        if send_text.find('<') != -1:
            send_text = self.clearHtmlTag(send_text)
        if searchText == '':
            searchText = send_text
        newTabArgs = 'false'
        if newTab:
            newTabArgs = 'true'
        if useQuote:
            # because array.push('') contain ', list.py will replace "'" to ""
            # so use  #quote as ', in appendContent wiil replace #quote back to '
            user_log_js = "userlog(#quote" + send_text + "#quote,#quote" + url + "#quote,#quote" + module + "#quote,#quote" + library + "#quote, #quote" + rid + "#quote, #quote" + searchText+ "#quote);"

            query_url_js = "queryUrlFromServer(#quote" + send_text + "#quote,#quote" + url + "#quote,#quote" + module + "#quote,#quote" + library + "#quote, #quote" + rid + "#quote, #quote" + searchText+ "#quote, " + newTabArgs + ");"
            if Config.background_after_click != '' and text.find('path-') == -1:
                chanage_color_js = "chanageLinkColor(this, #quote"+ Config.background_after_click +"#quote, #quote" + Config.fontsize_after_click + "#quote, #quote" + resourceType + "#quote);"

        else:
            user_log_js = "userlog('" + send_text + "','" + url + "','" + module + "','" + library + "', '" + rid + "', '" + searchText + "', '" + resourceType + "');"
            query_url_js = "queryUrlFromServer('" + send_text + "','" + url + "','" + module + "','" + library + "', '" + rid + "', '" + searchText + "', '" + resourceType + "', " + newTabArgs + ");"
            if Config.background_after_click != '' and text.find('path-') == -1:
                chanage_color_js = "chanageLinkColor(this, '" + Config.background_after_click + "', '" + Config.fontsize_after_click + "');"

        
            
        if url.startswith('http') == False and url != '':
            #js = "$.post('/exec', {command : 'open', fileName : '" + url + "'}, function(data){});"
            cmd = 'open'
            if url.endswith('.md'):
                cmd = 'edit'

            js = "exec('" + cmd + "','" + searchText + "','" + url + "');"
            link = '<a target="_blank" href="javascript:void(0);" onclick="' + js + chanage_color_js + user_log_js + '">'
            if showText != '':
                link += showText + '</a>'
            else:
                link += text + '</a>'
            return link

        open_js = ''
        if ignoreUrl == False:
            if urlFromServer:
                user_log_js = ''
                open_js = query_url_js;
            else:
                urls = [url]    
                if module != '' or resourceType != '':
                    resultDict = self.clientQueryEnginUrl(url, searchText, resourceType, module)
                    if resultDict != None and len(resultDict) > 0:
                        urls = resultDict.values()
                for link in urls:
                    if link == '':
                        continue
                    if newTab:
                        if useQuote:
                            open_js += "window.open(#quote" + link + "#quote);"
                        else:
                            open_js += "window.open('" + link + "');"
                    else:
                        if useQuote:
                            open_js += "window.location.href = #quote" + link + "#quote;"
                        else:
                            open_js += "window.location.href = '" + link + "';"
                        break
        #open_js = ''
 
        result = ''
        
        if dialogMode:
            result = '<a href="#" class="bind_hover_card" data-toggle="popover" data-placement="top" data-trigger="hover" data-popover-content="' + rid + '#' + resourceType + '#' + aid + '" id="' + aid + '">'
        else:
            result = '<a target="_blank" href="javascript:void(0);"'

            if aid != '':
                result += ' id=' + aid 

            if script != '':
                script = script.replace('"', "'")
                if useQuote:
                    script = script.replace("'", '#quote')
                result += ' onclick="' + script + open_js + chanage_color_js + user_log_js + '"'
            else:
                result += ' onclick="' + open_js + chanage_color_js + user_log_js + '"'


            if style != '':
                result += ' style="' + style + '"'

            result += '>' 

        if img != '':
            result += img + '</a>'
        else:
            if showText != '':
                result += showText
            else:
                result += text
            result += '</a>'

        return result

    def toSmartLink(self, text, br_number=Config.smart_link_br_len, engin='', noFormat=False, showText='', module='', library='', rid='', resourceType=''):
        if text != '' and len(text.strip()) <= Config.smart_link_max_text_len:
            url = ''
            if engin != '':
                url = self.toQueryUrl(self.getEnginUrl(engin.strip()), text)
            else:
                url = self.bestMatchEnginUrl(text, resourceType=resourceType)
            if noFormat:
                return self.enhancedLink(url, text, showText=showText, module=module, library=library, rid=rid, resourceType=resourceType)
            else:
                return self.enhancedLink(url, self.formatTitle(text, br_number), showText=showText, module=module, library=library, rid=rid, resourceType=resourceType)
        if noFormat:
            return text
        else:
            return self.formatTitle(text, br_number)

    def formatTitle(self, title, br_number=Config.smart_link_br_len):
        if len(title) > br_number:
            at = title.find(' ', br_number)
            if at != -1:
                return title[0 : at] + '<br>' + self.formatTitle(title[at:], br_number)
            else:
                return title
        else:
            return title

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
             
    def getNavLinkList(self, engin):
        if self.ddg_mode:
            if len(self.ddg_search_engin_type) == 0 or len(self.ddg_search_engin_dict) == 0:
                self.loadDDGEngins()
            return self.ddg_search_engin_type
        else:
            if Config.extension_mode:
                return self.engin_extension
            else:
                return self.search_engin_type + self.engin_extension
        #return ['paper', 'book', 'project', 'course', 'talk', 'organization', 'people', 'social']

    def getEnginTypes(self):
        return self.search_engin_type

    def getEnginExtensions(self):
        return self.engin_extension

    def getLastEnginType(self):
        return self.search_engin_type[len(self.search_engin_type) - 1]

    def genMoreEnginHtml(self, aid, script, text, content_divID, color='', doubleQ=True, descHtml=''):
        #return ' <a id="' + aid +'" href="' + 'javascript:void(0);' + '" onClick="' + script + ';"> <font size="2" color="#999966">more</font></a>'
        div = '<div id="' + content_divID + '"></div>';
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
            html += '<div id="' + desc_divID + '" style="display: none;">' + descHtml + '</div>'
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
        script += "appendContent('" + content_divID + "','" + id + "','" + title.strip().replace(" ", '%20') + "','" + url+ "','" + info + "'," + hidenEngin + ");"
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


    def genDescHtml(self, desc, titleLen, keywordList):
        start = 0
        html = '<br>'
        desc = ' ' + desc
        while True:
            end = self.next_pos(desc, start, titleLen, keywordList)
            if end < len(desc):
                html += self.color_keyword(desc[start : end], keywordList) + '<br>'
                start = end
            else:
                html += self.color_keyword(desc[start : ], keywordList) + '<br>'
                break

        return html

    def next_pos(self, text, start, titleLen, keywordList, htmlStyle=True):
        min_end = len(text)
        c_len = titleLen
        if htmlStyle:
            c_len = titleLen + 10
        for k in keywordList:
            end = text.lower().find(' ' + k, start + 2)
            if end != -1 and end + 1 < min_end:
                end += 1
                min_end = end

        if min_end < len(text):
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

   
    def color_keyword(self, text, keywordList, color_index=0, html_style=True):
        result = text
        #if text.find('<a') != -1:
        #    return text
        for k in keywordList:
            k = ' ' + k
            if result.find(k + ' ') != -1:
                continue
            if result.find(k) == -1:
                continue
            k = k.strip()
            if (color_index - 1) % 2 == 0:
                if html_style == True:
                    #result = result.replace(k, '<font color="#33EE22">' + k + '</font>')
                    result = self.replacekeyword(result, k, '<font color="#33EE22">' + k + '</font>')
                else:
                    result = result.replace(k, utils.getColorStr('brown', k))
            else:
                if html_style == True:
                    #result = result.replace(k, '<font color="#66CCFF">' + k + '</font>')
                    result = self.replacekeyword(result, k, '<font color="#66CCFF">' + k + '</font>')
                    #return result.encode('utf-8')
                else:
                    result = result.replace(k, utils.getColorStr('darkcyan', k))

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
                with open(full_path, 'r+') as f:
                    try:
                        data = mmap.mmap(f.fileno(), 0)
                        if re_file.search(data):
                            final_file_list.append(full_path)
                    except Exception as e:
                        print str(e) + full_path
            else:
                final_file_list += self.find_file_by_pattern(pattern, full_path)
        return final_file_list

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

    def sortRecords(self, records):
        return self.quickSort(records)

    def largeoreq(self, item1, item2, sortType):
        if sortType == "published":
            return item1.get_published().strip() >= item2.get_published().strip()
        else:
            return item1.get_id().strip() >= item2.get_id().strip()

    def lessoreq(self, item1, item2, sortType):
        if sortType == "published":
            return item1.get_published().strip() <= item2.get_published().strip()
        else:
            return item1.get_id().strip() <= item2.get_id().strip()

    def quickSort(self, alist, sortType="published"):
        self.quickSortHelper(alist,0,len(alist)-1, sortType)

    def quickSortHelper(self, alist,first,last, sortType):
        if first<last:

            splitpoint = self.partition(alist,first,last, sortType)

            self.quickSortHelper(alist,first,splitpoint-1, sortType)
            self.quickSortHelper(alist,splitpoint+1,last, sortType)


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


    def gen_plugin_content(self, selection, search_box=True):
        '''
        f = open("web_content/chrome/input", 'w');
        f.write(' | ' + selection.replace('"', ' ').replace("'", " ").replace('\n', '').strip() + '| | ')
        f.close()
        cmd = "./list.py -i web_content/chrome/input -b 4  -c 1  -p -e 'd:star' -n -d "
        '''
        print str(datetime.datetime.now())
        cmd = "./list.py -i ' | " + selection.replace('"', ' ').replace("'", " ").replace('\n', '').strip() + " | | ' -b 4  -c 1  -p -e 'd:star' -n -d "
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
        if search_box:
            return '<iframe  id="iFrameLink" width="600" height="300" frameborder="0"  src="http://' + Config.ip_adress + '/web_content/chrome/test.html"></iframe>'
        else:
            return '<iframe  id="iFrameLink" width="600" height="210" frameborder="0"  src="http://' + Config.ip_adress + '/web_content/chrome/test.html"></iframe>'
        #return '{"firstAccess" : "' + data + '"}'

    def suportFrame(self, url, sec):
        output = ''
        try:
            output = subprocess.check_output("curl --max-time " + str(sec) + " --head " + url, shell=True)
            print output
        except Exception as e:
            output = ''
        if output != '' and output.find('X-Frame-Options:') < 0:
            return True
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


    def clearHtmlTag(self, htmlstr):
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
        return s

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
