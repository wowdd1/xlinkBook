#! /usr/bin/env python


from spider import *

class ThinkTankSpider(Spider):
    
    def __init__(self):
        Spider.__init__(self)
        self.school = 'thinktank'

    def doWork(self):
        self.getUSAThinkTank('https://en.wikipedia.org/wiki/List_of_think_tanks_in_the_United_States')
        self.getThinkTankBaseInUSA('https://en.wikipedia.org/wiki/Category:Think_tanks_based_in_the_United_States')
        self.getThinkTank('https://en.wikipedia.org/wiki/List_of_think_tanks')

    def getUSAThinkTank(self, url):
        self.parseHtml(url, 'thinktank-usa', 'Acton Institute', 'World Resources Institute')

    def getThinkTankBaseInUSA(self, url):
        self.parseHtml(url, 'thinktank-basein-usa', 'The American Assembly', 'Yankee Institute for Public Policy')

    def getThinkTank(self, url):
        self.parseHtml(url, 'thinktank', 'United Nations University', 'International Growth Centre')

    def parseHtml(self, url, id, startTag, endTag):
        print url
        start = False
        end = False
        r = requests.get(url)
        soup = BeautifulSoup(r.text)

        file_name = self.get_file_name("thinktank/" + id, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
        
        for a in soup.find_all('a'):
             
            title = a.text.strip()
            if (title.startswith(startTag)):
                start = True
            if start:
                if title == "edit":
                    continue
                print title
                url = "https://en.wikipedia.org" + a['href']
                self.count += 1
                self.write_db(f, id + "-" + str(self.count), title, url)
            if title.startswith(endTag):
                end = True
            if end:
                break

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

start = ThinkTankSpider()
start.doWork()
    
