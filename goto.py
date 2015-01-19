#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.08

import os,sys
import getopt
import webbrowser
from utils import Utils
from update.all_subject import print_all_subject

engin = ""
keyword = ""
use_subject = ""

def usage(argv0):
    print ' usage:'
    print '-h,--help: print help message.'
    print '-c, --course: the keyword for search the web'
    print '-e, --engin: what search for search include: google baidu bing yahoo'
    print '-u, --use: seach in what subject'
    print "subject include:"
    print_all_subject()
    print 'ex: ' + argv0 + ' -s "cs199" -u eecs'

def openBrowser(url):
    if url == "":
        print "not found url"
    else:
        print "open " + url
        webbrowser.open(url)

def search(keyword, engin):
    utils = Utils()
    url = utils.getUrl(keyword, use_subject, engin) 
    if url != '':
        openBrowser(url)

def main(argv):
    global keyword, engin, use_subject
    try:
        opts, args = getopt.getopt(argv[1:], 'hc:e:u:', ["help","course","engin","use"])
    except getopt.GetoptError, err:
        print str(err)
        usage(argv[0])
        sys.exit(2)
    for o, a in opts:
        if o in ('-h', '--help'):
            usage(argv[0])
        elif o in ('-c', '--course'):
            keyword = a
        elif o in ('-e', '--engin'):
            engin = a
        elif o in ('-u', '--use'):
            use_subject = str(a)
           
    if keyword != "":
        search(keyword, engin) 
             

if __name__ == '__main__':
    main(sys.argv)
