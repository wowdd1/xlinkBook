#!/usr/bin/env python


from spider import *
sys.path.append("..")
from utils import Utils

class LabPapersSpider(Spider):

    def __init__(self):
        Spider.__init__(self)
        self.utils = Utils()

    def doWork(self):
        self.getGoogleLabPapers()
        #self.getYahooLabPapers()

    def getYahooLabPapers(self):
        for page in range(0, 125):
            url = "https://labs.yahoo.com/publications?field_publications_research_area_tid=All&field_publications_date_value[value]=&page=" + str(page)
            r = requests.get(url)
            print url
            soup = BeautifulSoup(r.text)
            for div in soup.find_all('div', class_='f-c07v0'):
                print div.div.h3.a.text
                soup2 = BeautifulSoup(div.prettify())
                main = soup2.find('div', class_='f-c07_main')
                aside = soup2.find('div', class_='f-c07_aside')
                print main.text.strip()
                print aside.text.strip()

    def getGoogleLabPapers(self):

        r = requests.get("http://research.google.com/pubs/papers.html")
        soup = BeautifulSoup(r.text)
        for li in soup.find_all('li', class_="research-area"):
            subject = self.utils.removeDoubleSpace(li.a.span.text.strip()).replace(' ','-').lower()
            print subject
            r2 = requests.get('http://research.google.com' + li.a['href']) 
            soup2 = BeautifulSoup(r2.text)

            file_name = self.get_file_name("eecs/papers" + "/" + subject, 'google-research')
            file_lines = self.countFileLineNum(file_name)
            f = self.open_db(file_name + ".tmp")
            self.count = 0
            for li in soup2.find_all('li'):
                if li.p == None or li.a['href'].startswith('http://www.google.com') == False:
                    continue
                count = 0
                soup3 = BeautifulSoup(li.prettify())
                title = ''
                author = 'author:'
                journal = 'journal:'
                for p in soup3.find_all('p'):
                    count += 1
                    data = self.utils.removeDoubleSpace(p.text.strip().replace('\n',''))
                    if count == 1:
                        title = data
                    if count == 2:
                        author += data
                    if count == 3:
                        journal += data
                print title
                self.count += 1
                self.write_db(f, 'google-' + subject + '-' + str(self.count), title, li.a['href'], author + ' ' + journal)
            self.close_db(f)
            if file_lines != self.count and self.count > 0:
                self.do_upgrade_db(file_name)
                print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
            else:
                self.cancel_upgrade(file_name)
                print "no need upgrade\n"

start = LabPapersSpider()
start.doWork()
