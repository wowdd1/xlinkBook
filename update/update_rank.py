#!/usr/bin/env python
# -*- coding: utf-8 -*-
#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07

from spider import *
sys.path.append("..")
from utils import Utils

class BaikeSpider(Spider):

    def __init__(self):
        Spider.__init__(self)
        self.subject = 'rank'
        self.school = "baike"

    def processBaikeData(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        file_name = self.get_file_name(self.subject + "/programmer", self.school)
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
                        self.write_db(f, line[0 : pos_1], line[pos_1 + 1 : pos_3], "", 'description:' + line[pos_3 + 1 :])
                        self.count += 1

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def processWikiTuringData(self, url):

        file_name = self.get_file_name(self.subject + "/Turing-Award", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        for tr in soup.find_all("tr"):
            if tr.th != None and tr.text.strip()[0:1] == "1" or tr.text.strip()[0:1] == "2":
                i = 0
                link = "http://en.wikipedia.org" + str(tr.td.a["href"])
                year = ""
                title = ""
                remark = ""
                for line in tr.text.strip().split("\n"):
                    i += 1
                    #print '---' + str(i) + " " + line
                    if i == 1:
                        year = line
                        continue
                    if len(line) < 50:
                        title += " " + line
                        continue
                    if line.startswith("For") or len(line) > 50:
                        #if i != 3:
                        print year + " " + title + " " + link
                        remark = 'description:' + line
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

        file_name = self.get_file_name(self.subject + "/Computer-Pioneer-Award", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
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


    def processComputerScienceData(self, url):
        r = requests.get(url)
        utils = Utils()
        user_url = ''
        last_line = ''
        last_citations = ''
        remark = 'description:'
        file_name = self.get_file_name(self.subject + "/computer-science-citations", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
        good_line = False 

        for line in r.text.split('\n'):
            good_line = False 
            remark = 'description:'
            if line.strip() == '':
                continue
            if line.find('<') != -1 and line.find('>') != -1:
                line = utils.clearHtmlTag(line).strip()
            else:
                line = line.strip()
            if len(line) < 5 or line.find('<a href') != -1:
                last_line = line
                continue
            if last_line != '':
                if last_line[0 : 1].isdigit():
                    good_line = True
                    line = utils.clearHtmlTag(last_line + ' ' + line)
                last_line = ''
            else:
                if line[0 : 1].isdigit() and line.find('(') > 0:
                    good_line = True
                    line = utils.removeDoubleSpace(line.replace('\n', ''))
            
            if good_line == False:
                continue 
            citations = line[0 : line.find(" ")]
            person = line[line.find(" ") + 1 : line.find("(")]
            place = line[line.find('(') + 1 : line.find(')')]
            info = line[line.find(')') + 2 :].strip()
            #print citations
            title = person + ' (' + place + ')'
            #print info
            remark +=  citations + ' citations, ' + info
            if citations != last_citations:
                self.count += 1
            last_citations = citations
            self.write_db(f, 'csc-' + str(self.count), title, '', remark)

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def processTop100Scientific(self, url):
        file_name = self.get_file_name(self.subject + "/top100-scientific", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        for tr in soup.find_all('tr'):
            if tr.td.text.isnumeric():
                count = 0
                desc = ""
                title = ""
                for line in tr.prettify().split('\n'):
                    count += 1
                    if count == 6:
                        title = line.strip()
                    if count == 9:
                        desc = 'description:' + line.strip()
                print title
                self.count += 1
                self.write_db(f, 'top100-scientific-' + str(self.count), title, '', desc)
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"
        
    def processLeaderOfCountry(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        start = False
        file_name = self.get_file_name(self.subject + "/head-of-country", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
        for tr in soup.find_all('tr'):
            textList = tr.text.split('\n')
            title = ''
            index = 0
            country = ''
            for text in textList:
                if text == '中国':
                    start = True
                if text == '通用名称':
                    title = ''
                    break
                index += 1
                if index == 2:
                    country = text.strip()
                if index == 3 or index == 2:
                    continue
                title += text.strip() + ' '
            if start and title != '':
                print title.strip()
                self.count += 1
                self.write_db(f, "head-of-country-" + str(self.count), country, '', 'description:' + title.strip())
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def processOldTR35(self):
        r = requests.get('http://www2.technologyreview.com/tr35/?year=1999')
        soup = BeautifulSoup(r.text)
        ul = soup.find('ul', class_='years')
        soup = BeautifulSoup(ul.prettify())
        for li in soup.find_all('li'):
            year = li.a.text.strip()
            if year == '2013':
                continue

            file_name = self.get_file_name(self.subject + "/mit-tr35/tr35-" + year + "#", '')
            file_name = file_name[0 : file_name.find('#')]
            file_lines = self.countFileLineNum(file_name)
            f = self.open_db(file_name + ".tmp")
            self.count = 0

            r2 = requests.get('http://www2.technologyreview.com/' + li.a['href'])
            sp = BeautifulSoup(r2.text)
            for div in sp.find_all('div', class_='item'):
                data = div.text.strip().replace('\t', '').split('\n')
                index = 0
                title = ''
                desc = 'description:'
                for d in data:
                    if d == '':
                        continue
                    index += 1
                    if index == 1:
                        title = d
                    else:
                        desc += d + ' '
                print title 
                print desc
                self.count += 1
                self.write_db(f, 'tr35-' + year + '-' + str(self.count), title, 'http://www2.technologyreview.com/' + div.a['href'], desc)
            self.close_db(f)
            if file_lines != self.count and self.count > 0:
                self.do_upgrade_db(file_name)
                print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
            else:
                self.cancel_upgrade(file_name)
                print "no need upgrade\n"

    def processTR35(self):
        utils = Utils()
        for i in range(0, 3):
            year = str(2013 + i)
            r = requests.get('http://www.technologyreview.com/lists/innovators-under-35/' + year)
            soup = BeautifulSoup(r.text)
            ul = soup.find('ul', class_='people')
            soup = BeautifulSoup(ul.prettify())

            file_name = self.get_file_name(self.subject + "/mit-tr35/tr35-" + year + "#", '')
            file_name = file_name[0 : file_name.find('#')]
            file_lines = self.countFileLineNum(file_name)
            f = self.open_db(file_name + ".tmp")
            self.count = 0

            for li in soup.find_all('li'):
                data = utils.removeDoubleSpace(li.text.strip().replace('\t', '').replace('\n', ''))
                title = data[0 : data.find(',')].strip()
                desc = 'description:' + data[data.find(',') + 1 :].strip() 
                print title
                print desc
                self.count += 1
                self.write_db(f, 'tr35-' + year + '-' + str(self.count), title, 'http://www.technologyreview.com/' + li.a['href'], desc)
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
        self.processComputerScienceData('http://web.cs.ucla.edu/~palsberg/h-number.html')
        self.processTop100Scientific('http://www.adherents.com/people/100_scientists.html#')
        self.processLeaderOfCountry('https://zh.wikipedia.org/wiki/%E5%90%84%E5%9B%BD%E9%A2%86%E5%AF%BC%E4%BA%BA%E5%88%97%E8%A1%A8')
        self.processTR35()
        self.processOldTR35()
start = BaikeSpider()
start.doWork()
