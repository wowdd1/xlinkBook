#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.20

from spider import *
sys.path.append("..")
from utils import Utils

class ApacheSpider(Spider):

    def __init__(self):
        Spider.__init__(self)
        self.school = "apache"

    def doWork(self):
        url = "https://projects.apache.org/json/foundation/projects.json"
        r = requests.get(url)
        print r.text
        jobj = json.loads(r.text)
        utils = Utils()
        #print jobj
        file_name = self.get_file_name("eecs/apache/" + "apache-projects", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for obj in jobj:
             desc = "description:"
             title = jobj[obj]['name']
             link = jobj[obj]['homepage']
             if jobj[obj].get("description") != None:
                 desc += utils.removeDoubleSpace(jobj[obj]['description'].strip().replace('\n', ''))
             print title
             self.count += 1
             self.write_db(f, "apache-project-" + str(self.count), title[title.find(" ") :].strip(), link, desc)

        self.close_db(f)
        if self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

start = ApacheSpider()
start.doWork()
