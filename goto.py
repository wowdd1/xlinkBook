#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.08

import os,sys
import getopt
import webbrowser
from utils import Utils
from update.all_subject import print_all_subject
from config import Config

engin = ""
keyword = ""
use_subject = u""
search_keyword = False
search_video = False
filter = ''

def usage(argv0):
    print ' usage:'
    print '-h,--help: print help message.'
    print '-c, --course: the course for search on the web'
    print '-q, --query: the query keyword for search on the web'
    print '-e, --engin: what search for search include: google baidu bing yahoo'
    print '-u, --use: seach in what subject'
    print '-v, --video: search video'
    print "\nsubject include:"
    print_all_subject()
    print '\nex: ' + argv0 + ' -c "cs199" -u eecs'
    print '\nthe suported engin:\n' + get_all_engins()

def get_all_engins():
    utils = Utils()
    return '  '.join(utils.search_engin_dict.keys())

def openBrowser(url):
    if url == "":
        print "not found url"
    else:
        print "open " + url
        webbrowser.open(url)

def search(keyword, engin, search_keyword = False):
    url = ''
    if search_keyword == False:
        utils = Utils()
        record = utils.getRecord(keyword, use_subject)
        url = record.get_url().strip()
        keyword = record.get_title().strip()

    if search_video:
        engin_list = ['youtube', 'coursera', 'edx', 'googlevideo', 'chaoxing', 'youku', 'tudou', 'videolectures']
        for e in engin_list:
            openWeb(e, keyword, url)
    else:
        openWeb(engin, keyword, url)

def openWeb(engin, keyword, url):
    if engin.lower() == 'edx':
        keyword = keyword.replace(' ', '+')

    if engin != '':
        utils = Utils()
        url = utils.getEnginUrlEx(engin, keyword)

    if url != '':
        openBrowser(url)


def main(argv):
    global keyword, engin, use_subject, search_keyword, search_video, filter
    try:
        opts, args = getopt.getopt(argv[1:], 'hc:e:u:q:vf:', ["help","course","engin","use", 'query', 'video', 'filter'])
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
        elif o in ('-v', '--video'):
            search_video = True
        elif o in ('-f', '--filter'):
            filter = a
           
    if keyword != "":
        if keyword.find('db/') != -1:
            url = 'http://' + Config.ip_adress + '/?db=' + keyword[keyword.find('/') + 1 : keyword.rfind('/') + 1] + '&key=' + keyword[keyword.rfind('/') + 1 : ]
            if filter != '':
                url += '&filter="' + filter.replace(' ', '%20') + '"'
            openBrowser(url)
        else:
            search(keyword, engin, search_keyword) 
             

if __name__ == '__main__':
    main(sys.argv)
