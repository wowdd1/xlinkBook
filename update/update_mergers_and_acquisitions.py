#!/usr/bin/env python

from spider import *

sys.path.append("..")
from utils import Utils

class MergersAndAcquisitionsSpider(Spider):
    def __init__(self):
        Spider.__init__(self)
        self.school = 'wiki'


    def doWork(self):
        utils = Utils()
        wiki_dict = {'google' : 'http://en.wikipedia.org/wiki/List_of_mergers_and_acquisitions_by_Google',\
                     'facebook' : 'http://en.wikipedia.org/wiki/List_of_mergers_and_acquisitions_by_Facebook',\
                     'microsoft' : 'http://en.wikipedia.org/wiki/List_of_mergers_and_acquisitions_by_Microsoft',\
                     'apple' : 'http://en.wikipedia.org/wiki/List_of_mergers_and_acquisitions_by_Apple',\
                     'ibm' : 'http://en.wikipedia.org/wiki/List_of_mergers_and_acquisitions_by_IBM',\
                     'yahoo' : 'http://en.wikipedia.org/wiki/List_of_mergers_and_acquisitions_by_Yahoo!',\
                     'twitter' : 'http://en.wikipedia.org/wiki/List_of_mergers_and_acquisitions_by_Twitter'}
        for key, url in wiki_dict.items():
            r = requests.get(url)
            soup = BeautifulSoup(r.text)
            table = soup.find('table', class_='wikitable')
            #print table
            soup = BeautifulSoup(table.prettify())
            count = 0
            desc = ''
            title = ''
            file_name = self.get_file_name('economics/' + key, self.school)
            file_lines = self.countFileLineNum(file_name)
            f = self.open_db(file_name + ".tmp")
            self.count = 0
            item_id = key + '-merger-'

            for td in soup.find_all('td'):
                count += 1

                if key == 'google':
                    if count > 8:
                        print title
                        count = 1
                        self.count += 1
                        self.write_db(f, item_id + str(self.count), title, '', utils.removeDoubleSpace(desc))
                        title = ''
                        desc = ''
                        print '----------------------------------'
                    if count != 1 and count != 8:
                        if count == 2:
                            desc += td.text.strip()[td.text.strip().find(' ') :].strip() + ' '
                        elif count == 3:
                            title = utils.removeDoubleSpace(td.text.strip())
                        else:
                            desc += td.text.strip() + ' '
                if key == 'facebook':
                    if count > 10:
                        count = 1
                        print title
                        self.count += 1
                        self.write_db(f, item_id + str(self.count), title, '', utils.removeDoubleSpace(desc))
                        title = ''
                        desc = ''
                        print '----------------------------------'
                    if count != 1 and count != 9 and count != 10:
                        if count == 2:
                            desc += td.text.strip()[td.text.strip().find(' ') :].strip() + ' '
                        elif count == 3:
                            title = utils.removeDoubleSpace(td.text.strip())
                        elif count == 5 and td.a != None:
                            desc += td.a.text.strip() + ' '
                        else:
                            desc += td.text.strip() + ' '
                if key == 'microsoft':
                    if count > 7:
                        count = 1
                        print title
                        self.count += 1
                        self.write_db(f, item_id + str(self.count), title, '', utils.removeDoubleSpace(desc))
                        title = ''
                        desc = ''
                        print '----------------------------------'
                    if count != 1 and count != 7:
                        if count == 2:
                            desc += td.text.strip()[td.text.strip().find(' ') :].strip() + ' '
                        elif count == 3:
                            title = utils.removeDoubleSpace(td.text.strip())
                        else:
                            desc += td.text.strip() + ' '
                if key == 'apple':
                    if count > 8:
                        print title
                        count = 1
                        self.count += 1
                        self.write_db(f, item_id + str(self.count), title, '', utils.removeDoubleSpace(desc))
                        title = ''
                        desc = ''
                        print '----------------------------------'
                    if count != 1 and count != 7 and count != 8:
                        if count == 2:
                            desc += td.text.strip()[td.text.strip().find(' ') :].strip() + ' '
                        elif count == 3:
                            title = utils.removeDoubleSpace(td.text.strip())
                        else:
                            desc += td.text.strip() + ' '
                if key == 'ibm':
                    if count > 6:
                        print title
                        count = 1
                        self.count += 1
                        self.write_db(f, item_id + str(self.count), title, '', utils.removeDoubleSpace(desc))
                        title = ''
                        desc = ''
                        print '----------------------------------'
                    if count != 6:
                        if count == 1:
                            desc += td.text.strip()[td.text.strip().find(' ') :].strip() + ' '
                        elif count == 2:
                            title = utils.removeDoubleSpace(td.text.strip())
                        else:
                            desc += td.text.strip().replace('\n','') + ' '
                if key == 'yahoo':
                    if count > 8:
                        count = 1
                        print title
                        self.count += 1
                        self.write_db(f, item_id + str(self.count), title, '', utils.removeDoubleSpace(desc))
                        title = ''
                        desc = ''
                        print '----------------------------------'
                    if count != 1 and count != 8:
                        if count == 2:
                            desc += td.text.strip()[td.text.strip().find(' ') :].strip() + ' '
                        elif count == 3:
                            title = utils.removeDoubleSpace(td.text.strip())
                        else:
                            desc += td.text.strip() + ' '
                if key == 'twitter':
                    if count > 8:
                        count = 1
                        print title
                        self.count += 1
                        self.write_db(f, item_id + str(self.count), title, '', utils.removeDoubleSpace(desc))
                        title = ''
                        desc = ''
                        print '----------------------------------'
                    if count != 1 and count != 8:
                        if count == 2:
                            desc += td.text.strip()[td.text.strip().find(' ') :].strip() + ' '
                        elif count == 3:
                            title = utils.removeDoubleSpace(td.text.strip())
                        else:
                            desc += td.text.strip() + ' '

            self.close_db(f)
            if file_lines != self.count and self.count > 0:
                self.do_upgrade_db(file_name)
                print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
            else:
                self.cancel_upgrade(file_name)
                print "no need upgrade\n"
start = MergersAndAcquisitionsSpider()
start.doWork()
