#!/usr/bin/env python
# -*- coding: utf-8-*-
#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07

from spider import *

class NetEasySpider(Spider):

    #163 ocw
    #"""
    def __init__(self):
        Spider.__init__(self)
        self.school = "neteasy"
        self.urls = { '163ocw' : "http://open.163.com/ocw/",\
                      '163cnocw' : "http://open.163.com/cuvocw/"}

    def process163Data(self, soup, subject):
        #if self.need_update_subject(self.subject) == False:
        #    return
        file_name = self.get_file_name('videos/' + subject, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
        for div in soup.find_all("div", class_ = "g-cell1 g-card1"):
            self.count = self.count + 1
            course_num = "163-ocw-" + str(self.count)
            for a in div.find_all("a"):
                if a.attrs.has_key("class") == False:
                    #print a.h5.string
                    #print a["href"]
                    title = ""
                    if a.h5.string == None:
                        pos = str(a.h5).find(">", 3)
                        title = str(a.h5)[pos + 1: str(a.h5).find("<" , pos)]
                    else:
                        title = a.h5.string
                    desc = title
                    if title.find('《') != -1:
                        title = title.replace('《','$')
                        title = title.replace('》','%')
                        title = title[title.find('$') + 1 : title.find('%')].strip()
                    self.write_db(f, course_num, title, str(a["href"]), 'description:' + desc)

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def doWork(self):
        print "downloading 163 ocw info"
        for subject, url in self.urls.items():
            r = requests.get(url)
            soup = BeautifulSoup(r.text)

            self.process163Data(soup, subject)



start = NetEasySpider()
start.doWork();
