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
        self.getMitMediaLabs()
        self.getSocialRobotLabs()
        self.getBerkeleyEECSLabs()

    def getBerkeleyEECSLabs(self):
        r = requests.get('http://www.eecs.berkeley.edu/Research/Areas/Centers/')
        soup = BeautifulSoup(r.text)
        start = False

        file_name = self.get_file_name(self.school + "/" + "berkeley-eecs-labs", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for li in soup.find_all('li'):
            if li.a != None and li.a['href'].startswith('http'):
                
                title = li.a.text.strip()
                if title.startswith('Algorithms'):
                    start = True
                if start:
                    self.count += 1
                    self.write_db(f, 'berkeley-eecs-lab-' + str(self.count), title, li.a['href'], 'description:' + self.utils.removeDoubleSpace(li.p.text.strip().replace('\n', '')))
                    print title
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def getSocialRobotLabs(self):
        r = requests.get('https://en.wikipedia.org/wiki/Social_robot')
        soup = BeautifulSoup(r.text)

        file_name = self.get_file_name(self.school + "/" + "Social-robot-labs", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for a in soup.find_all('a', class_='external text'):
            print a.text    
            self.count += 1
            self.write_db(f, 'social-robot-lab-' + str(self.count), a.text, a['href'])
            if a.text.startswith('Department'):
                break

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def getMitMediaLabs(self):
        r = requests.get('https://www.media.mit.edu/research/groups-projects')
        soup = BeautifulSoup(r.text)

        file_name = self.get_file_name(self.school + "/" + "MIT-MEDIA-LAB", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
        for span in soup.find_all('span', class_='field-content'):
            if span.a != None and span.a.text.startswith('more') == False:
                title = span.a.text
                link = 'https://www.media.mit.edu' + span.a['href']
                print title
                self.count += 1
                self.write_db(f, 'mit-media-lab-' + str(self.count), title, link)

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

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
