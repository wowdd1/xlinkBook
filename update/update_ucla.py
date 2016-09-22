#!/usr/bin/env python

from spider import *
sys.path.append("..")
from record import Record

class UclaSpider(Spider):

    def __init__(self):
        Spider.__init__(self)
        self.school = 'ucla'
    '''

    def getCourseHomePage(self, url):
        r = None
        try:
            r = requests.get(url)
        except Exception , e:
            print e
            return url
        soup = BeautifulSoup(r.text)
        for a in soup.find_all('a'):
            if a.text.strip() == 'Course Webpage':
                return a['href']
        return url

    def processData(self, subject, subject_code, term_list):
        if self.need_update_subject(subject) == False:
            return
        print "downloading ucla " + subject + " course info"
        subject_code = subject_code.replace(' ', '+')

        file_name = self.get_file_name(subject, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        course_dict = {}
        for term in term_list:
            url = "http://www.registrar.ucla.edu/schedule/crsredir.aspx?termsel=" + term + '&subareasel=' + subject_code
            print 'requesting ' + url
            r = requests.get(url) 
            soup = BeautifulSoup(r.text)
            for option in soup.find_all('option'):
                course_num = option.text[0 : option.text.find('-')].strip().replace(' ', '')

                title = option.text[option.text.find('-') + 1 : ].strip()
                link = self.getCourseHomePage('http://www.registrar.ucla.edu/schedule/detselect.aspx?termsel=' + term\
                                             + '&subareasel=' + subject_code + '&idxcrs=' + option['value'].replace(' ', '+'))

                if course_dict.get(course_num, '') == '':
                    print course_num + ' ' + title + ' ' + link
                    course_dict[course_num] = Record(self.get_storage_format(course_num, title, link, ''))

        for k, record in [(k,course_dict[k]) for k in sorted(course_dict.keys())]:
            self.count += 1
            self.write_db(f, record.get_id().strip(), record.get_title().strip(), record.get_url().strip())
                
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"


    def doWork(self):
        r = requests.get('http://www.registrar.ucla.edu/schedule/schedulehome.aspx')
        soup = BeautifulSoup(r.text)
        i = 0
        term_list = []
        for option in soup.find_all('option'):
            i += 1
            if i < 5:
                term_list.append(option['value'])
            else:
                self.processData(option.text, option['value'], term_list)

    '''

    def processData(self, subject, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text)

        file_name = self.get_file_name(subject, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for div in soup.find_all('div', class_='media-body'):
            data = div.text.split('\n')
            title = data[1].strip()
            id = title[0 : title.find('.')]
            title = title[title.find('.') + 1 :].strip()
            print id + ' ' + title
            desc = data[len(data) - 2].strip()
            self.count += 1
            self.write_db(f, id, title, '', 'description:' + desc)

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"



    def doWork(self):
        r = requests.get('http://registrar.ucla.edu/Academics/Course-Descriptions')
        soup = BeautifulSoup(r.text)
        for li in soup.find_all('li'):
            if li.a != None and li.a['href'].find('Course-Details') != -1:
                if self.need_update_subject(li.a.text) == False:
                    continue
                print li.a.text
                self.processData(li.a.text, 'http://registrar.ucla.edu' + li.a['href'])


start = UclaSpider()
start.doWork()

