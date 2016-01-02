#! /usr/bin/env python

from spider import *
sys.path.append("..")
from utils import Utils

class EthzSpider(Spider):
    def __init__(self):
        Spider.__init__(self)
        self.school = "ethz"
        self.semkezDict = {}
        self.deptDict = {}
        self.utils = Utils()

    def processData(self, semkez, deptId, subject):
        print "processing " + semkez + " " + deptId + " " + subject

        r = requests.get('http://www.vvz.ethz.ch/Vorlesungsverzeichnis/sucheLehrangebot.do?wahlinfo=&seite=0&katalogdaten=&lerneinheitstitel=&studiengangTyp=&strukturAus=on&rufname=&bereichAbschnittId=0&lang=en&ansicht=3&lehrsprache=&studiengangAbschnittId=0&semkez=' + semkez + '&famname=&deptId=' + deptId + '&unterbereichAbschnittId=0&lerneinheitscode=')
        soup = BeautifulSoup(r.text)

        file_name = self.get_file_name(subject.lower(), self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0


        for a in soup.find_all('a'):
            if a.attrs.has_key('href') and a['href'].find('lerneinheitPre.do') != -1:
                title = self.utils.removeDoubleSpace(a.text.strip().replace('\n','').replace('\t', ''))
                if len(title) > 2:
                    print title
                    self.count += 1
                    self.write_db(f, self.school + "-" + str(deptId) + "-" + str(self.count), title, 'http://www.vvz.ethz.ch' + a['href'])

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"


    def doWork(self):
        r = requests.get('http://www.vvz.ethz.ch/Vorlesungsverzeichnis/sucheLehrangebotPre.do?lang=en')
        soup = BeautifulSoup(r.text)
        for select in soup.find_all('select', class_='w50'):
            if select['name'] == "semkez":
                soup1 = BeautifulSoup(select.prettify())
                for option in soup1.find_all('option'):
                    if option.text.strip() != '':
                        self.semkezDict[option['value']] = option.text.strip()
       
            if select['name'] == "deptId":
                soup1 = BeautifulSoup(select.prettify())
                for option in soup1.find_all('option'):
                    if option.text.strip() != '':
                        self.deptDict[option['value']] = option.text.strip()

        for k, v in [(k,self.deptDict[k]) for k in self.deptDict.keys()]:
            if self.need_update_subject(v) == False:
                continue
            year = time.strftime("%Y") 
            for semkez in self.semkezDict.keys():
                if semkez[0 : 4] == year:
                    self.processData(semkez, k, v)

start = EthzSpider()
start.doWork()


