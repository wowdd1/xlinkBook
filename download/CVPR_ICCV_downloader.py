#!/usr/bin/env python

#!/usr/bin/python
import urllib,urllib2
from bs4 import *
import requests
import os

url_dict = {}
r = requests.get('http://www.cv-foundation.org/openaccess/menu.py')
soup = BeautifulSoup(r.text)
for a in soup.find_all('a'):
    if a.text == 'Main Conference':
        key = a['href'][a['href'].find('openaccess') + 11 :]
        key = key[0 : key.find('.')]
        url_dict[key] = a['href']

for key in url_dict.keys():

    #pre-created folder
    paperpath = './' + key + '/'

    if os.path.exists(paperpath) == False:
        os.makedirs(paperpath)

    print 'Start to download all ' + key + ' papers...'
    url = url_dict[key]
    req = urllib2.Request(url,headers={'User-Agent' : "Magic Browser"})
    page = urllib2.urlopen(req)

    #parse
    soup = BeautifulSoup(page.read())

    #content div
    content_div = soup.find('div', {'id':'content'}) 

    for item in content_div.findAll('dt',{'class':'ptitle'}):
        pdflink = item.findAll('a')[0]
        url_paper = pdflink.get('href')
        url_paper = 'http://www.cv-foundation.org/openaccess/' + url_paper
        print url_paper
    
        name = pdflink.contents
        forbidden = '\\/:*?"<>|'
        for c  in name:
            for c in forbidden:
                name[0] = name[0].replace(c,'')   
        name = paperpath + name[0] + '.pdf'
 
        pdfpage = urllib2.urlopen(url_paper)
        f = open(name, 'wb')
        f.write(pdfpage.read())
        f.close()

    print 'End.'
