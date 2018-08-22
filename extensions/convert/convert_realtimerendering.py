#!/usr/bin/env python
# -*- coding: utf-8-*-  

import sys
import getopt
import requests
import json
from bs4 import BeautifulSoup



def convert(source, crossrefQuery=''):

    r = requests.get(source)

    soup = BeautifulSoup(r.text)

    count = 0

    '''
    all_links = []

    for a in soup.find_all('a'):

        if a.has_key('href'):
            all_links.append(a.text.replace('\n', ' ').strip() + '(' + a['href'] + ')')

    line = ', '.join(all_links)
    print line.encode('utf-8')
    return 'w'

    '''

    if source.find('kesen') != -1:
        for dl in soup.find_all('dl'):
            soup1 = BeautifulSoup(dl.prettify())
            for dt in soup1.find_all('dt'):
                title = dt.text.strip().replace('\n', '')
                url = ''
                if dt.a != None:
                    url = dt.a['href']
                #if title.startswith('('):
                #    continue
                if title.find('(') != -1:
                    title = title[0 : title.find('(')].strip()
                line = ' | ' + title + ' | ' + url + ' | '
                print line.encode('utf-8')

        return
    elif source.find('refs.html') != -1:

        for li in soup.find_all('li'):
            title = ''
            url = ''
            author = ''
            desc = ''
            text = li.text.strip().replace('\n', ' ').encode('utf-8')
            links = ''

            if text.find('http') != -1:
                links = text[text.find('http') : ]
                text = text[0 : text.find('http')]

            if text.find(',') == -1:
                continue


            if li.a != None:
                url = li.a.text.encode('utf-8')

            start = text.find('"')
            end = text.find('"', start + 1)

            if start != -1 and start < end:

                title = text[start + 1 : end - 1]
                author = 'author:' + text[0 : start].replace(', and', ', ').strip()
                if author.endswith(','):
                    author = author[0 : len(author) - 1]

                desc = 'description:' + text[end + 1 :].strip()
            else:
                title = text

            count += 1


            line = ' | ' + title + ' | ' + url + ' | ' + author + ' ' 
            if links != '':
                line += 'website:' 

                linksList = links.split(' ')
                linkCount = 0
                for a in linksList:
                    if a.find(',') != -1:
                        a = a.replace(',', '')
                    linkText = a.strip()
                    if linkText.endswith('/'):
                        linkText = linkText[0 : len(linkText) - 1]
                    if linkText.find('/') != -1:

                        linkText = linkText[linkText.rfind('/') + 1 : ]
                        
                    linkText = linkText.replace('"', '').replace("'", '')
                    if len(linksList) == 1 and len(linkText) > 60:
                        linkText = linkText[0 : 60]
                    elif len(linksList) > 1 and len(linkText) > 15:
                        linkText = linkText[0 : 15]
                    if linkText == '':
                        linkText = 'link'
                    #line += '<a target="_blank" href="' + a + '">' + linkText + '</a>'
                    line += linkText + '(' + a + ')'
                    linkCount += 1
                    #domainStatistics(linkText, a)
                    if linkCount < len(linksList):
                        line += ', '

            line += ' ' + desc

            print line

    elif source.find('refs3') != -1 or source.find('refs2') != -1 or source.find('refs1') != -1:

        for li in soup.find_all('li'):
            title = ''
            url = ''
            author = ''
            desc = ''
            text = li.text.strip().replace('\n', '').encode('utf-8')
            if text.find('.') == -1 and text.find(',') == -1:
                continue
            start = text.find('"')
            end = text.find('"', start + 1)

            if start != -1 and start < end:

                title = text[start + 1 : end - 1]
                author = 'author:' + text[0 : start].replace(', and', ', ').strip()
                if author.endswith(','):
                    author = author[0 : len(author) - 1]
                desc = 'description:' + text[end + 1 :].strip()


            else:
                if li.i != None:
                    title = li.i.text.encode('utf-8')
                else:
                    title = text

            if li.a != None:
                url = li.a['href'].encode('utf-8').replace('\n', '')

            line = ' | ' + title + ' | ' + url + ' | ' + author + ' ' + desc
            count += 1

            print line

    elif source.find('books') != -1:
        lastTitle = ''
        for tr in soup.find_all('tr'):
            if tr != None and tr.td != None and tr.td.b != None:

                count += 1
                title = tr.td.b.text.replace('\n', ' ')
                url = ''
                if lastTitle == title:
                    continue
                lastTitle = title

                if tr.td.a != None:
                    url = tr.td.a['href']
                print ' | ' + title + ' | ' + url + ' | '

    elif source.find('blog') != -1:
        for page in range(1, 48):
            url = source + 'page/' + str(page)

            #print url
            if page != 1:
                r = requests.get(url)
                soup = BeautifulSoup(r.text)

            line = ''
            for item in soup.find_all('div', class_='meta'):

                if item.h2 != None:

                    line = ' | ' + item.h2.text.replace('\n', '').strip() + ' | ' + item.h2.a['href'] + ' | '
                    print line.encode('utf-8')
                    count += 1

            if line == '':
                break


    print 'Total ' + str(count) + ' records'
    '''
    if len(domainDict) > 0:
        for item in sorted(domainDict.items(), key=lambda domainDict:int(len(domainDict[1])), reverse=True):
            website = 'website:'
            siteDict = {}
            for site in sorted(item[1], reverse=True):
                if siteDict.has_key(site):
                    continue
                else:
                    siteDict[site] = site
                website += site + ', '
            website = website.strip()
            if website.endswith(','):
                website = website[0 : len(website) - 1]

            print ' | ' + item[0] + ' - ' + str(len(item[1])) + ' | ' + item[0] + ' | ' + website
    '''
'''   
domainDict = {}
def domainStatistics(text, url):
    if url.startswith('http') == False:
        return
    url = url.replace('https', 'http').replace('www.', '')
    domain = url
    index = url.find('/', url.find('://') + 3)
    if index != -1:
        domain = url[0 : index]
    if text == '':
        text = 'link'
    text = text.replace('%20', ' ').replace('%', '').strip()

    if url.endswith('/') == False:
        url += '/'
    if domainDict.has_key(domain):
        domainDict[domain].append(text + '(' + url + ')')
    else:
        domainDict[domain] = [text + '(' + url + ')']
'''

def main(argv):
    source = ''
    crossrefQuery = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'u:q:', ["url", "crossrefQuery"])
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)


    for o, a in opts:

        if o in ('-u', '--url'):
            source = a
        if o in ('-q', '--crossrefQuery'):
            crossrefQuery = a

    if source == "":
        print "you must input the input file or dir"
        return

    convert(source, crossrefQuery=crossrefQuery)


if __name__ == '__main__':
    main(sys.argv)
    