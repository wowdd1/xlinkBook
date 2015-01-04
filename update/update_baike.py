#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07

from spider import *

class BaikeSpider(Spider):

    def __init__(self):
        Spider.__init__(self)
        self.school = "bake"


    def processBaikeData(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text);
        file_name = self.get_file_name("eecs/programmer", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
        p_all = soup.find_all("p")

        for p in p_all:
            if p.prettify()[0:60].find("Peter Norvig") != -1:
                for line in p.prettify().replace('<br>', '').replace('</br>', '').replace('<br/>', '').replace('<p>', '').replace('</p>', '').split("\n"):
                    line = line.strip()
                    if line != "" and line != "# Name Description":
                        pos_1 = line.find(" ")
                        pos_2 = line.find(" ", pos_1 + 1)
                        pos_3 = line.find(" ", pos_2 + 1)
                        print line[0 : pos_1] + " " + line[pos_1 + 1 : pos_3] + " " + line[pos_3 + 1 :]
                        self.write_db(f, line[0 : pos_1], line[pos_1 + 1 : pos_3], "", line[pos_3 + 1 :])
                        self.count += 1

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def processWikiTuringData(self, url):

        file_name = self.get_file_name("eecs/Turing-Award", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
        r = requests.get(url)
        soup = BeautifulSoup(r.text);
        for tr in soup.find_all("tr"):
            if tr.th != None and tr.text.strip()[0:1] == "1" or tr.text.strip()[0:1] == "2":
                i = 0
                link = "http://en.wikipedia.org" + str(tr.td.a["href"])
                year = ""
                title = ""
                remark = ""
                for line in tr.text.strip().split("\n"):
                    i += 1
                    if i == 1:
                        year = line
                        continue
                    if i == 2 or len(line) < 50:
                        title += " " + line
                        continue
                    if i == 3:
                        print year + " " + title + " " + link
                        remark = line
                        self.count += 1
                        self.write_db(f, year, title.strip(), link, remark)
                        i = 0
                        continue

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def processWikiPioneerData(self, url):

        file_name = self.get_file_name("eecs/Computer-Pioneer-Award", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
        r = requests.get(url)
        soup = BeautifulSoup(r.text);
        title = ""
        for tr in soup.find_all("tr"):
            #print tr.text.strip()         
            if tr.text.strip()[0:1] == "1" or tr.text.strip()[0:1] == "2":
                title = title.strip()
                if len(title) > 0 and title[0:1] == "1" or title[0:1] == "2":
                    self.write_db(f, title[0: title.find(" ")], title[title.find(" ") + 1 :], "")
                    print title
                    self.count += 1
                title = ""
                for line in tr.text.strip().split("\n"):
                    title += " " + line.strip()

            else:
                title += " " + tr.text.replace("\n", " ").strip()

        title = title.strip()
        if len(title) > 0 and title[0:1] == "1" or title[0:1] == "2":
            self.write_db(f, title[0: title.find(" ")], title[title.find(" ") + 1 :], "")
            print title
            self.count += 1
                
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def doWork(self):
        self.processWikiTuringData("http://en.wikipedia.org/wiki/Turing_Award")
        self.processWikiPioneerData("http://en.wikipedia.org/wiki/Computer_Pioneer_Award")

        self.processBaikeData("http://www.baike.com/wiki/IT%E4%B8%9A%E6%9C%80%E5%85%B7%E5%BD%B1%E5%93%8D%E5%8A%9B%E7%9A%84284%E4%BD%8D%E7%A8%8B%E5%BA%8F%E5%91%98")



start = BaikeSpider()
start.doWork()
