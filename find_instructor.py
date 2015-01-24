#!/usr/bin/env python

import webbrowser
import getopt
import sys
import requests
from bs4 import BeautifulSoup

keyword = ''

faculty_list = ['http://www.eecs.mit.edu/people/faculty-advisors',\
                'http://cs.stanford.edu/faculty',
                'http://www.eecs.berkeley.edu/Faculty/Lists/EE/list.shtml',\
                'http://www.eecs.berkeley.edu/Faculty/Lists/CS/list.shtml',\
                'http://www.seas.harvard.edu/electrical-engineering/people',\
                'http://www.seas.harvard.edu/computer-science/people']
def usage(argv0):
    print ' usage:'
    print '-h,--help: print help message.'

def getMitFacultyUrl(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    for a in soup.find_all('a'):
        if a.text == 'Personal Website':
            return a['href']
    return url

def search(keyword):
    for url in faculty_list:
        print 'searching ' + url
        r = requests.get(url)
        if r.text.lower().find(keyword.lower()) != -1:
            soup = BeautifulSoup(r.text)
            for a in soup.find_all('a'):
                if a.attrs.has_key("href") and a.text.lower().strip() == keyword.lower().strip():
                    link = ''
                    if url.find('berkeley') != -1:
                        link = 'http://www.eecs.berkeley.edu' + a['href']
                    elif url.find('eecs.mit') != -1:
                        link = getMitFacultyUrl(a['href'])
                    else:
                        link = a['href']
                    print 'found ' + a.text + ' ' + link
                    webbrowser.open(link)
                    return

            webbrowser.open(url)
            return

    print 'not found'




def main(argv):
    global keyword
    try:
        opts, args = getopt.getopt(argv[1:], 'h', ["help"])
        if len(args) == 1:
            keyword = args[0]
    except getopt.GetoptError, err:
        print str(err)
        usage(argv[0])
        sys.exit(2)
    for o, a in opts:
        if o in ('-h', '--help'):
            usage(argv[0])
    if keyword != '':
        search(keyword)

if __name__ == '__main__':
    main(sys.argv)
