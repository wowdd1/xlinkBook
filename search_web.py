#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.08

import os,sys
import getopt
import webbrowser

def usage(argv0):
    print ' usage:'
    print '-h,--help: print help message.'
    print '-s, --search: the keyword for search the web'
    print 'ex: ' + argv0 + ' -s "cs199"'

def openBrowser(url):
    if url == "":
        print "not found url"
    else:
        print "open " + url
        webbrowser.open(url)

def search(args):
    print 'searching , %s'%args
    urls = []
    url = ""
    i = 0
    file_path = os.path.abspath('.') + "/db/" + ".urls"
    if os.path.exists(file_path) == False:
        print "no url file found in db"
        return

    f = open(file_path)
    for line in f.readlines():
        if line.startswith(args):
            print "found " + line
            pos = line.find("http")
            urls.append(line[pos:line.find("|",pos)].strip().lower())

    if len(urls) > 1:
       for u in urls:
           if u.find("google.com") == -1 and u.find("baidu.com") == -1 \
              and u.find("bing.com") == -1 and u.find("yahoo.com") == -1:
               url = u
       if url == "":
           url = urls[0]
    elif len(urls) == 1:
        url = urls[0]
    
    openBrowser(url)
    f.close()

def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:], 'hs:', [])
    except getopt.GetoptError, err:
        print str(err)
        usage(argv[0])
        sys.exit(2)
    for o, a in opts:
        if o in ('-h', '--help'):
            usage(argv[0])
            sys.exit(1)
        elif o in ('-s', '--search'):
            search(a)
            sys.exit(0)

if __name__ == '__main__':
    main(sys.argv)
