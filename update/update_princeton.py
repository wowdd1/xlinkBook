#!/usr/bin/env python

from spider import *
sys.path.append("..")
from utils import Utils

class PrincetonSpider(Spider):
    termDict = {}
    course_num_list = []

    def __init__(self):
        Spider.__init__(self)
        self.school = "princeton"
        self.deep_mind = True
        self.utils = Utils()

    def isInCourseNumList(self, course_num):
        for item in self.course_num_list:
            if item == course_num:
                return True
        self.course_num_list.append(course_num)
        return False

    def formatInstructors(self, text):
        text = text.strip().replace('\n', ' ')
        while (text.find('  ') != -1):
            text = text.replace('  ', ' ')
        return text

    def getMoreInfo(self, url):
        description = ''
        instructors = 'instructors:'
        link = ''
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        div_timetable = soup.find('div', id='timetable')
        div_dec = soup.find('div', id='descr')
        
        for a in soup.find_all('a'):
            if a.attrs.has_key("href") and a['href'].startswith('/course-offerings/dirinfo.xml'):
                instructors += self.formatInstructors(a.text) + ' '
            if a.text.startswith('http://www'):
                link = a.text
        if link == '':
            link = url
        if div_dec != None:
            description = instructors + 'description:' + div_dec.text.replace('\n', '').strip()
        return link, description

    def processData(self, f, subject_code, subject, term):
        url = "http://registrar.princeton.edu/course-offerings/search_results.xml?term=" + term + "&subject=" + subject_code
        print "processing " + subject_code + " " + subject + " " + url
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        for tr in soup.find_all("tr"):
            i = 0
            course_num = ""
            course_title = ""
            description = ''
            link = ""
            for td in tr.children:
                if str(td).strip() != "":
                    i += 1
                    if i == 2 and td.a.text.find(subject_code) != -1:
                        link = "http://registrar.princeton.edu/course-offerings/" + td.a["href"]
                        course_num = td.a.text.replace("\n", "").strip().replace("  ", "")
                        if course_num.find(" ", course_num.find(subject_code)) != -1:
                            course_num = course_num[course_num.find(subject_code) : course_num.find(" ", course_num.find(subject_code))]
                        else:
                            course_num = course_num[course_num.find(subject_code) : ]
                        if self.deep_mind:
                            link, description = self.getMoreInfo(link)
                    elif i == 3 and course_num != "":
                        if self.isInCourseNumList(course_num) == True:
                            continue

                        course_title = self.utils.removeDoubleSpace(str(td)[str(td).find(">") + 1 : str(td).find("<", + 2)].strip().replace("&amp;", ""))
                        print course_num + " " + course_title
                        self.write_db(f, course_num, course_title, link, description)
                        self.count += 1
                    elif i >= 4:
                        course_num = ""
                        break

    def doWork(self):
        r = requests.get("http://registrar.princeton.edu/course-offerings/")
        soup = BeautifulSoup(r.text)
        
        div = soup.find("div", id="selsubj")
 
        for option in soup.find("select", id="term").children:
            if str(option).strip() == "" or str(option).find("value") == -1:
                continue
            key, value = self.getKeyValue(str(option))
            self.termDict[key] = value
        """
        1164 15-16 Spr
        1162 15-16 Fall
        1154 14-15 Spr
        1152 14-15 Fall
        1144 13-14 Spr
        1142 13-14 Fall
        1134 12-13 Spr
        1132 12-13 Fall
        1124 11-12 Spr
        """
        for line in  div.text.strip().split("\n"):
            if line.strip() != "" and self.need_update_subject(line[line.find(" ") + 1 :].strip()) == True:
                line = line.strip()
                subject_code = line[0 : line.find(" ")]
                subject = line[line.find(" ") + 1 :]
                file_name = self.get_file_name(subject + "-15-16", self.school)
                file_lines = self.countFileLineNum(file_name)
                f = self.open_db(file_name + ".tmp")
                self.count = 0

                self.processData(f, subject_code, subject, "1164")
                self.processData(f, subject_code, subject, "1162")

                self.close_db(f)
                if file_lines != self.count and self.count > 0:
                    self.do_upgrade_db(file_name)
                    print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
                else:
                    self.cancel_upgrade(file_name)
                    print "no need upgrade\n"

start = PrincetonSpider()
start.doWork()
