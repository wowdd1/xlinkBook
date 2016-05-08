#!/usr/bin/env python

from spider import *

class DuckduckgoSpider(Spider):
    include_unoffered_courses = False

    def __init__(self):
        Spider.__init__(self)
        self.school = "duckduckgo"
        self.subject = "engin_list"


    def doWork(self):
        r = self.requestWithProxy2('https://duckduckgo.com/bang_lite.html')
        soup = BeautifulSoup(r.text)

        file_name = self.get_file_name('config/' + self.subject, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
        engin_dict = {}
        engin_name_dict = {}
        for ul in soup.find_all('ul'):
            soup2 = BeautifulSoup(ul.prettify())
            for li in soup2.find_all('li'):
                if li.h6 != None:
                    data = li.h6.text.strip()
                    engin_type = data.replace(' (', '(')
                    engin_type = engin_type[0 : len(engin_type) - 1].strip()
                    print '#' + engin_type.lower()
                    data = li.text[li.text.find(':') + 1 : ].strip().split('\n')
                    engin_dict[engin_type] = data
        span = soup.find('span', class_='small')
        if span != None:
            data = span.text[span.text.find(':') + 1 : ].strip().split('\n') 
            for d in data:
                #print d[0 : d.find('(')]
                command = d[d.find('!') : ]
                command = command[0 : len(command) - 1]
                #print command
                engin_name_dict[command] = d[0 : d.find('(')].strip()

        for k, v in engin_dict.items():
            for t in v:
                if t.find('(') != -1:
                    t = t[0: t.find('(')].strip()
                        
                title = t.strip()
                if engin_name_dict.has_key(title) and engin_name_dict[title] != None:
                    title = engin_name_dict[title]
                else:
                    print title
                self.count += 1
                self.write_db(f, 'ddg-' + k.lower() + '-' + str(self.count), title.replace("'", ' '), t, 'priority:0 description:' + k.lower())

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"


start = DuckduckgoSpider()
start.doWork()
