#!/usr/bin/env python

from spider import *
sys.path.append("..")
from utils import Utils

class BillionDollarClub(Spider):

    def __init__(self):
        Spider.__init__(self)
        self.school = 'billion-dollar-club'
        self.utils = Utils()


    def getKey(self, company):
        return company['Valuation']


    def doWork(self):
        r = self.requestWithProxy('http://graphics.wsj.com/billion-dollar-club/data/getData.php')
        j = json.loads(r.text)

        file_name = self.get_file_name('economics/startup', self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for jobj in sorted(j['companies'], key=self.getKey, reverse=True):

            #print jobj
            print jobj['Company']
            #print jobj['Total_funding']
            #print jobj['rounds']
            print jobj['Valuation']
            #print jobj['loc']
            #print jobj['Founded']
            #print jobj['industry']
            #print jobj['competitors']
            #print jobj['image_caption']
            company = jobj['Company'].replace('\n', '').strip()
            desc = 'ceo:' + jobj['ceo'] + ' description:' + str(jobj['Total_funding']) + ' ' + str(jobj['rounds']) +\
                   ' ' + str(jobj['Valuation']) + ' ' + jobj['loc'] + ' ' + str(jobj['Founded']) + ' ' + jobj['industry'] +\
                   ' competitors:' + jobj['competitors'] + ' '
            self.count += 1
            self.write_db(f, 'bdc-' + str(self.count), company, '', desc.replace('\n', '').strip())

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

start = BillionDollarClub()
start.doWork()
