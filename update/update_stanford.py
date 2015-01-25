#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2015.01.03

from spider import *
from update_stanford_cs import StanfordCSSpider

class StanfordSpider(Spider):
    include_unoffered_courses = False
    
    def __init__(self):
        Spider.__init__(self)
        self.school = "stanford"
        self.subject = "eecs"
        self.deep_mind = True
        self.records_dict = StanfordCSSpider().getRecordsDict()

    def getRealUrl(self, course_num):
        test_url = 'http://' + course_num + '.stanford.edu'
        backup_url = "https://explorecourses.stanford.edu/search?q=" + course_num
        try:
            r = requests.get(test_url)
        except Exception , e:
            return backup_url
        
        if r.status_code == 200:
            return test_url
        else:
            return backup_url 

    def processData(self, subject, url):
        if self.need_update_subject(subject) == False:
            return
        print "processing " + subject + " " + url

        r = requests.get(url)
        soup = BeautifulSoup(r.text); 
        course_num_list = []
        course_name_list = []
        course_description_list = []
        course_instructors_list = []

        file_name = self.get_file_name(subject, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for span in soup.find_all("span", attrs={"class": "courseNumber"}):
            course_num_list.append(span.text[0:len(span.text) - 1].replace(' ', ''))

        for span in soup.find_all("span", attrs={"class": "courseTitle"}):
            course_name_list.append(span.text.strip().strip())

        for div in soup.find_all("div", attrs={"class": "courseDescription"}):
            course_description_list.append(div.text.strip()) 
        i = 0
        for div in soup.find_all("div", attrs={"class": "courseAttributes"}):
            i += 1
            if i % 2 == 0:
                if div.text.strip().lower().find('instructors:') == -1:
                    course_instructors_list.append('')
                    i -= 1
                    continue
                course_instructors_list.append(div.text.strip().replace('\n', '').replace('Instructors: ;', '').strip())

        for i in range(0, len(course_num_list)):
            print course_num_list[i] + " " + course_name_list[i]
            if subject == 'Computer Science' and self.records_dict.get(course_num_list[i], '') != '' \
                       and self.records_dict.get(course_num_list[i]).get_instructors().find('none listed') == -1:
                description = "instructors:" + self.records_dict.get(course_num_list[i]).get_instructors().strip() + ' '
                url = self.records_dict.get(course_num_list[i]).get_url().strip()
            else:
                description = "instructors:" + course_instructors_list[i] + ' '
                url = 'http://' + course_num_list[i] + '.stanford.edu'
                if self.deep_mind:
                    url = self.getRealUrl(course_num_list[i])

            description += 'description:' + course_description_list[i] + ' '

            self.write_db(f, course_num_list[i], course_name_list[i], url, description)
            self.count += 1

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def doWork(self):
        r = requests.get("https://explorecourses.stanford.edu/browse")
        soup = BeautifulSoup(r.text);
        for li in soup.find_all("li"):
            subject = ""
            if li.a.text.find("(") != -1:
                subject = li.a.text[0: li.a.text.find("(")].strip()
            else:
                subject = li.a.text.strip()
            
            url = "https://explorecourses.stanford.edu/" + str(li.a["href"]).replace("&filter-term-Winter=on", "").replace("search", "print") + "&descriptions=on"
            if self.include_unoffered_courses == True:
                url += "&filter-term-Winter=off&filter-term-Autumn=off&filter-term-Summer=off&filter-term-Spring=off"
            else:
                url += "&filter-term-Autumn=on&filter-term-Summer=on&filter-term-Spring=on&filter-term-Winter=on"
            self.processData(subject, url)

start = StanfordSpider()
start.doWork()
