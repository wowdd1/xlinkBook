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

def search(args):
    print 'searching , %s'%args
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
            if i == 0:
                url = line[line.find("http"):line.find("\n")]
            i = i + 1

    print "open " + url
    webbrowser.open(url)
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
