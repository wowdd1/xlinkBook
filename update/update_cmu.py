#!/usr/bin/env python

from spider import *

class CMUSpider(Spider):
    dept_dict = {}
    semester_list = ["S15", "F14", "M14"]

    def __init__(self):
        Spider.__init__(self)
        self.school = "cmu"

    def getDescription(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text);
        div = soup.find("div", id="course-detail-description")
        if div != None:
            return div.text.replace("\n","")
        return ""

    def processData(self, semester, dept):
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

        file_name = self.get_file_name("eecs/cmu/" + self.dept_dict[dept] + "-" + semester, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for tr in soup.find_all("tr"):
            if tr.td != None and tr.td.a != None:
                pos = tr.prettify().find("</td>")
                title = tr.prettify()[tr.prettify().find("<td>", pos) + 4 : tr.prettify().find("</td>", pos + 3)].replace("\n", "").strip()
                while title.find("<") != -1:
                    title = title[0 : title.find("<")].strip()+ title[title.find(">") + 1:].replace("\n", "").strip()
                url = "https://enr-apps.as.cmu.edu" + tr.td.a.prettify()[tr.td.a.prettify().find("/open/SOC/SOCServlet"): tr.td.a.prettify().find("'", tr.td.a.prettify().find("/open/SOC/SOCServlet"))].replace("amp;","")
                course_num = tr.td.a.text 
                print course_num + " " + title
                self.count += 1
                self.write_db(f, dept + "-" + course_num, title, url, self.getDescription(url))

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

    def doWork(self):
        self.getDept()
        for dept in self.dept_dict.keys():
            if dept == "CB" or dept == "CS" or dept == "HCI" or dept == "ISR" or dept == "LTI" or dept == "MLG" or dept == "ROB":
                self.processData(self.semester_list[0], dept)


start = CMUSpider();
start.doWork()
