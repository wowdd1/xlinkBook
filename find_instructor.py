#!/usr/bin/env python

import webbrowser
import getopt
import sys
import requests
from bs4 import BeautifulSoup
import json

keyword = ''

faculty_list = ['http://www.eecs.mit.edu/people/faculty-advisors',\
                'http://cs.stanford.edu/faculty',
                'http://www.eecs.berkeley.edu/Faculty/Lists/EE/list.shtml',\
                'http://www.eecs.berkeley.edu/Faculty/Lists/CS/list.shtml',\
                'http://www.seas.harvard.edu/electrical-engineering/people',\
                'http://www.seas.harvard.edu/computer-science/people',\
                'https://www.cs.princeton.edu/people/faculty',\
                'http://www.math.princeton.edu/directory/faculty']
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

def getCmuFacultyUrl(keyword):
    post_data = {'combine' : keyword,\
                 'view_name':"directory_search",\
                 'view_display_id':"block"}
    r = requests.post('http://www.cs.cmu.edu/views/ajax', post_data)
    jobj = r.json()
    soup = BeautifulSoup(jobj[1]['data'])
    for a in soup.find_all('a'):
        if a.attrs.has_key("href") and a['href'].find('www.cs.cmu.edu/directory') != -1:
            r = requests.get('http://' + a['href'][2 : ])
            soup = BeautifulSoup(r.text)
            for a in soup.find_all('a'):
                if a.text.startswith('http://'):
                    return a['href']
                    
    return ''
def getPrincetonFacultyUrl(base_url, href):
    r = requests.get(base_url + href)
    soup = BeautifulSoup(r.text)
    for a in soup.find_all('a'):
        if a.text.startswith(base_url):
            return a['href']
    return base_url + href

def match(text, keyword):
    if text.lower().strip() == keyword.lower().strip():
        print text + ' match ' + keyword
        return True
    for word in text.strip().split(' '):
        if word == keyword.strip():
            print 'found word ' + word + ' in ' + text 
            return True

    return False

def search(keyword):
    for url in faculty_list:
        print 'searching ' + url
        r = requests.get(url)
        if r.text.lower().find(keyword.lower()) != -1:
            soup = BeautifulSoup(r.text)
            for a in soup.find_all('a'):
                if a.attrs.has_key("href") and match(a.text, keyword):
                    link = ''
                    if url.find('berkeley') != -1:
                        link = 'http://www.eecs.berkeley.edu' + a['href']
                    elif url.find('eecs.mit') != -1:
                        link = getMitFacultyUrl(a['href'])
                    elif url.find('cs.princeton') != -1:
                        link = getPrincetonFacultyUrl('http://www.cs.princeton.edu', a['href'])
                    elif url.find('math.princeton') != -1:
                        link = getPrincetonFacultyUrl('http://www.math.princeton.edu', a['href'])
                    else:
                        link = a['href']
                    print 'found ' + a.text + ' ' + link
                    webbrowser.open(link)
                    return

    cmu_url = getCmuFacultyUrl(keyword)
    if cmu_url != '':
        webbrowser.open(cmu_url)
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
