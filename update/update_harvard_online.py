#!/usr/bin/env python
    
#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07
    
from spider import *
sys.path.append("..")
from record import CourseRecord
from utils import Utils    

class HarvardOnlineSpider(Spider):

    def __init__(self):
       Spider.__init__(self)
       self. school = "harvard-online"
       self.url = "http://www.extension.harvard.edu/courses"
       self.deep_mind = True
       self.utils = Utils()
    #harvard online
    #"""
    
    
    def getHarvardOnlineLink(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        span = soup.find("span", class_ = "syllabi-bullet-hide")
    
        if span != None and span.a != None:
            if span.a.string.lower().find("Course website".lower()) != -1 :
                return str(span.a["href"])
        return url

    def getMoreInfo(self, url):
        website = url
        description = ''
        instructors = ''
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        span = soup.find("span", class_ = "syllabi-bullet-hide")
   
        if span != None and span.a != None:
            if span.a.string.lower().find("Course website".lower()) != -1 :
                website = str(span.a["href"])

        div = soup.find('div', class_='field field-course-detail field-course-credits')
        if div != None:
            description = "description:" + div.text.replace("\n", '').strip() + ' '

        for a in soup.find_all('a'):
            if a.attrs.get('href', '') != '' and a['href'].startswith('/about-us/faculty-directory'):
                instructors = "instructors:"+ a.text + ' ' + 'http://www.extension.harvard.edu' + a['href'] + ' '
        description = instructors + description
        return website, description
    
    def getHarvardOnlineCourse(self, subject, url, course_dict=None):
        if self.need_update_subject(subject) == False:
            return
        print "processing " + subject + " url " + url
        file_name = self.get_file_name(subject, self.school)
    
        file_lines = self.countFileLineNum(file_name)
        count = 0
        f = self.open_db(file_name + ".tmp")
    
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        course_num = ""
        title = ""
        link = ""
        description = ''
        print "processing html and write data to file..."
        if len(soup.find_all("li", class_ = "views-row")) > 0:
            for li in soup.find_all("li", class_ = "views-row"):
                if li.span != None:
                    course_num = li.span.span.string
                else:
                    course_num = li.prettify().split("\n")[1].strip()
                course_num = course_num.replace(' E-', '').strip()
                title = li.a.string.strip()
                link = "http://www.extension.harvard.edu" + str(li.a["href"]).strip()
                if self.deep_mind:
                    link, description = self.getMoreInfo(link)
                count = count + 1
                print course_num + " " + title + ' ' + link
                self.write_db(f, course_num, title, link, description)
                if course_dict != None:
                    if course_num.startswith('CSCI'):
                        course_num = course_num.replace('CSCI', 'CS')
                    course_dict[course_num] = CourseRecord(self.get_storage_format(course_num, title, link, description))
        else:
            for li in soup.find_all("li"):
                if li.attrs.has_key("class"):
                    if li.prettify().find("E-") != -1 and str(li.a["href"]).startswith("/courses"):
                        for item in li.prettify().split("\n"):
                            if item.find("E-") != -1:
                                course_num = item.replace(' E-', '').strip()
                        count = count + 1
                        title = li.a.string.strip()
                        link = "http://www.extension.harvard.edu" + str(li.a["href"]).strip()
                        if self.deep_mind:
                            link, description = self.getMoreInfo(link)
                        print course_num + " " + title + ' ' + link 
                        self. write_db(f, course_num, title, link, description)
                        if course_dict != None:
                            if course_num.startswith('E-'):
                                course_num = course_num.replace('CSCI', 'CS')
                            course_dict[course_num] = CourseRecord(self.get_storage_format(course_num, title, link, description))
        self.close_db(f)
        if file_lines != count and count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def getCourseDict(self, subject):
        course_dict = {}
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text)

        for li in soup.find_all("li", class_ = "is-more-items"):
            if li.a.string.lower() == subject.lower():
                self.getHarvardOnlineCourse(li.a.string, "http://www.extension.harvard.edu" + str(li.a["href"]), course_dict)
        return course_dict

    def getHarvardCourse(self, subject, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        code = ''

        file_name = self.get_file_name(subject.lower(), self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for div in soup.find_all('div', class_='view-group'):
            sp = BeautifulSoup(div.prettify())
            for div2 in sp.find_all('div'):
                code = div2.span.text.strip()
                link = 'http://www.extension.harvard.edu' + div2.a['href']
                title = self.utils.removeDoubleSpace(div2.text.replace('\n', '')).replace(' E- ', '-E')
                for t in title[title.find(code.upper()) : ].split(code.upper()):
                    if t != '':
                        title = code.upper() + t
                        course_num = title[0 : title.find(' ')].strip()
                        if title.find('(') != -1:
                            title = title[title.find(' ') : title.find('(')].strip()
                        else:
                            title = title[title.find(' ') :].strip()
                        print course_num + ' ' + title
                        self.count += 1
                        self.write_db(f, course_num, title, link)
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def doWork(self):
        print "downloading harvard online course info"
        #r = requests.get("http://www.extension.harvard.edu/courses/subject/computer-science")
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text)
    
    
        #for li in soup.find_all("li", class_ = "is-more-items"):
        #    self.getHarvardOnlineCourse(li.a.string, "http://www.extension.harvard.edu" + str(li.a["href"]))
        for div in soup.find_all('div', class_='view-content'):
            print div.a.text
            if self.need_update_subject(div.a.text) == False:
                continue
            self.getHarvardCourse(div.a.text, 'http://www.extension.harvard.edu' + div.a['href'])

def main(argv):
    start = HarvardOnlineSpider()
    start.doWork()

if __name__ == '__main__':
    main(sys.argv)
 
