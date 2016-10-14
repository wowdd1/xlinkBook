#!/usr/bin/env python

from spider import *
sys.path.append("..")
from utils import Utils

class BpCsSpider(Spider):

    def doWork(self):
        utils = Utils()
        r = requests.get('http://jeffhuang.com/best_paper_awards.html')
        soup = BeautifulSoup(r.text)
        file_name = self.get_file_name("eecs/papers/best-cs-paper", "")
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for table in soup.find_all('table'):
            sp = BeautifulSoup(table.prettify())
            #for thead in sp.find_all('thead'):
            #    print thead.text.strip()
            
            year = ''
            line = ''
            conf = ''
            for td in sp.find_all('td'):
                if (td.text.strip() == 'Microsoft Research'):
                    break
                if td.a != None and td.a.attrs.has_key('name') and False == td.a.attrs.has_key('href'):
                    conference = td.a.text.strip()
                    conference = conference[0 : conference.find('(')].strip().lower()
                    continue
                #utils.removeDoubleSpace(tbody.text).strip()
                text = utils.removeDoubleSpace(td.text.replace('; et al.', '')).strip()
                if (len(text) == 4):
                    if len(line.strip()) > 4:
                        if conf == '':
                            conf = conference
                        self.writeLines(f, line, conf + '-' + year)
                        conf = conference
                        line = ''
                        line += text + '|'
                    else:
                        line += text + '|'
                    year = text
                else:
                    line += text + '|'
            if len(line.strip()) > 4:
                self.writeLines(f, line, conference + '-' + year)
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def writeLines(self, f, line, number):
        count = 0
        title = ''
        for item in line.split('|'):
            if item == '':
                break
            count += 1
            if count == 1:
                continue
            if count % 2 == 0 and len(item) > 0:
                print number + ' ' + item
                title = item
            else:
                print item
                self.count += 1
		self.write_db(f, number, title, 'http://scholar.google.com/scholar?as_q=&num=10&btnG=Search+Scholar&as_epq=' + title, 'id:' + number + ' author:' + item)
start = BpCsSpider()
start.doWork()
