#!/usr/bin/env python


from spider import *

class AminerSpider(Spider):

    def __init__(self):
        Spider.__init__(self)
        self.school = 'aminer'
        self.subject = 'rank'

    def processBestpaper(self):
        r = requests.get('http://api2.aminer.org/api/bestpaper/best_vs_topcited?')
        jobj = json.loads(r.text)
        for conf in jobj:
            file_name = self.get_file_name(self.subject + '/' + self.school + '/' + conf['conf_name'].replace('/','-').lower() + '-ccf-' + conf['values'][0].lower(), self.school)
            file_lines = self.countFileLineNum(file_name)
            f = self.open_db(file_name + ".tmp")
            self.count = 0

            for year, papers in conf['values'][1].items():
                print conf['conf_name'] + ' ' + year
                for paper in papers['papers']:
                    print paper['title']
                    isBest = ''
                    if paper['isBest']:
                        isBest = "best paper"
                    year = str(paper['year'])
                    rank = 'ratings:' + str(paper['rank'])
                    citation = ''
                    if paper['n_citation'] > 0:
                        citation = str(paper['n_citation']) + ' citation'
                    authors = []
                    if paper.get('authors', '') != '':
                        for obj in paper['authors']:
                            if obj.get('name', '') != '':
                                authors.append(str(obj['name']))
                        authors = ', '.join(authors)           
                    else:
                        authors = ''
                    authors = 'author:' + authors
 
                    desc = 'description:' + year + ' ' + isBest + ' ' + citation + ' ' + rank + ' ' + authors
                    self.count += 1
                    self.write_db(f, conf['conf_name'].lower() + '-bp-' + str(self.count), paper['title'], ''.join(paper['url']), desc)

            self.close_db(f)
            if file_lines != self.count and self.count > 0:
                self.do_upgrade_db(file_name)
                print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
            else:
                self.cancel_upgrade(file_name)
                print "no need upgrade\n"

    def processBestResearcher(self, keyword):
        r = requests.get('http://api.aminer.org/api/search/people?size=100&sort=h_index&query=' + keyword)
        jobj = json.loads(r.text)
        file_name = self.get_file_name(self.subject + '/' + self.school + '/' + keyword.lower().replace(' ', '_'), self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for researcher in jobj['result']:
            print researcher['name']
            self.count += 1
            self.write_db(f, keyword.lower().replace(' ', '-') + '-br-' + str(self.count), researcher['name'], '', '')

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def doWork(self):
        #self.processBestResearcher('Social Network')
        #self.processBestResearcher('Data Mining')
        #self.processBestResearcher('Machine Learning')
        #self.processBestResearcher('Deep Learning')
        self.processBestpaper()



start = AminerSpider()
start.doWork()
