#!/usr/bin/env python
    
#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.08
    

import os
import sys
import re
import itertools
import unicodedata
from update.all_subject import default_subject
import prettytable
from prettytable import PrettyTable
import requests
import sys
from bs4 import BeautifulSoup;
from record import Record

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

    def __init__(self):
        self.loadEngins()

    def loadEngins(self):
        if os.path.exists('config/engin_list'):
            f = open('config/engin_list','rU')
            all_lines = f.readlines()
            for line in all_lines:
                record = Record(line)
                if record.get_title() != '':
                    self.search_engin_dict[record.get_title().strip()] = record

    def removeDoubleSpace(self, text):
        text = text.replace('\n','')
        while (text.find('  ') != -1):
            text = text.replace('  ', ' ')
        return text

    def validEngin(self, engin):
        for item in self.search_engin_dict.keys():
            if item.lower().find(engin.lower()) != -1:
                return True
        print "invalided search engin: " + engin
        return False

    def shortFileName(self, file_name):
        pos = 0
        while (file_name.find('/', pos) != -1):
            pos = file_name.find('/', pos) + 1
        return file_name[pos : ]

    def getRecord(self, keyword, use_subject='', path='', return_all=False):
        subject = default_subject;
        if use_subject != "":
            subject = use_subject
        if path == '':
            path = self.getPath(subject)

        print 'searching %s'%keyword + " in " + subject
        record_list = []
        for file_name in self.find_file_by_pattern(".*", path):
            f = open(file_name)
            for line in f.readlines():
                record = Record(line)
                record.set_path(file_name)
                if record.get_id().lower().strip() == keyword.lower().strip():
                    print "found " + record.get_id() + ' ' + record.get_title() + ' ' + record.get_url() + ' in ' + self.shortFileName(file_name)
                    if return_all:
                        record_list.append(record)
                    else:
                        return record
        if return_all:
            if len(record_list) > 0:
                return record_list
            else:
                print "no record found in " + subject +" db"
                return record_list.append(Record(''))
        else:
            print "no record found in " + subject +" db"
            return Record('')

    def getPath(self, subject):
        return os.getcwd() + "/db/" + subject + "/"

    def getEnginUrl(self, engin):
        for record in self.search_engin_dict.values():
            item = record.get_url().strip()
            if engin == 'google':
                return 'https://www.google.com.hk/?gws_rd=cr,ssl#safe=strict&q='
            if engin == 'googlevideo' and item.lower().find('google.com.hk/videohp') != -1:
                return item
            if engin == 'youku' and item.lower().find('soku.com/search') != -1:
                return item
            if engin == 'tudou' and item.lower().find('soku.com/t') != -1:
                return item
            if engin == 'mooc-list' and item.lower().find('google.com/cse') != -1:
                return item
            if engin == 'indeed' and item.lower().find('www.indeed') != -1:
                return item
            if engin.strip() == "arxiv-sanity" and item.lower().find('sanity') != -1:
                return item
            if engin == "arxiv" and item.lower().find('arxiv.org') != -1:
                return item
            if item.lower().find(engin.lower()) != -1:
                return item
        return ''

    def getEnginUrlEx(self, engin, keyword, query=''):
        url = ''
        if engin != '':
            url = self.getEnginUrl(engin) + keyword
        if engin == "arxiv":
            url = url.replace("$", keyword)
        if engin == "doaj":
            url = url.replace('$', keyword)
        if engin == "crunchbase" and query.find(':') != -1:
            url = self.getEnginUrl(engin) + keyword.strip().replace(' ', '-')
            query = query[query.find(':') + 1 :].strip()
            if query == 'star':
                query = 'organization'
            url = url.replace('$', query)

        return url
    
    def getEnginHtmlLink(self, engin, keyword):
        return ' <a href="' + self.getEnginUrlEx(engin, keyword) + '" target="_blank"> <font size="2" color="#999966">' + engin + '</font></a>'

    def getEnginList(self, engins):
        if engins.startswith('description:') or engins.startswith('d:'):
            engin_list = []
            tags = engins[engins.find(':') + 1 :].strip().split(' ')
            for record in self.search_engin_dict.values():
                desc = record.get_describe().strip()
                desc = desc[desc.find(':') + 1 :].strip()
                for tag in tags:
                    if desc.find(tag) != -1:
                        engin = record.get_title().strip()
                        if engin == 'google' or engin == 'scholar' or engin == 'youtube':
                            engin_list.insert(0, engin)
                        else:
                            engin_list.append(record.get_title().strip())
            return engin_list
        else:
            return engins.split(' ')

    def getAllEnginList(self):
        engin_list = []
        for record in self.search_engin_dict.values():
            engin = record.get_title().strip()
            if engin == 'google' or engin == 'scholar' or engin == 'youtube':
                engin_list.insert(0, engin)
            else:
                engin_list.append(record.get_title().strip())
        return engin_list

    def getEnginListLinks(self, engins, topic, id='', query = ''):
        if topic == '':
            return ''
        result = {}
        keyword = topic.strip()
        for engin in engins:
            if self.searchByID(engin):
                keyword = id.strip()
            else:
                keyword = topic.strip()
            result[engin] = ' <a href="' + self.getEnginUrlEx(engin, keyword, query) + '" target="_blank"> <font size="2" color="#999966">' + engin + '</font></a>'

        return result

    def genMoreLink(self, aid, script):
        #return ' <a id="' + aid +'" href="' + 'javascript:void(0);' + '" onClick="' + script + ';"> <font size="2" color="#999966">more</font></a>'
        return ' <font size="2" color="#999966"><a id="' + aid +'" href="' + 'javascript:void(0);' + '" onClick="' + script + ';"><font color="#999966">...</font></a></font>'

    def searchByID(self, engin):
        if engin.strip() == 'textbooksearch':
            return True
        return False

    def isEnginUrl(self, url):
        if url.find('soku.com') != -1 or url.find('google.com.hk/videohp') != -1:
            return True

        for key in self.search_engin_dict.keys():
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
        re_file = re.compile(pattern)
        if base == ".":
            base = os.getcwd()
    
        final_file_list = []
        #print base  
        cur_list = os.listdir(base)
        for item in cur_list:
            if item == ".svn" or item == ".git" or item == ".DS_Store":
                continue
    
            full_path = os.path.join(base, item)
            #print full_path
            if os.path.isfile(full_path):
                if re_file.search(full_path):
                    final_file_list.append(full_path)
            else:
                final_file_list += self.find_file_by_pattern(pattern, full_path)
        return final_file_list
    
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

    def clearHtmlTag(self, html):
        while(html.find('<') != -1 and html.find('>') != -1):
            start = html.find('<')
            end = html.find('>')
            if start > end:
                break
            html = html.replace(html[html.find('<') : html.find('>') + 1], '')
        return html

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


