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

    def do_work(self):

        self.processBaikeData("http://www.baike.com/wiki/IT%E4%B8%9A%E6%9C%80%E5%85%B7%E5%BD%B1%E5%93%8D%E5%8A%9B%E7%9A%84284%E4%BD%8D%E7%A8%8B%E5%BA%8F%E5%91%98")



start = BaikeSpider()
start.do_work()
