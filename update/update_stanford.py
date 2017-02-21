#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2015.01.03

from spider import *
from update_stanford_online import StanfordOnlineSpider
sys.path.append("..")
from record import CourseRecord
import time

class StanfordSpider(Spider):
    include_unoffered_courses = False
 
    def __init__(self):
        Spider.__init__(self)
        self.school = "stanford"
        self.subject = "eecs"
        self.deep_mind = True
        self.course_dict = {}
        stanfordOnlineSpider = StanfordOnlineSpider()
        self.course_name_dict = stanfordOnlineSpider.getCourseNameDict()

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

    def getDescriptionDict(self, subject):
        results = {}
        for line in open(self.get_file_name(subject, self.school),'rU').readlines():
            record = CourseRecord(line)
            results[record.get_id().strip()] = record.get_description().strip()
        return results

    def formatCourseTitle(self, title):
        if title.find('(') != -1:
            title = title[0 : title.find('(')]
        if title.find(':') != -1:
            title = title[0 : title.find(':')]
        return title.strip()

    def isCourseProcessed(self, course_num):
        if self.course_dict.get(course_num, '') != '':
            return True
        else:
            self.course_dict[course_num] = 'record'
            return False

    def processData(self, f, subject, url):
        print "processing " + subject + " " + url

        from update_stanford_cs import StanfordCSSpider
        r = requests.get(url)
        soup = BeautifulSoup(r.text) 
        course_num_list = []
        course_name_list = []
        course_description_list = []
        course_instructors_list = []

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
        if len(course_num_list) - len(course_instructors_list) == 1:
            course_instructors_list.append('')
        for i in range(0, len(course_num_list)):
            if self.isCourseProcessed(course_num_list[i]):
                continue

            print course_num_list[i] + " " + course_name_list[i]
            description = "instructors:" + course_instructors_list[i] + ' '
            url = 'http://' + course_num_list[i] + '.stanford.edu'
            if self.deep_mind:
                url = self.getRealUrl(course_num_list[i])
            if self.course_name_dict.get(self.formatCourseTitle(course_name_list[i]), '') != '':
                description +='videourl:' + self.course_name_dict[self.formatCourseTitle(course_name_list[i])] + ' ' 

            description += 'description:' + course_description_list[i] + ' '

            self.course_dict[course_num_list[i]] = CourseRecord(self.get_storage_format(course_num_list[i], course_name_list[i], url, description))


    def doWork(self):
        r = requests.get("https://explorecourses.stanford.edu/browse")
        soup = BeautifulSoup(r.text)
        year = int(time.strftime('%Y',time.localtime(time.time())))
        td = soup.find('td', attrs={"class": "selected"})
        #year_args = ['&academicYear=' + str(year -2) + str(year -1), '&academicYear=' + str(year -1) + str(year)]
        #year_args = ['&academicYear=' + str(year -1) + str(year)]
        year_args = ['&academicYear=' + td.text.replace("-", "").strip()]
        for li in soup.find_all("li"):
            subject = ""
            if li.a.text.find("(") != -1:
                subject = li.a.text[0: li.a.text.find("(")].strip()
            else:
                subject = li.a.text.strip()
            if self.need_update_subject(subject) == False:
                continue

            url = "https://explorecourses.stanford.edu/" + str(li.a["href"]).replace("&filter-term-Winter=on", "").replace('&academicYear=', '').replace("search", "print") + "&descriptions=on"
            if self.include_unoffered_courses == True:
                url += "&filter-term-Winter=off&filter-term-Autumn=off&filter-term-Summer=off&filter-term-Spring=off"
            else:
                url += "&filter-term-Autumn=on&filter-term-Summer=on&filter-term-Spring=on&filter-term-Winter=on"
            
            self.course_dict = {}
            file_name = self.get_file_name(subject, self.school)
            file_lines = self.countFileLineNum(file_name)
            f = self.open_db(file_name + ".tmp")
            self.count = 0

            for year_arg in year_args:
                self.processData(f, subject, url + year_arg)

            for k, record in [(k,self.course_dict[k]) for k in sorted(self.course_dict.keys())]:
                title = record.get_title().strip()
                if title.find('(') != -1:
                    title = title[0 : title.find('(')].strip()
                self.write_db(f, k, title, record.get_url().strip(), record.get_describe().strip())
                self.count += 1 

            self.close_db(f)
            if file_lines != self.count and self.count > 0:
                self.do_upgrade_db(file_name)
                print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
            else:
                self.cancel_upgrade(file_name)
                print "no need upgrade\n"

def main(argv):
    start = StanfordSpider()
    start.doWork()

if __name__ == '__main__':
    main(sys.argv)
