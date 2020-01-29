#!/usr/bin/env python
# -*- coding: utf-8-*-  

import sys
import getopt
import requests
import json
from bs4 import BeautifulSoup


#'seed/new' : {'tag' : 'h3', 'start' : 2},\
#'seed/publication' : {'tag' : 'i', 'min_num' : 3},\

def convert(source, crossrefQuery=''):


    r = requests.get(source)

    title = ''
    url = ''
    for line in r.text.split('\n'):
        if line == '#EXTM3U' or line.strip() == '':
            continue
        if line.startswith('#'):
            title = line[line.find(',') + 1 :]

        if line.startswith('http'):

            url = line

        if title != '' and url != '':
            #if url.strip().endswith('.m3u8'):
            result = ' | ' + title + ' | ' + url + ' | '

            print result.encode('utf-8')
            title = ''
            url = ''




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
    