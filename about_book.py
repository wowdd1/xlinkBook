#!/usr/bin/env python

import getopt
import requests
import json
import sys
from bs4 import BeautifulSoup;
from utils import Utils

utils = Utils()
def searchAmazon(name):
    print 'searching ' + name

    r = requests.get('http://www.amazon.cn/s/?url=search-alias%3Dstripbooks&field-keywords=' + name)
    soup = BeautifulSoup(r.text)
    div = soup.find('div', class_='a-row a-spacing-small')
    itemid = div.a['href'][div.a['href'].find('dp/') + 3 :]

    print 'itemid: ' + itemid
    print "book:  " + div.a.text
    user_agent = {'User-agent': 'Mozilla/5.0'}
    r = requests.get('http://www.amazon.cn/gp/product-description/ajaxGetProuductDescription.html?asin=' + itemid + '&deviceType=web', headers = user_agent)


    soup = BeautifulSoup(r.text)
    
    for div in soup.find_all('div'):
        sp = BeautifulSoup(div.prettify())
        if div.h3 != None:
            for p in sp.find_all('p'):
                title = p.text.strip()
                if title == '':
                    print ''
                else:
                    title = title[0:len(title) - 4]
                    print title


def searchISBNDB(name):
    print 'searching ' + name
    r = requests.get('http://isbndb.com/search/all?query=' + name)
    soup = BeautifulSoup(r.text)
    div = soup.find('div', id='bookResults')
    print div.ul.li.a.text.strip()

    r = requests.get(div.ul.li.a['href'])
    soup = BeautifulSoup(r.text)
    div = soup.find('div', class_='bookSnippetBasic')
    sp = BeautifulSoup(div.prettify())
    publish = ''
    isbn10 = ''
    isbn13 = ''
    for d in sp.find_all('div'):
        text = utils.removeDoubleSpace(d.text)
        if text.find('Publisher') != -1:
            publish = text[text.find(':') + 1 :].strip()
            break
    
    isbn10 = publish[publish.find('ISBN10:') + 8 :  publish.find('ISBN10:') + 8 + 10]
    isbn13 = publish[publish.find('ISBN13:') + 8 :  publish.find('ISBN13:') + 8 + 13]
    publish = publish[0 : publish.find('ISBN')]
    print 'publish ' + publish
    print 'isbn10 ' + isbn10
    print 'isbn13 ' + isbn13 

def usage(argv0):
    return ''

def main(argv):
    keyword = ''
    try:
        opts, args = getopt.getopt(argv[1:], 'hn:', ["help", "name"])
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
        searchISBNDB(keyword)

if __name__ == '__main__':
    main(sys.argv)
