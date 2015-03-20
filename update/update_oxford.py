#!/usr/bin/env python

from spider import *

class OxfordSpider(Spider):
    
    def __init__(self):
        Spider.__init__(self)
        self.school = 'oxford'


    def doWork(self):
        r = requests.get('https://www.cs.ox.ac.uk/teaching/courses/')
        soup = BeautifulSoup(r.text)

        file_name = self.get_file_name('eecs', self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for a in soup.find_all('a'):
            if a.attrs.has_key("href") and a['href'].startswith('/teaching/courses'):
                print a.text
                self.count += 1
                self.write_db(f, self.school + '-' + str(self.count), a.text, 'https://www.cs.ox.ac.uk' + a['href'])

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

start = OxfordSpider()
start.doWork()
