#!/usr/bin/env python


from spider import *

class ProjectsSpider(Spider):
    def __init__(self):
        Spider.__init__(self)
        self.school = "projects"


    def doWork(self):
       self.getDARPAProjects() 
       self.getAIProjects()

    def getAIProjects(self):
        r = requests.get("https://en.wikipedia.org/wiki/List_of_artificial_intelligence_projects")
        soup = BeautifulSoup(r.text)
        start = False
        end = False

        file_name = self.get_file_name("eecs/" + self.school + "/" + "ai", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for li in soup.find_all("li"):
            if li.a != None:
                if li.a.text == "aHuman Project":
                    start = True
                if li.a.text == "Watson":
                    end = True
            if start:
                title = li.text.strip()
                desc = ""
                link = ""
                if li.a != None:
                    link = "https://en.wikipedia.org" + li.a['href']
                if title.find(',') != -1:
                    desc = "description:" + title[title.find(',') + 1 :].strip()
                    title = title[0 : title.find(',')]
                print title
                self.count += 1
                self.write_db(f, "ai-project-" + str(self.count), title, link, desc)

            if end:
                break

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"


    def getDARPAProjects(self):
        r = requests.get("https://en.wikipedia.org/wiki/DARPA")
        soup = BeautifulSoup(r.text)
        start = False
        end = False

        file_name = self.get_file_name(self.school + "/" + "DARPA", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for li in soup.find_all("li"):
            if li.a != None:
                if li.a.text == "4MM":
                    start = True
                if li.a.text == "Project Vela":
                    end = True
            if start:    
                title = li.text.strip()
                desc = ""
                link = ""
                if li.a != None:
                    link = "https://en.wikipedia.org" + li.a['href']
                if title.find(':') != -1:
                    desc = "description:" + title[title.find(':') + 1 :].strip()
                    title = title[0 : title.find(':')]
                print title
                self.count += 1
                self.write_db(f, "darpa-project-" + str(self.count), title, link, desc)
 
            if end:
                break

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"
start = ProjectsSpider()
start.doWork()
