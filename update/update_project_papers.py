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
