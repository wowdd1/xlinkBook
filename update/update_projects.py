#!/usr/bin/env python


from spider import *
sys.path.append("..")
from utils import Utils

class ProjectsSpider(Spider):
    def __init__(self):
        Spider.__init__(self)
        self.school = "projects"
        self.utils = Utils()

    def doWork(self):
       self.getDARPAProjects() 
       self.getDARPAOpenProjects()
       self.getAIProjects()
       self.getDotNetFoundationProjects()

       self.getMicrosoftResearch()
       self.getAICProjects()
       self.getDARPAWikiProjects()
    def getAICProjects(self):
        r = requests.get('http://www.ai.sri.com/project_list/mode=All&sort=titleAsc')
        soup = BeautifulSoup(r.text)
        pages = 0

        file_name = self.get_file_name("eecs/" + self.school + "/" + "AIC", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for a in soup.find_all('a'):
            if a.text.strip() == 'End':
                pages = int(a['href'][len(a['href']) - 1 : ])

        for page in range(0, pages + 1):
            r2 = requests.get('http://www.ai.sri.com/project_list/mode=All&sort=titleAsc&page=' + str(page))
            soup2 = BeautifulSoup(r2.text)
            for td in soup2.find_all('td', class_='project'):
                if td.h2 != None:
                    title = td.h2.a.text
                    desc = "description:" + self.utils.removeDoubleSpace(td.p.text.replace('\n',''))
                    print title
                    self.count += 1
                    self.write_db(f, 'aic-project-' + str(self.count), title, 'http://www.ai.sri.com' + td.h2.a['href'], desc)
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"


    def getMicrosoftResearch(self):
        file_name = self.get_file_name("eecs/" + self.school + "/" + "microsoft-research", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
        for page in range(1, 13):
            r = requests.get("http://research.microsoft.com/apps/catalog/default.aspx?p=" + str(page) + "&sb=no&ps=100&t=projects&sf=&s=&r=&vr=&ra=")
            soup = BeautifulSoup(r.text)
            for div in soup.find_all('div', class_='l'):
                sp = BeautifulSoup(div.prettify())
                name_div = sp.find('div', class_='name')
                desc_div = sp.find('div', class_='desc')
                title = name_div.a.text.strip()
                desc = "description:" + self.utils.removeDoubleSpace(desc_div.text.strip().replace('\n', ''))
                print title
                self.count += 1
                self.write_db(f, 'ms-research-' + str(self.count), title, 'http://research.microsoft.com' + name_div.a['href'], desc)
               
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"
        
    def getDotNetFoundationProjects(self):
        r = requests.get("http://www.dotnetfoundation.org/projects")
        soup = BeautifulSoup(r.text)

        file_name = self.get_file_name("eecs/" + self.school + "/" + "DotNetFoundation", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for td in soup.find_all("td", class_="project-cell"):
            link = "http://www.dotnetfoundation.org" + td.div.span.a['href']
            title = td.text.strip()
            self.count += 1
            self.write_db(f, 'DotNetFoundation-project-' + str(self.count), title, link, '')

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def getDARPAWikiProjects(self):
        r = requests.get("https://en.wikipedia.org/wiki/DARPA")
        soup = BeautifulSoup(r.text)
        start = False
        end = False

        file_name = self.get_file_name("projects/" + "DARPA-WIKI", self.school)
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
                self.write_db(f, "darpa-wiki-project-" + str(self.count), title, link, desc)

            if end:
                break

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

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


    def getDARPAOpenProjects(self):
        #r = requests.get("https://en.wikipedia.org/wiki/DARPA")
        f = open("index.html", "r")
        html = f.read()
        soup = BeautifulSoup(html)
        file_name = self.get_file_name(self.school + "/" + "DARPA-open", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for tr in soup.find_all('tr'):
            sp = BeautifulSoup(tr.prettify())
            count = 0
            title = ""
            desc = "description:"
            for line in tr.text.split("\n"):
                line = line.strip()
                if line == "":
                    continue
                count += 1
                if count == 1:
                    title = line
                else:
                    desc += line + " "
            if title == "DARPA Program":
                continue
            print title
            self.count += 1
            self.write_db(f, "darpa-open-project-" + str(self.count), title, "", desc)
                

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def getDARPAProjects(self):
        #r = requests.get("https://en.wikipedia.org/wiki/DARPA")
        f = open("2.htm", "r")
        html = f.read()
        soup = BeautifulSoup(html)
        file_name = self.get_file_name(self.school + "/" + "DARPA-history", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for div in soup.find_all('div', class_='listing__right'):
            title = div.div.text + " " + div.h2.a.text
            #desc = "description:" + div.div.text.replace("\n", "")
            print title
            self.count += 1
            self.write_db(f, "darpa-history-project-" + str(self.count), title, div.h2.a['href'], "")

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"
start = ProjectsSpider()
start.doWork()
