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
import prettytable
from prettytable import PrettyTable
import requests
import sys
from bs4 import BeautifulSoup;
from record import Record
from record import PriorityRecord
from record import CourseRecord
from record import ReferenceRecord
from record import PaperRecord
from record import ContentRecord
import time
reload(sys)
sys.setdefaultencoding('utf8')


regex = re.compile("\033\[[0-9;]*m")
py3k = sys.version_info[0] >= 3
if py3k:
    unicode = str
    basestring = str
    itermap = map
    uni_chr = chr
    from html.parser import HTMLParser
else:
    itermap = itertools.imap
    uni_chr = unichr
    from HTMLParser import HTMLParser

class TableHandler(HTMLParser):

    def __init__(self, **kwargs):
        HTMLParser.__init__(self)
        self.kwargs = kwargs
        self.tables = []
        self.last_row = []
        self.rows = []
        self.max_row_width = 0
        self.max_cell_width = 100
        self.active = None
        self.last_content = ""
        self.is_last_row_header = False

    def setMaxCellWidth(self, width):
        self.max_cell_width = width

    def handle_starttag(self,tag, attrs):
        self.active = tag
        if tag == "th":
            self.is_last_row_header = True

    def handle_endtag(self,tag):
        if tag in ["th", "td"]:
            stripped_content = self.last_content.strip()[0 : self.max_cell_width]
            self.last_row.append(stripped_content)
        if tag == "tr":
            self.rows.append(
                (self.last_row, self.is_last_row_header))
            self.max_row_width = max(self.max_row_width, len(self.last_row))
            self.last_row = []
            self.is_last_row_header = False
        if tag == "table":
            table = self.generate_table(self.rows)
            self.tables.append(table)
            self.rows = []
        if tag == "span":
            return
        self.last_content = " "
        self.active = None
    def handle_data(self, data):
        self.last_content += data
    def generate_table(self, rows):
        """
        Generates from a list of rows a PrettyTable object.
        """
        table = PrettyTable(**self.kwargs)
        for row in self.rows:
            if len(row[0]) < self.max_row_width:
                appends = self.max_row_width - len(row[0])
                for i in range(1,appends):
                    row[0].append("-")

            if row[1] == True:
                self.make_fields_unique(row[0])
                table.field_names = row[0]
            else:
                table.add_row(row[0])
        return table

    def make_fields_unique(self, fields):
        """
        iterates over the row and make each field unique
        """
        for i in range(0, len(fields)):
            for j in range(i+1, len(fields)):
                if fields[i] == fields[j]:
                    fields[j] += "'"


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
    search_engin_type = []
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
        if os.path.exists('db/metadata/engin_list'):
            f = open('db/metadata/engin_list','rU')
            all_lines = f.readlines()
            for line in all_lines:
                record = PriorityRecord(line)
                if record.get_title() != '':
                    self.search_engin_url_dict[record.get_title().strip()] = record.get_url().strip()
                    self.search_engin_dict[record.get_title().strip()] = record
        if os.path.exists('db/metadata/engin_type'):
            f = open('db/metadata/engin_type','rU')
            all_lines = f.readlines()
            for line in all_lines:
                if line.startswith('#'):
                    continue
                if line.strip() != '':
                    self.search_engin_type.append(line.strip().strip())
        if os.path.exists('db/metadata/engin_extension'):
            f = open('db/metadata/engin_extension','rU')
            all_lines = f.readlines()
            for line in all_lines:
                if line.startswith('#'):
                    continue
                if line.strip() != '':
                    self.search_engin_type.append(line.strip().strip())

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

    def shortFileName(self, file_name):
        pos = 0
        while (file_name.find('/', pos) != -1):
            pos = file_name.find('/', pos) + 1
        return file_name[pos : ]

    def getRecord(self, keyword, use_subject='', path='', return_all=False, log=False):
        subject = default_subject;
        if use_subject != "":
            subject = use_subject
        if path == '':
            path = self.getPath(subject)
        if log:
            print 'searching %s'%keyword + " in " + subject
        record_list = []
        print keyword
        print path
        for file_name in self.find_file_by_pattern(keyword, path):
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
                        return record
        if return_all:
            if len(record_list) > 0:
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
        return self.search_engin_url_dict[engin]

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
            url = self.getEnginUrl(engin) + keyword.strip()
        if engin == "arxiv":
            url = url.replace("%s", keyword.strip())
        if engin == "doaj":
            url = url.replace('%s', keyword.strip())
        if engin == "ust.hk":
            url = url.replace('%s', keyword.strip())
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

    def getEnginList(self, engins):
        if engins.startswith('description:') or engins.startswith('d:'):
            engin_list = []
            tags = engins[engins.find(':') + 1 :].strip().split(' ')
            #print engins
            if self.ddg_mode:
                return self.getDDGEnginList(tags)
            return self.realGetEnginList(tags, self.search_engin_dict.values())
        else:
            return engins.split(' ')

    def realGetEnginList(self, tags, records):
        engin_list = []
        for record in records:
            desc = record.get_describe().strip()
            desc = desc[desc.find(':') + 1 :].strip()
            for tag in tags:
                if desc.find(tag) != -1:
                    engin = record.get_title().strip()
                    engin_list.append(record.get_title().strip())
        return engin_list

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

    def getEnginListLinks(self, engins, topic, id='', query = '', color="#999966", fontSize=11):
        if self.ddg_mode:
            return self.getDDGEnginListLinks(engins, topic, id, query, color, fontSize)
        if topic == '':
            return ''
        result = {}
        keyword = topic.strip()
        engin_display = ''
        for engin in engins:
            engin_display = engin
            if engin_display == 'search.mit':
                engin_display = 'mit'
            if engin_display == 'sanity':
                engin_display = 'arxiv-sanity'
            if self.searchByID(engin):
                keyword = id.strip()
            else:
                keyword = topic.strip()
            result[engin] = ' <a href="' + self.getEnginUrlEx(engin, keyword, query) + '" target="_blank" style="color:' + color + ' ; font-size: ' + str(fontSize) + 'pt;">' + engin_display + '</a>'

        return result

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
            div = '<div id="' + divid + '-' + str(count) + '">'
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
        return result

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
            return self.search_engin_type
        #return ['paper', 'book', 'project', 'course', 'talk', 'organization', 'people', 'social']

    def genMoreEnginHtml(self, aid, script, text, content_divID, color='', doubleQ=True):
        #return ' <a id="' + aid +'" href="' + 'javascript:void(0);' + '" onClick="' + script + ';"> <font size="2" color="#999966">more</font></a>'
        div = '<div id="' + content_divID + '"></div>';
        html = ''
        if color != '':
            if doubleQ:
                html = ' <font size="2"><a id="' + aid +'" href="' + 'javascript:void(0);' + '" onClick="' + script + '";><font color="' + color + '">' + text + '</font></a></font>'
            else:
                html = ' <font size="2"><a id="' + aid +'" href="' + 'javascript:void(0);' + '" onClick=' + script + ';><font color="' + color + '">' + text + '</font></a></font>'
        else:
            if doubleQ:
                html = ' <font size="2"><a id="' + aid +'" href="' + 'javascript:void(0);' + '" onClick="' + script + '";><font color="#999966">' + text + '</font></a></font>'
            else:
                html = ' <font size="2"><a id="' + aid +'" href="' + 'javascript:void(0);' + '" onClick=' + script + ';><font color="#999966">' + text + '</font></a></font>'
        return html + div

    def genMoreEnginScript(sefl, linkID, content_divID, id, title, info):
        script = ''
        script += "setText('" + linkID +"');"
        script += "showdiv('" + content_divID + "','" + linkID +"');"
        title = title.replace('"', '%20').replace("'",'%20').replace('&', '%20').replace(' ', '%20')
        info = info.replace('"', '%20').replace("'",'%20').replace('&', '%20').replace(' ', '%20')
        script += "appendContent('" + content_divID + "','" + id + "','" + title + "','" + info + "');"
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
                            return apply(func, method_arg)    
                        else:
                            return apply(func)

    def check_contain_chinese(self, check_str):
        for ch in check_str.decode('utf-8'):
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False
