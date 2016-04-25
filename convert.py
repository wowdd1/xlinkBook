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
start = 0
end = 1000
line_id = 0

def printLine(line, link=''):
    #line_id = random.randrange(10, 100, 2)
    print prefix + "-" + str(line_id) + " |"  + line.strip() + " | " + link + " |"


def convert(source):
    global start, line_id
    if source.startswith('http'):
       r = requests.get(source) 
       for atag in custom_html_tag.strip().split(' '):
           soup = BeautifulSoup(r.text)
           for tag in soup.find_all(atag):
               line = utils.removeDoubleSpace(tag.text.strip().replace('\n', ' '))
               if keyword_min_number > keyword_max_number:
                  return
               split_list = line.split(' ')
               if len(split_list) >= keyword_min_number and len(split_list) <= keyword_max_number:
                   if custom_filter != '':
                       filters = custom_filter.split(' ')
                       for ft in filters:
                           if line.find(ft) != -1:
                               line = ''
                               break
                   if line_id > end:
                       return     
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
            printLine(line)

def main(argv):
    global source, keyword_min_numberend, keyword_max_number, custom_html_tag, custom_filter
    global start, end
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'i:u:n:m:t:f:s:e:', ["input", "url", "number", "max", "tag", "filter", "start", "end"])
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

    if source == "":
        print "you must input the input file or dir"
        return

    convert(source)

if __name__ == '__main__':
    main(sys.argv)
    
