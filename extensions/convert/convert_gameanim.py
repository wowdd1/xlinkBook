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

    page_numbers = soup.find('ul', class_='page-numbers')

    page_numbers = page_numbers.text.encode('utf-8').strip().split('\n')

    page_numbers = int(page_numbers[len(page_numbers) - 1])

    for page in range(1, page_numbers + 1):
        if page != 1:
            url = source + 'page/' + str(page)
            r = requests.get(url)
            soup = BeautifulSoup(r.text)
        div = soup.find('div', id='cb-content')

        soup = BeautifulSoup(div.prettify())

        for item in soup.find_all('h2', class_='cb-post-title'):

            line =  ' | ' + item.a.text.strip() + ' | ' + item.a['href'] + ' | '

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
    