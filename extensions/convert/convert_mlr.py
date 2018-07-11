#!/usr/bin/env python
# -*- coding: utf-8-*-  

import sys
import getopt
import requests
import json
from bs4 import BeautifulSoup



def convert(source, crossrefQuery=''):

    r = requests.get(source)

    soup = BeautifulSoup(r.text)


    for div in soup.find_all('div', class_='paper'):
        sp = BeautifulSoup(div.prettify())

        titleP = sp.find('p', class_='title')

        authorSpan = sp.find('span', class_='authors')


        author = authorSpan.text.replace('\n', '').strip()

        while author.find('  ') != -1:
            author  = author.replace('  ', '')

        url = ''
        for a in sp.find_all('a'):
            if a.text.lower().find('pdf') != -1:
                url = a['href']
                break

        line = ' | ' + titleP.text.strip() + ' | ' + url + ' | author:' + author

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
    