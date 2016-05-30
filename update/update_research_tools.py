#!/usr/bin/env python

# -*- coding: utf-8 -*-
from spider import *

class ResrarchToolsSpider(Spider):

    def __init__(self):
        Spider.__init__(self)
        self.category = self.category_obj.tools


    def doWork(self):
        r = requests.get('http://connectedresearchers.com/online-tools-for-researchers/')
        soup = BeautifulSoup(r.text)
        div = soup.find('div', class_="entry-content")
        soup = BeautifulSoup(div.prettify())
        tools_dict = {}
        file_name = self.get_file_name('other/research-tools', "connectedresearchers")
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for li in soup.find_all('li'):
            if li.a != None and li.a['href'] != '':
                key = li.a.text.strip()
                print key
                desc =li.text[li.text.find(key) + len(key) : li.text.find('.')].strip()
                desc = desc[desc.find(' ') : ].strip().replace('\n', '')
                print desc
                if tools_dict.has_key(key) == False:
                    tools_dict[key] = desc
                    self.count += 1
                    self.write_db(f, 'research-tool-' + str(self.count), key, li.a['href'], "description:" + desc)
         
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n" 
                


start = ResrarchToolsSpider()
start.doWork()
