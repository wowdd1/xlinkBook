#!/usr/bin/env python

import webbrowser
import getopt
import sys
import requests
from bs4 import BeautifulSoup


def usage(argv0):
    print ' usage:'
    print '-h,--help: print help message.'
    print '-n,--name: the faculty name'

def searchMAS(name):
    r = requests.get('http://academic.research.microsoft.com/io.ashx?type=9&s=0&query=' + name)
    soup = BeautifulSoup(r.text)
    a = soup.find('a')
    if a != None:
        r = requests.get(a['href'])
        soup = BeautifulSoup(r.text)
        homepage = soup.find('a', id='ctl00_MainContent_AuthorItem_imgHomePageLink')
        if homepage != None:
            print 'found ' + name + ' ' + a['href']
            webbrowser.open(homepage['href'])
    print 'not found'


def main(argv):
    keyword = ''
    try:
        opts, args = getopt.getopt(argv[1:], 'hn:u:', ["help", "name"])
        if len(args) == 1:
            keyword = args[0]
    except getopt.GetoptError, err:
        print str(err)
        usage(argv[0])
        sys.exit(2)
    for o, a in opts:
        if o in ('-h', '--help'):
            usage(argv[0])
        if o in ('-n', '--name'):
            keyword = a    

    if keyword != '':
        searchMAS(keyword)

if __name__ == '__main__':
    main(sys.argv)
