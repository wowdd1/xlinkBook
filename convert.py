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
from config import Config

utils = Utils()
source = ''
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

pid = 21
sub_pid = 0
sub_sub_pid = 0
sub_sub_sub_pid = 0
sub_sub_sub_sub_pid = 0
app_mode = False
unit = 0
chapter = 0
sub_chapter = 0
code_list = []
last_pid = ''
rawdata = False

def customFormat(title, link, rID='', desc='', source=''):
    if delete_from_char != '':
        if len(delete_from_char) == 1:
            if title.find(delete_from_char) != -1:
                title = doDelete(title, delete_from_char, Config.delete_forward)
        else:
            for dc in delete_from_char.split(' '):
                if title.find(dc) != -1:
                    title = doDelete(title, dc, Config.delete_forward)
                    break
    if rID == '':
        rID = parentid + "-" + str(line_id)
    if link.startswith('http') == False and source != '':
        link = source[0 : source.find('/', source.find('//') + 2)] + link
    return [rID, customFormatTitle(title), link, desc]

def doDelete(title, char, forward):
    if forward:
        return title[0 : title.find(char)].strip()
    else:
        return title[title.find(char) + 1 :].strip()
    return title

def customFormatTitle(title):
    #return title[title.find(']') + 1 :].strip()
    if title.find('<') != -1:
        title = title.replace('<', '')
    if title.find('>') != -1:
        title = title.replace('>', '')
    return title

def customPrint(data):
    if keys.has_key(data[1]) == False:
        keys[data[1]] = ''
        print data[0] + " | "  + data[1].replace('|', '') + " | " + data[2] + " | " + data[3]



def customParserHtml(html, source):
    global line_id
    #step1 parse html

    return False
    
    soup = BeautifulSoup(html)
    '''
    for div in soup.find_all('div', class_="  row  result"):
        line = div.h2.text.strip() + ' ' + div.span.text.strip()
        if coditionCheck(line, div.a) == False:
            continue
        if line != '':
            line_id += 1

        if line_id >= start and line_id <= end:
            printLine(div.h2.text.strip() + ' ' + div.span.text.strip(), 'http://cn.indeed.com' + div.a['href'])
        else:
            return True
    return True
    '''
    
    soup = BeautifulSoup(html)
    author = ''
    title = ''
    count = 0
    for td in soup.find_all('td'):
        if td.i != None:
            title = td.text
        else:
            if title != '':
                count += 1
                author = td.text.strip().replace(',', '').replace(' and', ',').replace(' &', ',').replace('editors', '').strip().replace('(author)', '').strip()

                print 'neuroscience-books-' + str(count) + ' | ' + title.strip() + ' | | author:' +  author
                title = ''




    return True
    

    #step2 call printLine

    #step3 return True if sucess


def coditionCheck(line, tag):
    if filter(custom_filter, line):
        return False
    if contain(custom_contain, line, tag) == False:
        return False

    return True  

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

ids = {}
def customPrintFile(line):
    global parentid
    global pid, sub_pid, sub_sub_pid, sub_sub_sub_pid, sub_sub_sub_sub_pid, app_mode
    global unit, chapter, sub_chapter, last_pid
    #customid = str(line_id)


    customid = 'famous-neuroscientists'
    #customid = parentid + '-' + str(line_id)
    customid = parentid

    if line.strip().startswith('|'):
        print customid + '-' + str(line_id) + line + 'author:' + line[line.find('|') + 1 : line.find('|', line.find('|') + 1)].strip()
        return

    #id = parentid + '-' + line[0 : line.find(' ')]
    #if ids.has_key(id):
    #    return
    #ids[id] = id

    id = line[0 : line.find(' ')]

    '''
    #if parentid != '':
    #    customid = parentid
    #line = line.replace(':', '').strip()
    id = ''
    if len(line.strip()) == 1:
        id = line.strip()
    else:
        id = line[0 : line.find(' ')]
    
    if id.startswith('PART'):
        pid += 1
        sub_pid = 0
        print  customid + '-' + str(pid) + ' | ' + utils.caseLine(line[line.find('-') + 1:].strip()) + ' | | parentid:' + customid
    elif id.find(':') != -1:
        sub_pid += 1
        print  customid + '-' + str(pid) + '.' + str(sub_pid) + ' | ' + line[line.find(':') + 1:].strip() + ' | | parentid:' + customid + '-' + str(pid)

    parentid = get_parent_code(id)
    if parentid == id:
        parentid = customid
    if parentid == customid and id.isdigit():
        parentid = last_pid
    if parentid == None:
        print id
        print code_list

    if len(id) == 1 and id.isdigit() == False:
        #line = line[line.find(' ') :].strip()
        #new_line = ''
        #for item in line.split(' '):
        #    new_line += item[0 : 1] + item[1:].lower() + ' '
        #new_line = new_line.strip()
        print customid + '-' + id + ' | ' + line[line.find(' ') :].strip() + ' | | parentid:' + customid 
        last_pid = id
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
        pid += 1
        sub_pid = 0
        sub_sub_pid = 0

        print customid + '-' + str(pid) + ' | ' + line[line.find(' ') : ].strip() + ' | | parentid:' + customid
    elif id.find('.') == -1:
        sub_pid += 1
        sub_sub_pid = 0
        print customid + '-' + str(pid) + '.' + str(sub_pid)+ ' | ' + line[line.find(' ') : ].strip() + ' | | parentid:' + customid + '-' + str(pid)

    elif id.find('.') != -1:
        sub_sub_pid += 1
        if sub_pid != 0:
            print customid + '-' + str(pid) + '.' + str(sub_pid) + '.' + str(sub_sub_pid) + ' | ' + line[line.find(' ') : ].strip() + ' | | parentid:' + customid + '-' + str(pid) + '.' + str(sub_pid)
        else:
            print customid + '-' + str(pid)  + '.' + str(sub_sub_pid) + ' | ' + line[line.find(' ') : ].strip() + ' | | parentid:' + customid + '-' + str(pid)
    '''
    '''
    if line.startswith("Appendix"):
        app_mode = True
        print customid + '-Appendix' + ' | ' + line[line.find(' ') :].strip() + ' | | parentid:' + customid
        #print customid + '-Appendix' + ' | ' + line[line.find(' ', line.find(' ') + 1) :].strip() + ' | | parentid:' + customid
        sub_pid = 0
        return
    if app_mode:
        sub_pid += 1
        print customid + '-Appendix.' + str(sub_pid) + ' | ' + line[line.find(' '):].strip() + ' | | parentid:' + customid + '-Appendix'
        return
    '''
    
    if id== 'pid':
        pid += 1
        sub_pid = 0
        sub_sub_pid = 0
        sub_sub_sub_pid = 0
        sub_sub_sub_sub_pid = 0
        print customid + '-' + str(pid) + ' | ' + utils.caseLine(line[line.find(' ') : ].strip()) + ' | | parentid:' + customid
    elif id == 'sub_pid':
        sub_pid += 1
        sub_sub_pid = 0
        sub_sub_sub_pid = 0
        sub_sub_sub_sub_pid = 0
        print customid + '-' + str(pid) + '.'  + str(sub_pid) + ' | ' + line[line.find(' ') : ].strip() + ' | | parentid:' + customid + '-' + str(pid)
    elif id == "sub_sub_pid":
    #else:
        sub_sub_pid += 1
        sub_sub_sub_pid = 0
        sub_sub_sub_sub_pid = 0
        #if sub_pid == 0:
        #    sub_pid += 1
        #    print customid + '-' + str(pid)  + '.'  + str(sub_sub_pid) + ' | ' + line[line.find(' ') : ].strip() + ' | | parentid:' + customid + '-' + str(pid) 
        #else:
        print customid + '-' + str(pid) + '.'  + str(sub_pid) + '.'  + str(sub_sub_pid) + ' | ' + line[line.find(' ') : ].strip() + ' | | parentid:' + customid + '-' + str(pid) + '.'  + str(sub_pid)
    elif id == 'sub_sub_sub_pid':
        sub_sub_sub_pid += 1
        sub_sub_sub_sub_pid = 0
        print customid + '-' + str(pid) + '.'  + str(sub_pid) + '.'  + str(sub_sub_pid) + '.'  + str(sub_sub_sub_pid) + ' | ' + line[line.find(' ') : ].strip() + ' | | parentid:' + customid + '-' + str(pid) + '.'  + str(sub_pid) + '.' + str(sub_sub_pid)
    elif id == 'sub_sub_sub_sub_pid':
        sub_sub_sub_sub_pid += 1
        print customid + '-' + str(pid) + '.'  + str(sub_pid) + '.'  + str(sub_sub_pid) + '.'  + str(sub_sub_sub_pid) + '.'  + str(sub_sub_sub_sub_pid) + ' | ' + line[line.find(' ') : ].strip() + ' | | parentid:' + customid + '-' + str(pid) + '.'  + str(sub_pid) + '.' + str(sub_sub_pid) + '.'  + str(sub_sub_sub_pid)


    '''
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
        print custom + '-' + str(unit) + ' | ' + utils.caseLine(title[title.find(' ', title.find(' ') + 1) :].strip()) + ' | | parentid:' + custom
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
    '''
    #print customid  + '-' + str(line_id) + ' | ' + line.strip()  + ' | | '
    #print customid  +  ' | ' + line.strip()  + ' | | '
    #print line[0 : line.find(' ')].lower() + ' | ' + line[line.find(' ') :].strip()+ ' | | '


def printLine(line, link='', source='', id='', desc=''):
    #line_id = random.randrange(10, 100, 2)
    data = customFormat(line.strip(), link, id, desc, source)
    customPrint(data)

def filter(filters, line):
    if filters != '':
       filter_list = filters.split(' ')
       for ft in filter_list:
           if line.find(ft) != -1:
               return True
    return False


def contain(contains, line, tag):
    if contains == '':
        return True
    custom_contain_split = contains.split(' ')
    for c in custom_contain_split:
       if c != '' and contain2(line, c, tag): #line.find(c) != -1:
           return True
    return False


def contain2(line, keyword, tag):
    if keyword.startswith('http') and tag.attrs.has_key("href") or tag.attrs.has_key("src"):
        if tag.attrs.has_key("href"):
            return tag['href'].find(keyword[keyword.find('//') + 2 :]) != -1
        else:
            return tag['src'].find(keyword[keyword.find('//') + 2 :]) != -1
    else:
        return line.find(keyword) != -1

def defaultParserHtml(tags, html, source):
    global start, line_id
    for atag in custom_html_tag.strip().split(' '):
       soup = BeautifulSoup(html)
       data = None
       if atag.find('#') != -1:
           cls = atag[atag.find('#') + 1 :]
           atag = atag[0 : atag.find('#')]
           data = soup.find_all(atag, class_=cls)
       else:
           data = soup.find_all(atag)
       for tag in data:
           line = utils.removeDoubleSpace(tag.text.strip().replace('\n', ' '))
           if keyword_min_number > keyword_max_number:
              return
           split_list = line.split(' ')
           #print split_list  
           #print str(len(split_list)) + ' ' + str(keyword_min_number) + ' ' + str(keyword_max_number)
           if len(split_list) >= keyword_min_number and len(split_list) <= keyword_max_number:

               if line_id > end:
                   return  

               if coditionCheck(line, tag) == False:
                   continue

               if line != '':
                   line_id += 1
               if line != '' and line_id >= start and line_id <= end:
                   if tag.attrs.has_key("href"):
                       printLine(line, tag['href'], source)
                   elif tag.attrs.has_key("src"):
                       printLine(line, tag['src'], source)
                   elif tag.a != None and tag.a.attrs.has_key("href"):
                        printLine(line, tag.a['href'], source)
                   else:
                        printLine(line)

def convert(source):
    global start, line_id
    if source.startswith('http') or source.endswith('html') or source.endswith('htm'):
       html_content = ''
       if source.startswith('http'):
           user_agent = {'User-agent': 'Mozilla/5.0'}
           r = requests.get(source, headers = user_agent) 
           html_content = r.text
       elif source.endswith('html') or source.endswith('htm'):
           f = open(source)
           html_content = ''.join(f.readlines())

       if customParserHtml(html_content, source):
           return
       else:
           defaultParserHtml(custom_html_tag.strip().split(' '), html_content, source)

    else:
        f = open(source)
        lines = f.readlines()
        #lines = reversed(f.readlines())
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
    
