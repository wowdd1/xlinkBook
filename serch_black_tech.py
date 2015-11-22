#! /usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup


list_all = {"", "微软", "谷歌", "facebook"}

for a in list_all:
    for i in range(0, 5):
        r = requests.get('https://www.google.com.hk/search?newwindow=1&safe=strict&biw=1436&bih=782&ei=MLlRVpjyB8iXsAHGt43wAQ&start=' + str(i * 10)+ '&sa=N&q=' + a + '黑科技')
        sp = BeautifulSoup(r.text)
        for h3 in sp.find_all('h3', class_='r'):
            print h3.text
            #print h3.prettify()[h3.prettify().find('http') : h3.prettify().find('"', h3.prettify().find('http'))].strip()
            #print '\n'
    print '\n\n\n'
