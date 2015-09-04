#!/usr/bin/env python


from spider import *
sys.path.append("..")
from utils import Utils

class ProjectPaperSpider(Spider):
    def __init__(self):
        Spider.__init__(self)
        self.utils = Utils()
        self.school = "project-papers"

    def doWork(self):
        self.getWastonPapers()
        #self.getRoboBrainPapers()
        self.getSTAIRPapers()
        self.getSTARTPapers()
    def getSTARTPapers(self):
        r = requests.get("http://start.mit.edu/publications.php")
        soup = BeautifulSoup(r.text)

        file_name = self.get_file_name("eecs/" + self.school + "/" + "START", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
       
        link = ""
        title = ""
        journal = ""
        author = ""
        for td in soup.find_all("td"):
            if td.a != None and td.strong == None and td.a["href"] != "index.php":
                print ""
                if td.a["href"].find("http") == -1:
                    link = "http://start.mit.edu/" + td.a["href"]
                else:
                    link = td.a["href"]
                print link
            else:
                if td.strong != None:
                    if td.em != None:
                        journal = "journal:" + td.em.text + " "
                        print journal
                    if td.strong != None:
                        title = td.strong.text
                        print title
                else:
                    if td.em != None:
                        title = td.em.text
                        print title
                if td.text.find(".") != -1:
                    author = "author:" + td.text[0 : td.text.find(".")] + " "
                    print author
                    print ""
                    self.count += 1
                    self.write_db(f, "start-paper-" + str(self.count), title, link, author + journal)
                    title = ""
                    link = ""
                    author = ""
                    journal = ""

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def getSTAIRPapers(self):
        r = requests.get("http://stair.stanford.edu/papers.php")
        soup = BeautifulSoup(r.text)

        file_name = self.get_file_name("eecs/" + self.school + "/" + "STAIRP", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for li in soup.find_all("li"):
            title = ""
            link = ""
            if li.span == None:
                continue
            title = li.span.text
                
            if li.a != None:
                link = li.a['href']
            self.count += 1
            self.write_db(f, "STAIRP-paper-" + str(self.count), title, link)

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def getRoboBrainPapers(self):
        r = requests.get("http://robobrain.me/#/about")
        soup = BeautifulSoup(r.text)
        file_name = self.get_file_name("eecs/" + self.school + "/" + "robotbrain", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        print r.text
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"


    def getWastonPapers(self):
        r = requests.get('http://researcher.watson.ibm.com/researcher/view_group_pubs.php?grp=2099')
        soup = BeautifulSoup(r.text)
        file_name = self.get_file_name("eecs/" + self.school + "/" + "waston", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for div in soup.find_all("div", class_="publication"):
            link = ""
            authors = ""
            journal = ""
            title = div.h4.text.strip()
            if div.h4.a != None:
                link = div.h4.a['href']
            sp = BeautifulSoup(div.prettify())
            count = 0
            for span in sp.find_all("span", class_="pubspan"):
                count += 1
                data = self.utils.removeDoubleSpace(span.text.strip().replace("\n", ""))
                if count == 1:
                    authors = "author:" + data + " "
                if count == 2:
                    journal = "journal:" + data
            print title
            print authors
            print journal
            print link
            self.count += 1
            self.write_db(f, "waston-paper-" + str(self.count), title, link, authors + journal)

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

start = ProjectPaperSpider()
start.doWork()
