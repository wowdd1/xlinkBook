#!/usr/bin/env python

from spider import *

class ColumbiaSpider(Spider):
    def __init__(self):
        Spider.__init__(self)
        self.school = 'columbia'
        self.term = ''
        self.id = ''
        self.title = ''
        self.course_dict = {}


    def processCourses(self, f, url):
        print url
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        for tr in soup.find_all('tr'):
            if tr.text.find('ColumbiaWeb') == -1 and tr.text.find('NOTE:') == -1:
                if tr.text.startswith('Section'):
                    if self.course_dict.has_key(self.id):
                        continue
                    else:
                        self.course_dict[self.id] = ''

                    url = 'http://www.columbia.edu' + tr.a['href']
                    if tr.text.find('Instructor') != -1:
                        instructors = 'instructors:' + tr.text[tr.text.find('Instructor') + 12 :].strip().replace(' and', ',')
                        print instructors
                    self.count += 1
                    self.write_db(f, 'columbia-' + self.id.lower(), self.title, url, self.term + ' ' + instructors)
                else:
                    data = tr.td.b.prettify().replace('\n', '').split('<br/>')
                    self.term = data[0][data[0].find('>') + 1 :].strip()
                    self.id = self.term[self.term.rfind(' ') : ].strip()
                    self.term = 'term:' + self.term[0 : self.term.find(' ', self.term.find(' ') + 1)]
                    if self.term.endswith(':'):
                        self.term = ''
                    self.title = data[1][0 : data[1].find('<')].strip().replace('&amp;', '')
                    print self.title
                    print self.id
                    print self.term


    def doWork(self):
        r = requests.get('http://www.columbia.edu/cu/bulletin/uwb/home.html')
        soup = BeautifulSoup(r.text)
        for a in soup.find_all('a'):
            if a['href'].find('sel/dept-') != -1:
                print a['href']
                r2 = requests.get('http://www.columbia.edu/cu/bulletin/uwb/' + a['href'])
                soup2 = BeautifulSoup(r2.text)
                for tr in soup2.find_all('tr'):
                    if tr.text.strip().startswith(a['href'][a['href'].find('-') + 1 : a['href'].find('.')]):
                        if tr.td != None and tr.td.text.find('\n') == -1 and tr.a != None and tr.a['href'].find('bulletin') != -1:
                            subject = tr.td.text
                            subject = subject.replace('(', '').replace(')', '')
                            if self.need_update_subject(subject) == False:
                                continue
                            soup3 = BeautifulSoup(tr.prettify())


                            file_name = self.get_file_name(subject, self.school)
                            file_lines = self.countFileLineNum(file_name)
                            f = self.open_db(file_name + ".tmp")
                            self.count = 0
                                                            
                            self.course_dict = {}

                            for a in soup3.find_all('a'):
                                self.processCourses(f, 'http://www.columbia.edu' + a['href'])
                            
                            self.close_db(f)
                            if file_lines != self.count and self.count > 0:
                                self.do_upgrade_db(file_name)
                                print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
                            else:
                                self.cancel_upgrade(file_name)
                                print "no need upgrade\n"

        print 'ok'

    def neurosciencephd(self):
        r = requests.get('http://www.neurosciencephd.columbia.edu/course-listing')
        soup = BeautifulSoup(r.text)
        for tr in soup.find_all('tr'):
            if tr.text.find('Department') == -1:
                count = 0
                title = ''
                i = ''
                for item in tr.text.strip().split('\n'):
                    if item.strip() != '':
                        count += 1
                        if count == 1:
                            title =  item.strip()
                        if count == 3:
                            i =  item.strip()
                        if count == 8:
                            print i + ' | ' + title + ' | | instructors:' + item.strip()

start = ColumbiaSpider()
start.doWork()
