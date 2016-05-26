#!/usr/bin/env python


from spider import *
sys.path.append("..")
from utils import Utils


class AlexaSpider(Spider):

    def __init__(self):
        Spider.__init__(self)
        self.school = "alexa"
        self.subject = "top500web"
        self.category = self.category_obj.website        


    def doWork(self):
        u = Utils()

        file_name = self.get_file_name("rank/" + self.subject, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for i in range(0, 20):

            r = requests.get('http://www.alexa.com/topsites/global;' + str(i))
            soup = BeautifulSoup(r.text)

            for li in soup.find_all('li', class_='site-listing'):
                sp = BeautifulSoup(li.prettify())

                div = sp.find('div', class_='description')
                print li.div.text + ' ' + li.a.text + ' ' + 'http://www.alexa.com' + li.a['href'] +" "+  u.removeDoubleSpace(div.text).strip()
                self.count += 1
                self.write_db(f, 'alexa-' + li.div.text, li.a.text, 'http://' + li.a['href'][li.a['href'].find('/', 1) + 1 : ], "description:" + u.removeDoubleSpace(div.text).strip())



        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"


start = AlexaSpider()
start.doWork()
