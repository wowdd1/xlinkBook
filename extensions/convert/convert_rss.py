#!/usr/bin/env python
# -*- coding: utf-8-*-  

import sys
import getopt
import requests
import feedparser


def convert(source, crossrefQuery=''):

    d = feedparser.parse(source)

    for item in d['entries']:
        line = ' | ' + item['title'] + ' | ' + item['link'] + ' | '

        print line.encode('utf-8')

    return


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
    