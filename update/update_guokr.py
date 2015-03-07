#!/usr/bin/env python

from spider import *

class GuokrSpider(Spider):
    def __init__(self):
        Spider.__init__(self)
        self.school = 'guokr'
        self.base_url = 'http://mooc.guokr.com'

    def processData(self, dept_id, subject, short_subject_name):
        print 'process ' + subject
        total = -1000
        offset = 0 
        step = 100

        file_name = self.get_file_name(subject + '/' + self.school + '/' + subject, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        title = ''
        course_id = ''
        url = ''
        desc = ''
        while True:
            r = requests.get(self.base_url + '/apis/academy/course_list.json?dept_id=' + dept_id + '&order=grading&retrieve_type=by_params&limit=' + str(step) + '&offset=' + str(offset))
            jobj = json.loads(r.text)
            if total == -1000:
                total = int(jobj['total'])
            for c in jobj['result']['courses']:
                self.count += 1
                course_id = self.school + '-' + short_subject_name + '-' + str(self.count)
                title = c['name'].strip()
                url = c['url']
                desc = 'platform:' + c['platform'] + ' description:' + c['school'] + ' ' + c['date_status']
                print course_id + ' ' + title
                self.write_db(f, course_id, title, url, desc.strip())
           
            total -= step
            offset += step
            if total <= 0:
                break;
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def doWork(self):
        r = requests.get(self.base_url + '/course/')
        soup = BeautifulSoup(r.text)
        li = soup.find('li', class_='search-field category')
        soup = BeautifulSoup(li.prettify())
        for li in soup.find_all('li'):
            if li.a.attrs.has_key('data-id'):
                data_id = li.a['data-id']
                if data_id == '52':
                    self.processData(data_id, 'Computer Science', 'cs')
                if data_id == '55':
                    self.processData(data_id, 'Math', 'math')
                if data_id == '30':
                    self.processData(data_id, 'Electronics', 'ee')


start = GuokrSpider()
start.doWork()

