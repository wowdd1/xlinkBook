#!/usr/bin/env python


from spider import *

class BigDataUniversitySpider(Spider):
    def __init__(self):
        Spider.__init__(self)
        self.school = 'BigDataUniversity'
        self.subject = 'data-science'


    def doWork(self):
        r = requests.get('http://bigdatauniversity.com/wpcourses/')
        soup = BeautifulSoup(r.text)


        file_name = self.get_file_name('data-science/bigdata', self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0


        for div in soup.find_all('div', class_='media-body'):
            title = div.h3.a.text.strip()
            print title
            instructors = 'instructors:'
            if div.p != None:
                instructors += div.p.strong.text
            self.count += 1
            self.write_db(f, "bigdata-" + str(self.count), title, div.h3.a['href'], instructors)

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

start = BigDataUniversitySpider()
start.doWork()

