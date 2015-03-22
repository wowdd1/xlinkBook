#!/usr/bin/env python


from spider import *

class CambridgeSpider(Spider):


    def __init__(self):
        Spider.__init__(self)
        self.school = 'cambridge'

    def doWork(self):
        r = requests.get('http://www.cl.cam.ac.uk/teaching/1415/lecturers.html')
        soup = BeautifulSoup(r.text)

        file_name = self.get_file_name('eecs', self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for li in soup.find_all('li'):
            if li.a['href'][-1] == '/' and li.a['href'][0 : 1] != '.':
                print li.a.text
                self.count += 1
                self.write_db(f, self.school + '-' + str(self.count), li.a.text, 'http://www.cl.cam.ac.uk/teaching/1415/' + li.a['href'])
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"


start = CambridgeSpider()
start.doWork()
