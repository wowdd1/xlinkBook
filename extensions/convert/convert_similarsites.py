#!/usr/bin/env python
# -*- coding: utf-8-*-  

import sys
import getopt
import requests
import json
from bs4 import BeautifulSoup



def convert(source, crossrefQuery=''):

    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',\
               'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',\
               'Accept-Encoding' : 'gzip, deflate, br',\
               'Host' : 'www.similarsites.com',\
               'Cache-Control' : 'max-age=0',\
               'Connection' : 'keep-alive',\
               'Cookie' : 'D_IID=C6664628-C7B1-3869-AB01-73F16A25D896; D_UID=659B443D-3A88-3F2E-9201-3D26CF961980; D_ZID=3B93D359-B6B4-3064-AA21-135491563117; D_ZUID=2F983948-8701-3AE6-A2AA-F201F5205DEE; D_HID=CE9991F3-B49C-3A04-B004-E60B442BBA62; D_SID=110.52.225.214:fNwMMze7oCOYgkspU8o/oYkCE5TwwfXaUfVvMiAKFrw; _ga=GA1.2.1972242299.1547446106; _gid=GA1.2.593946926.1547446106; locale=en-us; __qca=P0-1755514587-1547446107047; sc_is_visitor_unique=rx4713989.1547451388.D0E84B764F2D4F77199BA17CD19E4759.2.2.2.2.2.2.2.2.2'}


    charList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    index = 0
    #charList = ['s']

    for char in charList:

        for i in range(0, 19):

            index += 1
            url = source + '/' + char + '/' + str(index)
    
            r = requests.get(url, headers=headers)
    
            soup = BeautifulSoup(r.text)  

            div = soup.find('div', id='title')

    
            if div != None and div.text.find('Sorry,') != -1:
                index = 0
                break

            print '#' + url

            trList = soup.find_all('tr')

            for tr in trList:
    
                if tr.a != None and tr.a['href'].startswith('/site'):
                    print tr.a.text.encode('utf-8')
            
            
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
    