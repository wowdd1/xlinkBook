#!/usr/bin/env python

from spider import *
import time
sys.path.append("..")
from record import CourseRecord

class CMUSpider(Spider):
    dept_dict = {}
    semester_list = []

    def __init__(self):
        Spider.__init__(self)
        self.school = "cmu"
        year = int(time.strftime('%Y',time.localtime(time.time())))
        self.semester_list.append('F' + str(year)[2:])
        self.semester_list.append('S' + str(year)[2:])
        self.semester_list.append('F' + str(year - 1)[2:])

    def getDescription(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text);
        description = ''
        ul = soup.find('ul', class_='list-unstyled instructor')
        if ul != None and ul.li != None:
            instructors = ul.text.replace('\n', '').strip()
            while instructors.find('  ') != -1:
                instructors = instructors.replace('  ', ' ')
            description += 'instructors:' + instructors + ' '
        
        for div in soup.find_all('div', class_='col-md-6'):
            if div != None and div.text.find('None') == -1 and div.text.find('Prerequisites') != -1:
                description += 'prereq:' + div.text.replace("\n","").replace('Prerequisites', '').strip() + ' '
                break

        div = soup.find("div", id="course-detail-description")
        if div != None:
            description += 'description:' + div.text.replace("\n","").replace('Description:', '').strip()
        return description

    def processData(self, semester_list, dept, subject):
        if self.need_update_subject(subject) == False:
            return

        file_name = ''
        if subject == 'eecs':
            file_name = self.get_file_name(subject + "/cmu/" + self.dept_dict[dept], self.school)
        else:
            file_name = self.get_file_name(subject, self.school)

        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
        course_dict = {}

        for semester in semester_list:
            print "processing " + self.dept_dict[dept] + " " + semester + " data"
            param = {"SEMESTER" : semester,
                 "MINI" : "NO",
                 "GRAD_UNDER" : "All",
                 "PRG_LOCATION" : "All",
                 "DEPT" : dept,
                 "LAST_NAME" : "",
                 "FIRST_NAME" : "",
                 "BEG_TIME" : "All",
                 "KEYWORD" : "",
                 "TITLE_ONLY" : "NO",
                 "SUBMIT" : ""}
            r = requests.post("https://enr-apps.as.cmu.edu/open/SOC/SOCServlet/search", params=param)
            soup = BeautifulSoup(r.text); 

            for tr in soup.find_all("tr"):
                if tr.td != None and tr.td.a != None:
                    pos = tr.prettify().find("</td>")
                    title = tr.prettify()[tr.prettify().find("<td>", pos) + 4 : tr.prettify().find("</td>", pos + 3)].replace("\n", "").strip()
                    while title.find("<") != -1:
                        title = title[0 : title.find("<")].strip()+ title[title.find(">") + 1:].replace("\n", "").strip()
                    url = "https://enr-apps.as.cmu.edu" + tr.td.a.prettify()[tr.td.a.prettify().find("/open/SOC/SOCServlet"): tr.td.a.prettify().find("'", tr.td.a.prettify().find("/open/SOC/SOCServlet"))].replace("amp;","")
                    course_num = dept + tr.td.a.text 
                    if course_dict.get(course_num, '') != '':
                        continue
                    print course_num + " " + title
                    course_dict[course_num] = CourseRecord(self.get_storage_format(course_num, title, url, self.getDescription(url)))

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

    def getDept(self):
        r = requests.get("https://enr-apps.as.cmu.edu/open/SOC/SOCServlet/search")
        soup = BeautifulSoup(r.text); 
        for child in soup.find("select", id="dept").children:
            if str(child).strip() == "":
                continue
            key = str(child)[str(child).find('"') + 1 : str(child).find('"', str(child).find('"') + 1)]
            value = str(child)[str(child).find(">") + 1 : str(child).find("(")].replace("&amp;", "").replace("\n", "").strip()
            self.dept_dict[key] = value

    def getSOCData(self):
        self.getDept()
        for dept in self.dept_dict.keys():
            if dept == "CB" or dept == "CS" or dept == "HCI" or dept == "ISR" or dept == "LTI" or dept == "MLG" or dept == "ROB" or dept == 'ECE':
                self.processData(self.semester_list, dept, 'eecs')
            else:
                self.processData(self.semester_list, dept, self.dept_dict[dept])

    def getRoboticsCourse(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        file_name = self.get_file_name("eecs/cmu/robotics-institute", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for li in soup.find_all("li", attrs={"class": "sub_title2"}):
            text = li.text
            course_number = ""
            course_name = ""
            url = ""
            if li.text.find("\n") != -1:
                text = li.text[0 : li.text.find("\n")].strip()
            course_number = text.split(":")[0].strip()
            course_name = text.split(":")[1].strip()
            if li.prettify().find("http") != -1:
                soup2 = BeautifulSoup(li.prettify())
                for a in soup2.find_all("a"):
                    if (a.attrs.has_key("href")):
                        url = a["href"]
                    
            print course_number + " " + course_name + " " + url
            self.count = self.count + 1
            self.write_db(f, course_number, course_name, url)

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def doWork(self):
        self.getSOCData()
        self.getRoboticsCourse("https://www.ri.cmu.edu/ri_static_content.html?menu_id=276#");

start = CMUSpider();
start.doWork()
