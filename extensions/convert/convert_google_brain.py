#!/usr/bin/env python
# -*- coding: utf-8-*-  

import sys
import getopt
import requests
import json
from bs4 import BeautifulSoup



def convert(source, crossrefQuery=''):

    url = 'https://ai.google/static/data/publications.json'

    r = requests.get(url)

    jobj = json.loads(r.text)

    for item in jobj['publications']:

        author = 'author:'

        desc = 'description:' + str(item['year'])


        for au in item['authors']:
            author += au['name'] + ', '
        author = author.strip()
        author = author[0 : len(author) - 2]

        line = ' | ' + item['title'] + ' | ' + item['search_url'] + ' | ' + author + ' ' + desc

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
    