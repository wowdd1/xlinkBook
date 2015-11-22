#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.20

from spider import *

class SourceforgeSpider(Spider):

    def __init__(self):
        Spider.__init__(self)
        self.school = "sourceforge"

    def processSourceforgeData(self, name, v):
        print "processing " + name
        file_name = self.get_file_name("eecs/projects/sourceforge/" + name, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
        for item in v:
            print str(item["downloads"]) + " " +  item["name"] + " " + "http://sourceforge.net" + item["project_url"]
            self.write_db(f, str(item["rank"]) + "-" + str(item["downloads"]), item["name"], "http://sourceforge.net" + item["project_url"])
            self.count += 1

        self.close_db(f)
        if self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def doWork(self):
        url = "http://sourceforge.net/top/top_data"
        r = requests.get(url)
        jobj = json.loads(r.text)

        for k,v in jobj.items():
            if k != "activity_week":
                self.processSourceforgeData(k,v)

start = SourceforgeSpider()
start.doWork()
