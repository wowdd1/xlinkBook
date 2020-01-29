#!/usr/bin/env python
# -*- coding: utf-8-*-  

import sys
import getopt
import requests
import json
from bs4 import BeautifulSoup



def convert(source, crossrefQuery=''):

    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    

    for page in range(0, 120, 12):
        url = source + '?start=' + str(page)
        #print url
        r = requests.get(url, headers=headers)
        #print r.text.encode('utf-8')
        found = False
        url = ''
        for line in r.text.split('\n'):
            if found:
                nline = ' | '+ line + ' | ' + url + ' | '
                print nline.encode('utf-8')
                found = False
                url = ''
            if line.find('question_link') != -1:
                found = True
                url = line[line.find('/') : ]
                url = 'http://chuansong.me' + url[0 : url.find('"')] 



def main(argv):
    source = ''
    crossrefQuery = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'u:q:', ["url", "crossrefQuery"])
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)


    for o, a in opts:

        if o in ('-u', '--url'):
            source = a
        if o in ('-q', '--crossrefQuery'):
            crossrefQuery = a

    if source == "":
        print "you must input the input file or dir"
        return

    convert(source, crossrefQuery=crossrefQuery)


if __name__ == '__main__':
    main(sys.argv)
    