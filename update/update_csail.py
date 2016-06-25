#!/usr/bin/env python


from spider import *
sys.path.append("..")
from utils import Utils

class CSAILSpider(Spider):

    def __init__(self):
        Spider.__init__(self)
        self.school = 'csail'
        self.utils = Utils()


    def doWork(self):
        r = requests.get('http://courses.csail.mit.edu/')
        soup = BeautifulSoup(r.text)

        file_name = self.get_file_name("eecs/ai", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for li in soup.find_all('li'):
            title = self.utils.removeDoubleSpace(li.a.text.strip())
            title = title.replace('\t', '')
            course_num = ''

            self.count += 1
            if title.find('.') != -1:
                course_num = title[0 : title.find(' ')]
                title = title[title.find(' ') + 1 :]
            else:
                course_num += self.school + '-' + str(self.count)   
                print title
            self.write_db(f, course_num, title, 'http://courses.csail.mit.edu/' + li.a['href'])
             

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

start = CSAILSpider()
start.doWork()
