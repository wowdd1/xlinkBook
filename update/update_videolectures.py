#!/usr/bin/env python

from spider import *

class VideolecturesSpider(Spider):

    def __init__(self):
        Spider.__init__(self)
        self.school = 'videolectures'

    def processData(self, subject):
        r = requests.get('http://videolectures.net/site/ajax/drilldown/?t=evt&cid=13&w=5')
        soup = BeautifulSoup(r.text)
        max_page = 1
        for a in soup.find_all('a'):
            if a.text == ' Last ':
                max_page = int(a['href'][a['href'].find('(') + 1 : a['href'].find(')')])
                break

        file_name = self.get_file_name(subject, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
        urls_list = []

        for page in range(1, max_page + 1):
            r = requests.get('http://videolectures.net/site/ajax/drilldown/?t=evt&p=' + str(page) + '&cid=13&w=5')
            soup = BeautifulSoup(r.text)
            for a in soup.find_all('a'):
                if a.attrs.has_key('lang'):
                    urls_list.append('http://videolectures.net' + a['href'])        
            i = 0
            title = ''
            desc = ''
            for span in soup.find_all('span'):
                i += 1
                if i == 1:
                    print title
                    title = span.text.strip()
                if i == 2:
                    desc = 'description:' + span.text.strip() + ' '
                if i == 3:
                    desc += span.text.strip()
                    self.count += 1
                    self.write_db(f, subject + '-' + str(self.count), title, urls_list[self.count - 1], desc)
                    i = 0

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"
        
    def doWork(self):
        self.processData('eecs-event')


start = VideolecturesSpider()
start.doWork()

