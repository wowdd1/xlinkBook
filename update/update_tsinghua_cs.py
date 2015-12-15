#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com

from spider import *

class TsinghuaSpider(Spider):

    def __init__(self):
        Spider.__init__(self)
        self.school = "tsinghua"
        self.subject = "eecs"

    def doWork(self):
        file_name = self.get_file_name(self.subject, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        r = requests.get('http://iiis.tsinghua.edu.cn/en/list-127-1.html')
        soup = BeautifulSoup(r.text)
        table = soup.find('table', class_='t_table')
        soup = BeautifulSoup(table.prettify())
        for a in soup.find_all('a'):
            if a.attrs.has_key("href") and a['href'].startswith('list') and len(a.text.strip()) > 2:
                title = a.text.strip()
                print title
                url = 'http://iiis.tsinghua.edu.cn/en/' + a['href']
                self.count += 1
                self.write_db(f, 'tsinghua-cs-' + str(self.count), title, url)

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

start = TsinghuaSpider()
start.doWork()
