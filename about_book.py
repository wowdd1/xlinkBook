#!/usr/bin/env python

import getopt
import requests
import json
import sys
from bs4 import BeautifulSoup;
from utils import Utils

utils = Utils()
def searchAmazonCN(namei, publish, isbn):
    print 'searching ' + name

    r = requests.get('http://www.amazon.cn/s/?url=search-alias%3Dstripbooks&field-keywords=' + name)
    soup = BeautifulSoup(r.text)
    div = soup.find('div', class_='a-row a-spacing-small')
    
    
    itemid = div.a['href'][div.a['href'].find('dp/') + 3 :]

    print 'itemid: ' + itemid
    print "book:  " + div.a.text
    user_agent = {'User-agent': 'Mozilla/5.0'}
    r = requests.get('http://www.amazon.cn/gp/product-description/ajaxGetProuductDescription.html?asin=' + itemid + '&deviceType=web', headers = user_agent)


    sp = BeautifulSoup(r.text)
    
    for div in sp.find_all('div'):
        sp2 = BeautifulSoup(div.prettify())
        if div.h3 != None:
            for p in sp2.find_all('p'):
                title = p.text.strip()
                print title
    searchISBNDB(name)
    print ''
    print 'other books:'
    for d in soup.find_all('div', class_='a-row a-spacing-small'):
        print d.a.text

def searchAmazon(name, publisher, isbn):
    print 'searching ' + name

    for book in getAmazonBookList(name):
        print book


    (publish, isbn10, isbn13) = searchISBNDB(name)
    if (publisher != ''):
        publish = publisher
    if isbn != '':
        isbn10 = isbn
        isbn13 = isbn

    searchPublish(publish, isbn10, isbn13) 

def getAmazonBookList(name):
    user_agent = {'User-agent': 'Mozilla/5.0'}
    r = requests.get('http://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Dstripbooks&field-keywords=' + name, headers = user_agent)
    soup = BeautifulSoup(r.text)
    div = soup.find('div', class_='a-row a-spacing-small')
    books = []
    for d in soup.find_all('div', class_='a-row a-spacing-small'):
        books.append(d.a.text.strip())
    return books


def searchPublish(publish, isbn10, isbn13):
    if publish.find('Cambridge University Press') != -1:
        getCambridgeContents(isbn13)    
    if publish.find('springer') != -1:
        getSpringerContents(isbn13)
    if publish.find('Reilly Media') != -1:
        getOreillyContents(isbn13)
    if publish.find('apress') != -1:
        getApressContents(isbn13)

def getApressContents(isbn):
    url = 'http://www.apress.com/' + isbn
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    div = None

    for d in soup.find_all('div', class_='tab-content'):
        if d.h3 != None and d.h3.text.strip() == 'Table of Contents':
            div = d
            break
    sp = BeautifulSoup(div.prettify())
    for p in sp.find_all('p'):
        print utils.removeDoubleSpace(p.text.strip()).strip()

def getOreillyContents(isbn):
    url = utils.getEnginUrlEx('oreilly', isbn)
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    div = soup.find('div', class_='book_text')
    url =  div.a['href']
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    lis = soup.find_all('li', class_='chapter')
    for li in lis:
        if li.h3 != None:
            print li.h3.text.strip()
        sp = BeautifulSoup(li.prettify())
        for li2 in sp.find_all('li', class_='sect1'):
            print '    ' + li2.h4.text.strip()

def getSpringerContents(isbn):
    
    url = 'http://www.springer.com/cn/book/' + isbn
    r = requests.get(url)
    print url
    soup = BeautifulSoup(r.text)
    for div in soup.find_all('div', class_='main'):
        print div.p.text

def getCambridgeContents(isbn):
    url = utils.getEnginUrlEx('Cambridge', isbn)
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    li = soup.find('li', id='contentsTab')
    content = li.div.p.prettify().split('<br/>')
    for c in content:
        print utils.clearHtmlTag(c.strip()).strip()
    
     

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
    return (publish, isbn10, isbn13)

def usage(argv0):
    return ''

def main(argv):
    keyword = ''
    lang_en = ''
    publish = ''
    isbn = ''
    try:
        opts, args = getopt.getopt(argv[1:], 'hn:l:p:i:', ["help", "name", "lang", "publish", "isbn"])
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
        if o in ('-l', '--lang'):
            lang_en = a
        if o in ('-p', '--publish'):
            publish = a
        if o in ('-i', '--isbn'):
            isbn = a

    if keyword != '':
        if lang_en == 'en':
            searchAmazon(keyword, publish, isbn)
        else:
            searchAmazonCN(keyword, publish, isbn)

if __name__ == '__main__':
    main(sys.argv)
