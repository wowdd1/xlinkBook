#!/usr/bin/env python


from spider import *
sys.path.append("..")
from utils import Utils

class LabsSpider(Spider):
    def __init__(self):
        Spider.__init__(self)
        self.school = "labs"
        self.utils = Utils()

    def doWork(self):
       self.getCSAILLabs()
    def getCSAILLabs(self):
        file_name = self.get_file_name(self.school + "/" + "CSAIL", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        r = requests.get('http://www.csail.mit.edu/research/activities/activities.php')
        soup = BeautifulSoup(r.text)
        div = soup.find('div', class_='node')
        soup = BeautifulSoup(div.prettify())
        for a in soup.find_all('a'):
            if a.attrs.has_key("href") and a['href'].startswith('http'):
                title = a.text.strip()
                print title
                self.count += 1
                self.write_db(f, 'csail-lab-' + str(self.count), title, a['href'])

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

start = LabsSpider()
start.doWork()
