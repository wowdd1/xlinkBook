#!/usr/bin/env python

# -*- coding: utf-8-*-  

import getopt
import time
import re
import os,sys
reload(sys)
sys.setdefaultencoding('utf-8')
import random
from utils import Utils
from bs4 import BeautifulSoup
import requests

utils = Utils()

source = ''
prefix = 'convert'

keyword_min_number = 3
keyword_max_number = 7
custom_html_tag = 'a'
custom_filter = ''
custom_contain = ''
start = 0
end = 10000
line_id = 0
delete_from_char = ''
parentid=''

keys = {}

def customFormat(id, title, link):
    '''
    stuff = title[0 : title.find(' ')].strip()
    if len(stuff) > 1:
        title = '    ' + title[title.find(' ') : ].strip()
    else:
        title = title[title.find(' ') : ].strip()
    return [stuff, title.replace("'", ' '), link]
    '''
    return [id, title, link]
def customPrint(data):
    '''
    if data[0].find('.') != -1:
        print parentid + '-' + data[0] + " |"  + data[1] + " | " + data[2] + " | " + "parentid:" + parentid + "-" + data[0][0 : data[0].find('.')]
    else:
        print parentid + '-' + data[0] + " |"  + data[1] + " | " + data[2] + " | " + "parentid:" + parentid
    '''
    if keys.has_key(data[1]) == False:
        keys[data[1]] = ''
        print parentid  + " | "  + data[1].replace('|', '') + " | " + data[2] + " | " 
        #print str(line_id) + " | "  + data[1].replace('|', '') + " | " + data[2] + " | " 
    #print data[0] + " |"  + data[1] + " | " + data[2] + " |"

pid = 0
sub_pid = 0
sub_sub_pid = 0
app_mode = False


unit = 0
chapter = 0
sub_chapter = 0

code_list = []
def get_parent_code(code):
    global code_list
    if len(code_list) == 0:
        code_list.append(code)
        return code
    else:
        if len(code) != code_list[len(code_list) - 1]:
            code_list.append(code)
        for i in range(len(code_list) - 1, -1, -1):
            if code.startswith(code_list[i]) and code != code_list[i]:
                return code_list[i]
        code_list.append(code)
        return code

def caseLine(line):
    new_line = ''
    for item in line.split(' '):
        new_line += item[0 : 1] + item[1:].lower() + ' '
    return new_line

def customPrintFile(line):
    global parentid
    global pid, sub_pid, sub_sub_pid, app_mode
    global unit, chapter, sub_chapter
    #customid = str(line_id)


    customid = 'MI211'
    #if parentid != '':
    #    customid = parentid
    #line = line.replace(':', '').strip()
    id = line[0 : line.find(' ')]
    
    '''
    if id.startswith('PART'):
        pid += 1
        sub_pid = 0
        print  customid + '-' + str(pid) + ' | ' + caseLine(line[line.find('-') + 1:].strip()) + ' | | parentid:' + customid
    elif id.find(':') != -1:
        sub_pid += 1
        print  customid + '-' + str(pid) + '.' + str(sub_pid) + ' | ' + line[line.find(':') + 1:].strip() + ' | | parentid:' + customid + '-' + str(pid)

    parentid = get_parent_code(id)
    if parentid == None:
        print id
        print code_list

    if len(id) == 1:
        line = line[line.find(' ') :].strip()
        new_line = ''
        for item in line.split(' '):
            new_line += item[0 : 1] + item[1:].lower() + ' '
        new_line = new_line.strip()
        print customid + '-' + id + ' | ' + new_line + ' | | parentid:' + customid 
    else:
        print customid + '-' + id + ' | ' + line[line.find(' ') :].strip() + ' | | parentid:' + customid  + '-' + parentid

    '''
    '''
    if line.strip().startswith('I ') or line.startswith('II')\
           or line.startswith('III')\
           or line.startswith('IV')\
           or line.startswith('V')\
           or line.startswith('VI')\
           or line.startswith('VII')\
           or line.startswith('VIII')\
           or line.startswith('IX')\
           or line.startswith('X ')\
	   or line.startswith('XI'):
    '''
    '''
    if line == "Appendices":
        app_mode = True
        pid = 0
        return
    if app_mode:
        if line.find(':') == 1:
            pid += 1
            sub_pid = 0
            print customid + '-Appendices' + str(pid) + ' | ' + line[line.find(' ') :] + ' | | parentid:' + customid
        else:
            sub_pid += 1
            print customid + '-Appendices' + str(pid) + '.' + str(sub_pid) + ' | ' + line + ' | | parentid:' + customid + '-Appendices' + str(pid)
        return

    if line.startswith('Part'):
        pid += 1
        sub_pid = 0
        print customid + '-' + str(pid) + ' | ' + line[line.find(' ', line.find(' ') + 1) : ].strip() + ' | | parentid:' + customid
    elif id.replace(':', '').isdigit() and len(id) < 5:
        sub_pid += 1
        print customid + '-' + str(pid) + '.'  + str(sub_pid) + ' | ' + line[line.find(' ') : ].strip() + ' | | parentid:' + customid + '-' + str(pid)
            

    if line.strip().startswith('PART'):
	pid += 1
	sub_pid = 0
        sub_sub_pid = 0
	line = line[line.find(' ', line.find(' ') + 1) : ].strip()
	print customid + '-' + str(pid) + ' | ' + line.strip() + ' | | parentid:' + customid
    elif line.strip().startswith('CHAPTER'):
	sub_pid += 1
        sub_sub_pid = 0
        #line = line[line.find(' ', line.find(' ') + 1) : ].strip()
        if pid == 0:
            print customid + '-' + str(pid) + ' | ' + line[line.find(' ', line.find(' ') + 1) : ].strip() + ' | | parentid:' + customid
        else:
            print customid + '-' + str(pid) + '.' + str(sub_pid)  + ' | ' + line[line.find(' ', line.find(' ') + 1) : ].strip()  + ' | | parentid:' + customid + '-' + str(pid)
    elif id.find('.') != -1:
        sub_sub_pid += 1
        if pid == 0:
            print customid + '-' + str(pid) + '.' + str(sub_sub_pid)  + ' | ' + line[line.find(' ') : ].strip() + ' | | parentid:' + customid + '-' + str(pid)
        else:
            print customid + '-' + str(pid) + '.' + str(sub_pid) + '.' + str(sub_sub_pid)  + ' | ' + line[line.find(' ') : ].strip() + ' | | parentid:' + customid + '-' + str(pid) + '.' + str(sub_pid)

            
    #elif line[0 : line.find(' ')].strip().find('.') != -1:

    elif line[0 : line.find(' ')].strip().isdigit() and line[0 : line.find(' ')].find('.') == -1:
        sub_sub_pid += 1
        if pid == 0:
	    print  customid + '-' + str(pid) + '.' + str(sub_sub_pid) + ' | ' + line[line.find(' ') : ].strip() + ' | | parentid:' + customid + '-'+ str(pid)
        else:
	    print  customid + '-' + str(pid)+ '.' + str(sub_pid) + '.' + str(sub_sub_pid) + ' | ' + line[line.find(' ') : ].strip() + ' | | parentid:' + customid + '-'+ str(pid) + '.' + str(sub_pid)
    #else:
    #    sub_sub_pid += 1
    #    print  customid + '-' + str(pid)+ '.' + str(sub_pid) + '.' + str(sub_sub_pid) + ' | ' + line.strip() + ' | | parentid:' + customid + '-'+ str(pid) + '.' + str(sub_pid)


    if line.find('.') != -1:
        number = line[0 : line.find(' ')].replace('.', '')
        title = line[line.find(' ') + 1 : ].strip()
        print customid + '-' + number + ' | ' + title + ' | | parentid:' + customid
    else:
        title = line[line.find(' ') + 1 : ].strip()
        #print customid + '-' + line[0 : line.find(' ')].strip() + ' | ' + title + ' | | parentid:' + customid
        #print line[0 : line.find(' ')].strip() + ' | ' + title + ' | | '
	print 'pitt-neurobio-' + str(line_id) + ' | ' + line + ' | | '

    title = line.strip()
    custom = '7.81'
    id = line[0 : line.find(' ')]
    if id.find('.') == -1 and id.find(':') == -1:
        return
    if id.find(':') != -1:
        id = id.replace(':', '')
        print custom + '-' + str(id) + ' | ' + title[title.find(' ') :].strip() + ' | | parentid:' + custom
    else:
        print custom + '-' + str(id) + ' | ' + title[title.find(' ') :].strip() + ' | | parentid:' + custom + '-' + id[0 : id.rfind('.')]

    custom = 'BIO118'
    title = line.strip()
    if id == 'Appendix':
        print custom + '-' + title[0 : title.find(':')].replace(' ', '') + ' | ' + title[title.find(':') + 1 :].strip() + ' | | parentid:' + custom
        return
    #id =id[0 : len(id) - 1]

    if title.startswith('PART') or id == '1':
    #if id.find('.') == -1: 
        unit += 1
        chapter = 0
        sub_chapter = 0
        sub_sub_pid = 0
        print custom + '-' + str(unit) + ' | ' + caseLine(title[title.find(' ', title.find(' ') + 1) :].strip()) + ' | | parentid:' + custom
    #elif title.startswith(' ') == False:
    #elif id.find('.') != -1 and id.find('.', id.find('.') + 1) == -1:
    elif id.isdigit() and id.find('.') == -1:
        chapter += 1
        sub_chapter = 0
        sub_sub_pid = 0
        print custom + '-' + str(unit) + '.' + str(chapter) + ' | ' + title[title.find(' ') :].strip() + ' | | parentid:' + custom  + '-' + str(unit)
    elif id.find('.') != -1:
        sub_chapter += 1
        sub_sub_pid = 0
        if unit == 1:
            print custom + '-' + str(unit) + '.' + str(sub_chapter) + ' | ' + title[title.find(' ') :].strip() + ' | | parentid:' + custom  + '-' + str(unit)
        else:
            print custom + '-' + str(unit) + '.' + str(chapter) + '.' + str(sub_chapter) + ' | ' + title[title.find(' ') :].strip() + ' | | parentid:' + custom  + '-' + str(unit) + '.' + str(chapter)
    else:
        sub_sub_pid += 1
        if unit == 1:
            print custom + '-' + str(unit) + '.' + str(sub_chapter) + '.' + str(sub_sub_pid) + ' | ' + title.strip() + ' | | parentid:' + custom  + '-' + str(unit) + '.' + str(sub_chapter)
        else:
            print custom + '-' + str(unit) + '.' + str(chapter) + '.' + str(sub_chapter) + '.' + str(sub_sub_pid) + ' | ' + title.strip() + ' | | parentid:' + custom  + '-' + str(unit) + '.' + str(chapter) + '.' + str(sub_chapter)

    custom = 'CS334A'
    id = line[0 : line.find(' ')]
    if id.find('.') != -1:
        print custom + '-' + id + ' | ' + line[line.find(' ') :].strip()+ ' | | parentid:' + custom + '-' + id[0 : id.rfind('.')]
    else:
        print custom + '-' + id + ' | ' + line[line.find(' ') :].strip()+ ' | | parentid:' + custom 
    #if title.find('(') != -1:
        #title = title[0 : title.find('(')].strip()
    #print customid + '-' + str(line_id) + ' | ' + title + ' | | '
    '''
    print line[0 : line.find(' ')].lower() + ' | ' + line[line.find(' ') :].strip()+ ' | | '

def format(line, link):
    if link != '' and line.startswith('http') == False:
        if source.find('com') != -1:
            link = source[0 : source.find('com') + 3] + link
        if source.find('uk') != -1:
            link = source[0 : source.find('uk') + 3] + link
    if delete_from_char != '' and line.find(delete_from_char) != -1:
        line = line[0 : line.find(delete_from_char)].strip()

    return customFormat(prefix + "-" + str(line_id), line, link)

def printLine(line, link=''):
    #line_id = random.randrange(10, 100, 2)
    data = format(line.strip(), link)
    customPrint(data)

def convert(source):
    global start, line_id
    if source.startswith('http') or source.endswith('html'):
       html_content = ''
       if source.startswith('http'):
           user_agent = {'User-agent': 'Mozilla/5.0'}
           r = requests.get(source, headers = user_agent) 
           html_content = r.text
       elif source.endswith('html'):
           f = open(source)
           html_content = ''.join(f.readlines())
       for atag in custom_html_tag.strip().split(' '):
           soup = BeautifulSoup(html_content)
           for tag in soup.find_all(atag):
               line = utils.removeDoubleSpace(tag.text.strip().replace('\n', ' '))
               if keyword_min_number > keyword_max_number:
                  return
               split_list = line.split(' ')
               #print split_list  
               #print str(len(split_list)) + ' ' + str(keyword_min_number) + ' ' + str(keyword_max_number)
               if len(split_list) >= keyword_min_number and len(split_list) <= keyword_max_number:
                   if custom_filter != '':
                       filters = custom_filter.split(' ')
                       for ft in filters:
                           if line.find(ft) != -1:
                               line = ''
                               break
                   if line_id > end:
                       return     
                   if custom_contain != '':
                       custom_contain_split = custom_contain.split(' ')
                       skip = False
                       for c in custom_contain_split:
                           if c != '' and line.find(c) != -1:
                               skip = False
                               break
                           else:
                               skip = True
                       if skip: 
                           continue
                   if line != '':
                       line_id += 1
                   if line != '' and line_id >= start and line_id <= end:
                       if tag.attrs.has_key("href"):
                           printLine(line, tag['href'])
                       elif tag.a != None and tag.a.attrs.has_key("href"):
                            printLine(line, tag.a['href'])
                       else:
                            printLine(line)
    else:
        f = open(source)
        lines = f.readlines()
        data = ''.join(lines)
        data = utils.clearHtmlTag(data)
    
        for line in data.split('\n'):
            if line.strip() != '':
                line_id += 1
            if line.strip() != '' and line_id >= start and line_id <= end:
                customPrintFile(line)

def main(argv):
    global source, keyword_min_number, keyword_max_number, custom_html_tag, custom_filter
    global start, end, custom_contain, delete_from_char, parentid
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'i:u:n:m:t:f:s:e:c:d:p:', ["input", "url", "number", "max", "tag", "filter", "start", "end", "contain", "delete", "parent"])
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)


    for o, a in opts:
        if o in ('-i', '--input'):
            source = a
        if o in ('-u', '--url'):
            source = a
        if o in ('-n', '--number'):
            keyword_min_number = int(a)
        if o in ('-m', '--max'):
            keyword_max_number = int(a)
        if o in ('-t', '--tag'):
            custom_html_tag = a
        if o in ('-f', '--filter'):
            custom_filter = a
        if o in ('-s', '--start'):
            start = int(a)
        if o in ('-e', '--end'):
            end = int(a)
        if o in ('-c', '--contain'):
            custom_contain = a
        if o in ('-d', '--delete'):
            delete_from_char = a
        if o in ('-p', "--parent"):
            parentid = a.strip()

    if source == "":
        print "you must input the input file or dir"
        return

    convert(source)

if __name__ == '__main__':
    main(sys.argv)
    
