#!/usr/bin/env python

from spider import *
sys.path.append("..")
from utils import Utils

class BrownCSSpider(Spider):
 
    def __init__(self):
        Spider.__init__(self)    
        self.school = "brown"
        self.utils = Utils()

    def doWork(self):
        r = requests.get('https://cs.brown.edu/courses/')
        soup = BeautifulSoup(r.text)
        start = False

        file_name = self.get_file_name("eecs/computer-science", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for tr in soup.find_all('tr'):
            data = tr.text.strip().replace('/n', '')
            if tr.a != None:

                rID = tr.a.text
                if rID.startswith('CSCI'):
                    start = True
                if start == False:
                    continue
                rTitle = data.replace(rID, '')
                if rTitle.find(')') != -1:
                    rTitle = rTitle[rTitle.find(')') + 1 :]
                elif rTitle.find('-') != -1:
                    rTitle = rTitle[rTitle.find('-') + 2 :]
                rID = rID.replace(' ', '-')

                #url = tr.a['href']
                #url = 'http://cs.brown.edu/courses/' + url[url.rfind('/') + 1 : url.rfind('.')]

                #if self.utils.websiteNotWorking(url, 5):
                url = 'https://cs.brown.edu' + tr.a['href']

                print rID + ' ' + rTitle
                self.count += 1
                self.write_db(f, rID, rTitle, url, '')

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

start = BrownCSSpider()
start.doWork()