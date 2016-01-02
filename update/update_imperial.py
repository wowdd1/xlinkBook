#! /usr/bin/env python


from spider import *


class ImperialSpider(Spider):
    def __init__(self):
        Spider.__init__(self)
        self.school = "imperial"


    def doWork(self):
        r = requests.get('http://www.imperial.ac.uk/study/pg/courses/by-department/')
        soup = BeautifulSoup(r.text)
        for li in soup.find_all('li', class_='link-list'):
            subject = li.a.text
            if self.need_update_subject(subject) == False:
                continue
            ol = BeautifulSoup(li.ol.prettify())
            print subject

            file_name = self.get_file_name(subject, self.school)
            file_lines = self.countFileLineNum(file_name)
            f = self.open_db(file_name + ".tmp")
            self.count = 0

            for li in ol.find_all('li', class_='course'):
                title = li.a.h4.text.strip()
                url = "http://www.imperial.ac.uk" + li.a['href']
                self.count += 1 
                self.write_db(f, self.school + "-" + subject.lower() + "-" +str(self.count), title, url)

            self.close_db(f)
            if file_lines != self.count and self.count > 0:
                self.do_upgrade_db(file_name)
                print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
            else:
                self.cancel_upgrade(file_name)
                print "no need upgrade\n"

start = ImperialSpider()
start.doWork()
