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


    if source.find('refs.html') != -1:

        for li in soup.find_all('li'):
            title = ''
            url = ''
            author = ''
            desc = ''
            text = li.text.strip().replace('\n', '').encode('utf-8')
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


            line = ' | ' + title + ' | ' + url + ' | ' + author + ' ' + desc
            if links != '':
                line += '<br>' + links.replace(',', '<br>')

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


    print 'Total ' + str(count) + ' records'

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
    