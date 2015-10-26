#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07

from spider import *

class OCWSpider(Spider):

    def __init__(self):
        Spider.__init__(self)
        self.school = "ocw"

    def getGoogleOCWData(self):

        file_name = self.get_file_name("ocw/google-school-ocw", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for pager in range(0, 21):
            #r = requests.get("https://www.google.com.hk/search?q=ocw&newwindow=1&safe=strict&es_sm=119&ei=Ha8tVoq6B8GisAH0mICwAw&start=" + str(pager * 10) + "&sa=N&biw=1436&bih=782")
            r = requests.get('https://www.google.com.hk/search?q=ocw&newwindow=1&safe=strict&es_sm=119&biw=1436&bih=292&ei=ALgtVqneN4uisAHGxKm4Aw&start=' + str(pager * 10) + '&sa=N')
            soup = BeautifulSoup(r.text)
            for h3 in soup.find_all('h3', class_='r'):
                title = h3.a.text
                url = h3.a['href'][h3.a['href'].find('http') : h3.a['href'].find('&')]
                if len(url) < 30:
                    if url.find('.edu') != -1 or url.find('ocw.') != -1:
                        print title + "  " + url
                        self.count += 1
                        self.write_db(f, 'school-ocw-' + str(self.count), title, url)


        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def get50OCWData(self):
        r = requests.get('http://onlineuniversityrankings2010.com/2010/open-edu-top-50-university-open-courseware-collections/')
        soup = BeautifulSoup(r.text)
        div = soup.find('div', class_='post-46 post post_box')
        soup = BeautifulSoup(div.prettify())

        file_name = self.get_file_name("ocw/50school-ocw", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
        for li in soup.find_all('li'):
            if li.a != None:
                self.count += 1
                print str(self.count)  + " " + li.a.text.strip()
                self.write_db(f, "50school-ocw-" + str(self.count), li.a.text.strip(), li.a['href'])

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def doWork(self):
        self.getGoogleOCWData()
        self.get50OCWData()
start = OCWSpider()
start.doWork()
