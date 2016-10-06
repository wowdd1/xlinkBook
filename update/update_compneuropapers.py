#!/usr/bin/env python

from spider import *

class CompneuroPapersSpider(Spider):

    def __init__(self):
	Spider.__init__(self)
	self.school = 'compneuropapers'
	self.batch_size = 300

    def doWork(self):
	papers = []
	for page in range(1, 150):
	    r = self.requestWithProxy('http://compneuropapers.tumblr.com/page/' + str(page))
	    #r = self.requestWithProxy2('http://compneuropapers.tumblr.com/page/' + str(page))
	    soup = BeautifulSoup(r.text)
	    item = False
	    for p in soup.find_all('p'):
		if p.a != None and p.a.text.strip() != '':
	            title = p.a.text.strip().replace('\n', '').strip()
		    title = title.replace('.', '')
                    self.count += 1
		    papers.append([title, p.a['href']])
		    item = True
		    print title
	    if item == False:
		if len(papers) > 0:
		    self.savePapers(papers)
		break

    def savePapers(self, papers):
        more = len(papers) % self.batch_size
	max = 0
	if more > 0:
	    self.realSavePapers(papers[0 : more], 'compneuro' + str(len(papers) - more + self.batch_size) + '-inc')
	    papers = papers[more : ]

	while (len(papers) - max) >= 0:
	    self.realSavePapers(papers[max : max + self.batch_size], 'compneuro' + str(len(papers) - max))
	    max = max + self.batch_size

    def realSavePapers(self, papers, filename):
        file_name = self.get_file_name('cognitive-neuroscience/papers/compneuro/' + filename, self.school)
	file_lines = self.countFileLineNum(file_name)
	f = self.open_db(file_name + ".tmp")
	count = 0
        for p in papers:
	    count += 1
	    self.write_db(f, 'compneuropapers-' + str(count), p[0], p[1])

        self.close_db(f)
	if file_lines != count and count > 0:
	    self.do_upgrade_db(file_name)
	    print "before lines: " + str(file_lines) + " after update: " + str(count) + " \n\n"
	else:
	    self.cancel_upgrade(file_name)
	    print "no need upgrade\n"


start = CompneuroPapersSpider()
start.doWork()
