#!/usr/bin/env python
    
#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07
    
from spider import *
from update_stanford import StanfordSpider
from update_stanford_online import StanfordOnlineSpider
sys.path.append("..")
from record import CourseRecord

class StanfordCSSpider(Spider):
    course_num_list = []

    def __init__(self):
        Spider.__init__(self)
        self.school = "stanford"
        self.subject = "eecs"
        stanfordSpider = StanfordSpider()
        stanfordOnlineSpider = StanfordOnlineSpider()

        self.description_dict = stanfordSpider.getDescriptionDict('Computer Science')
        self.course_name_dict = stanfordOnlineSpider.getCourseNameDict()
    
    def isInCourseNumList(self, course_num):
        for item in self.course_num_list:
            if item == course_num:
                return True
        self.course_num_list.append(course_num)
        return False
   
    def formatCourseTitle(self, title):
        if title.find('(') != -1:
            title = title[0 : title.find('(')]
        return title.strip()
 
    def processStanfordDate(self, f, url, course_dict):
        print 'processing ' + url
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        th_set = soup.find_all("th")
        td_set_all = soup.find_all("td")
        td_set = []
        td_set_2 = []
        del th_set[0:5]
        i = 0
        for td in td_set_all:
            i = i + 1
            if i == 1:
                td_set.append(td.string)
            if i == 2:
                td_set_2.append(td.string)
            if i == 4:
                i = 0
    
        for index in range(0,len(th_set)):
            link = th_set[index].prettify()
            link = link[link.find("http"):link.find("EDU") + 3]
            if self.isInCourseNumList(th_set[index].string):
                continue
            course_id = th_set[index].string.upper()
            description = ''
            description += 'instructors:' + td_set_2[index] + ' '
            if self.course_name_dict.get(self.formatCourseTitle(td_set[index]), '') != '':
                if self.course_name_dict.get(self.formatCourseTitle(td_set[index]), '') != '':
                    description += 'videourl:' + self.course_name_dict[self.formatCourseTitle(td_set[index])] + ' '

            if self.description_dict.get(course_id, '') != '':
                description += 'description:' + self.description_dict[course_id] + ' '
            course_dict[th_set[index].string.upper()] = CourseRecord(self.get_storage_format(th_set[index].string.upper(), td_set[index], link, description))

   
    def getCsCourseLinks(self):
        links = []
        r = requests.get('http://cs.stanford.edu/academics/courses')
        soup = BeautifulSoup(r.text)
        for a in soup.find_all('a'):
            if a.attrs.has_key('href') and a['href'].find('http://cs.stanford.edu/courses/schedules/') != -1:
                links.append(a['href'])

        return links

    def doWork(self):
        #stanford
        #"""
        print "downloading stanford course info"

        file_name = self.get_file_name("eecs/" + "cs", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
 
        print "processing html and write data to file..."
        course_dict = {}
        for url in self.getCsCourseLinks():
            self.processStanfordDate(f, url, course_dict)

        for k, record in [(k,course_dict[k]) for k in sorted(course_dict.keys())]:
            self.count += 1
            self.write_db(f, k, record.get_title().strip(), record.get_url().strip(), record.get_describe().strip()) 
    
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"
        #"""
    
def main(argv):
    start = StanfordCSSpider()
    start.doWork()

if __name__ == '__main__':
    main(sys.argv)

