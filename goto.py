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
use_subject = u""
search_keyword = False

def usage(argv0):
    print ' usage:'
    print '-h,--help: print help message.'
    print '-c, --course: the course for search on the web'
    print '-q, --query: the query keyword for search on the web'
    print '-e, --engin: what search for search include: google baidu bing yahoo'
    print '-u, --use: seach in what subject'
    print '-y, --youtube: search video in youtube'
    print "\nsubject include:"
    print_all_subject()
    print '\nex: ' + argv0 + ' -s "cs199" -u eecs'
    print '\nthe suported engin:\n' + get_all_engins()

def get_all_engins():
    utils = Utils()
    return ' , '.join(utils.search_engin_dict.keys())

def openBrowser(url):
    if url == "":
        print "not found url"
    else:
        print "open " + url
        webbrowser.open(url)

def search(keyword, engin, search_keyword = False):
    url = ''
    search_keywork = keyword
    utils = Utils()
    if search_keyword == False:
        record = utils.getRecord(keyword, use_subject)
        url = record.get_url().strip()
        search_keywork = record.get_title().strip()

    if engin != '':
        url = utils.getEnginUrl(engin) + search_keywork

    if url != '':
        openBrowser(url)

def main(argv):
    global keyword, engin, use_subject, search_keyword
    try:
        opts, args = getopt.getopt(argv[1:], 'hc:e:u:q:', ["help","course","engin","use", 'query'])
        if len(args) == 1:
            keyword = args[0]
    except getopt.GetoptError, err:
        print str(err)
        usage(argv[0])
        sys.exit(2)
    for o, a in opts:
        if o in ('-h', '--help'):
            usage(argv[0])
        elif o in ('-c', '--course'):
            keyword = a
        elif o in ('-q', '--query'):
            keyword = a
            search_keyword = True
        elif o in ('-e', '--engin'):
            engin = a
        elif o in ('-u', '--use'):
            use_subject = str(a)
           
    if keyword != "":
        search(keyword, engin, search_keyword) 
             

if __name__ == '__main__':
    main(sys.argv)
