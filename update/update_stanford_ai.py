#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2015.01.03

from spider import *

class StanfordAISpider(Spider):

    def __init__(self):
        Spider.__init__(self)
        self.school = "stanford"
        self.subject = "eecs"

    def doWork(self):
        r = requests.get('http://ai.stanford.edu/courses/')
        soup = BeautifulSoup(r.text)


        file_name = self.get_file_name(self.subject + '/ai', self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for tr in soup.find_all('tr'):
            data = tr.text.strip().split('\n')
            if len(data) == 4:
                url = tr.td.a['href']
                course_id = data[0]
                title = data[2]
                instructors = data[3]
                print course_id + ' ' + title + ' ' + instructors + ' ' + url
                self.count += 1
                self.write_db(f, 'stanford-ai-' + str(self.count), title, url, 'instructors:' + instructors)

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

start = StanfordAISpider()
start.doWork()
