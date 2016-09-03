#!/usr/bin/env python

from spider import *
import time

class NatureIndexSpider(Spider):

    def __init__(self):
        Spider.__init__(self)
        self.school = "natureindex"


    def doWork(self):
        year = int(time.strftime('%Y',time.localtime(time.time())))
        for institution in ['all', 'chemistry', 'earth-and-environmental', 'life-sciences', 'physical-sciences', 'nature-science']:
            r = requests.get('http://www.natureindex.com/annual-tables/' + str(year) + '/institution/all/' + institution)
            soup = BeautifulSoup(r.text)
            self.count = 0

            file_name = self.get_file_name('rank/' + self.school + '/' + institution, self.school)
            file_lines = self.countFileLineNum(file_name)
            f = self.open_db(file_name + ".tmp")

            for tr in soup.find_all('tr'):
                if tr.a != None:
                    self.count += 1
                    url = "http://www.natureindex.com" + tr.a['href']
                    text = tr.a.text.strip()
                    title = text[0 : text.find(',')].strip()
                    if title.find('(') != -1:
                        title = title[0 : title.find('(')].strip()
                    desc = text[text.find(',') + 1 :].strip()
                    id = 'natureindex-' + institution + '-' + str(tr.td.text.strip())
                    print str(tr.td.text.strip()) + ' ' + title

                    self.write_db(f, id, title, url, 'description:' + desc)



            self.close_db(f)
            if file_lines != self.count and self.count > 0:
                self.do_upgrade_db(file_name)
                print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
            else:
                self.cancel_upgrade(file_name)
                print "no need upgrade\n"


start = NatureIndexSpider()
start.doWork()
