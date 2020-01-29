#!/usr/bin/env python
# -*- coding: utf-8-*-  

import sys
import getopt
import requests
import json
from bs4 import BeautifulSoup



def convert(source, crossrefQuery=''):

    #headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
    headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

    #print source
    r = requests.get(source, headers=headers)
    #print source
    soup = BeautifulSoup(r.text)

    #
    #print source
    #print r.text


    for div in soup.find_all('div', class_='all_data'):
        #print div
        sp = BeautifulSoup(div.prettify())

        steamDiv = sp.find('div', class_='streaming_data')

        wmvDivs = sp.find_all('div', class_='wmv-text')

        titleDiv = sp.find('div', class_='presentationTitle')

        authorDiv = sp.find('div', class_='speakers')

        descDiv = sp.find('div', class_='keyword_data')

        url = ''
        author = ''
        desc = ''
        title = ''
        website = ''

        if steamDiv != None:

            url = steamDiv.a['href']

            url = url[url.find("http") : ]
            if url.find("'") != -1:
                url = url[0 : url.find("'")]
            website += "Video(" + url + "), "
        elif wmvDivs != None:
            for wmvDiv in wmvDivs:
                if wmvDiv.a.text.lower().find('mp4') != -1:
                    url = wmvDiv.a['href']
                    website += "Video(" + wmvDiv.a['href'] + "), "
                elif wmvDiv.a.text.lower().find('pdf') != -1:
                    website += "PDF(" + wmvDiv.a['href'] + "), "

        if website != '':
            website = 'website:' + website[0 : len(website) - 2]

        if authorDiv != None:
            author = 'author:' + removeDoubleSpace(authorDiv.text.strip().replace('\n', '')).replace(' ,', ',')
        if descDiv != None:
            desc = 'description:' + descDiv.text.strip().replace('\n', '')
        if titleDiv != None:
            title = titleDiv.text.strip().replace('\n', '')

        #https://developer.nvidia.com/gtc/2019/video/S91023
        if source.find('2019') != -1:
            url = url[url.find('gtc') : ]
            part = url[url.rfind('/') + 1 :].lower()
            url = 'https://developer.download.nvidia.com/video/gputechconf/' + url + '/' + part + '-' + title.lower().replace('&', 'and').replace('(', ' ').replace(')', '').replace(': ', '-').replace('"', '').replace("'", '').replace(' ', '-')
            url += '.mp4'
        line = ' | ' + title + ' | ' + url + ' | ' + website + ' ' + author + ' ' + desc 

        print line.encode('utf-8')
def removeDoubleSpace(text):
    text = text.replace('\n',' ')
    while (text.find('  ') != -1):
        text = text.replace('  ', ' ')
    return text

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
    #print 'start'
    convert(source, crossrefQuery=crossrefQuery)


if __name__ == '__main__':
    main(sys.argv)
    