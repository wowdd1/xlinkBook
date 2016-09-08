#!/usr/bin/env python

from spider import *
sys.path.append("..")
from utils import Utils

class BerkeleySpider(Spider):
    def __init__(self):
        Spider.__init__(self)
        self.school = "berkeley"
        self.utils = Utils()

    def processSubject(self, subject , url):
        r = requests.get(url)
        #print r.text
        desc = ''
        code = ''
        title = ''
        link = ''
        file_name = self.get_file_name(subject, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for line in r.text.split('\n'):
            line = line.strip()
            if line.startswith('<span class="title">'):
                title = self.utils.clearHtmlTag(line)
            elif line.startswith('<span class="code">'):
                code = self.utils.clearHtmlTag(line).replace('&#160;', '').replace(' ', '')
            elif line.startswith('<a href="/search/?P='):
                link = 'http://guide.berkeley.edu' + line[line.find('"') + 1 : line.find('"', line.find('"') + 1)]
            elif line.startswith('<p class="courseblockdesc">'):
                #desc = self.utils.clearHtmlTag(line)
                print code + ' ' + title
                self.count += 1
                self.write_db(f, code, title, link)

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def doWork(self):
        r = requests.get('http://guide.berkeley.edu/courses/')
        for line in r.text.split('\n'):
            if line.startswith('<li><a'):
                subject = self.utils.clearHtmlTag(line)
                subject = subject[0 : subject.find('(')].strip()
                if subject == 'Computer Science' or subject == 'Electrical Engineering':
                    continue
                if self.need_update_subject(subject):
                    print subject 
                    link = 'http://guide.berkeley.edu' + line[line.find('"') + 1 : line.find('"', line.find('"') + 1)]
                    self.processSubject(subject, link)
start = BerkeleySpider()
start.doWork()                        
