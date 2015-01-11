#!/usr/bin/env python

from spider import *

class PrincetonSpider(Spider):
    termDict = {}
    course_num_list = []

    def __init__(self):
        Spider.__init__(self)
        self.school = "princeton"

    def isInCourseNumList(self, course_num):
        for item in self.course_num_list:
            if item == course_num:
                return True
        self.course_num_list.append(course_num)
        return False

    def processData(self, f, subject_code, subject, term):
        url = "http://registrar.princeton.edu/course-offerings/search_results.xml?term=" + term + "&subject=" + subject_code
        print "processing " + subject_code + " " + subject + " " + url
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        for tr in soup.find_all("tr"):
            i = 0
            course_num = ""
            course_title = ""
            link = ""
            for td in tr.children:
                if str(td).strip() != "":
                    i += 1
                    if i == 2 and td.a.text.find(subject_code) != -1:
                        link = "http://registrar.princeton.edu/course-offerings/" + td.a["href"]
                        course_num = td.a.text.replace("\n", "").strip().replace("  ", "").replace(" ", "/")
                    elif i == 3 and course_num != "":
                        if self.isInCourseNumList(course_num) == True:
                            continue

                        course_title = str(td)[str(td).find(">") + 1 : str(td).find("<", + 2)].strip()
                        print course_num + " " + course_title
                        self.write_db(f, course_num, course_title, link)
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
                file_name = self.get_file_name(subject + "-14-15", self.school)
                file_lines = self.countFileLineNum(file_name)
                f = self.open_db(file_name + ".tmp")
                self.count = 0

                self.processData(f, subject_code, subject, "1154")
                self.processData(f, subject_code, subject, "1152")

                self.close_db(f)
                if file_lines != self.count and self.count > 0:
                    self.do_upgrade_db(file_name)
                    print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
                else:
                    self.cancel_upgrade(file_name)
                    print "no need upgrade\n"

start = PrincetonSpider()
start.doWork()
