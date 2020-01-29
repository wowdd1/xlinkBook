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

    soup = BeautifulSoup(r.text)

    span = soup.find('span', class_='current')

    pageMax = int(span.text)

    serverDict = {}

    for page in range(pageMax, 59, -1):

        if source.endswith('/') == False:
            source += '/'
        url = source + 'comment-page-' + str(page)
        r = requests.get(url)
    
        soup = BeautifulSoup(r.text)

    
        for li in soup.find_all('li', class_='comment'):
            litext = li.text.strip().encode('utf-8')
    
            desc = ''
            lineList = []
            for text in litext.split('\n'):
                text = text.strip()
                if text.find('ss:/') != -1 or text.find('ssr:/') != -1:
                    start = text.find('ss')
                    if start > 0:
                        desc += text[0 : text.find('ss')]
                    text = text[start : ]
                    start = text.find(' ')
                    if start != -1:
                        if start > 0:
                            desc += text[start :]
                        text = text[0 : start]
                    if serverDict.has_key(text):
                        continue
                    else:
                        serverDict[text] = ''
                    url = 'https://doub.pw/qr/qr.php?text=' + text
                    pageHtml = '<a target="_blank" href="https://doub.io/sszhfx/comment-page-' + str(page) + '/#comments">' + str(page) + '</a>'
                    line = ' | ' + text[0 : 13] + ' | ' + url + ' | description:' + 'page of ' + pageHtml + ' ' + text
                    lineList.append(line) 
                else:
                    desc += text + '<br>'

            if len(lineList) > 0:
                for line in lineList:
                    print line + '<br>' + desc



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
    