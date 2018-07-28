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

    count = 0


    if source.find('new') != -1:

        for h3 in soup.find_all('h3'):
            url = ''
            title = h3.text.strip()
            if title.lower() == 'news':
                continue
            if title.find(' - ') != -1:
                title = title[title.find(' - ') + 3 :].strip()
            if h3.a != None:
                url = h3.a['href']
            print ' | ' + title + ' | ' + url + ' | '
    elif source.find('publication') != -1:
        for li in soup.find_all('li'):
            title = ''
            if li.i != None:
                title = li.i.text.strip()
            else:
                title = li.text.strip()
            website = 'website:'
            url = ''
            desc = ''

            sp = BeautifulSoup(li.prettify())

            links = sp.find_all('a')
            count = 0
            if len(links) > 0:
                for a in links:
                    count += 1
                    if count == 1:
                        url = a['href']
                    website += a.text.strip() + '(' + a['href'] + ')'
                    if count != len(links):
                        website += ', '
            else:
                website = ''
            desc = li.text.replace(title, '$').replace('\n', ' ').strip()
            textList = desc.split('$,')

            if len(textList) == 2:
                author = 'author:' + textList[0].strip().replace('.', '')

                desc = author + ' description:' + textList[1].strip().replace('.', '')

            line = ' | ' + title + ' | ' + url + ' | ' + website + ' ' + desc
            print line.encode('utf-8')


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
    