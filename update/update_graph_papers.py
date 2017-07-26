#!/usr/bin/env python


from spider import *
sys.path.append("..")
from utils import Utils

class GraphPapersSpider(Spider):
    def __init__(self):
        Spider.__init__(self)
        self.school = 'GraphPapers'
        self.util = Utils()


    def getPapers(self, conference, year, link):
        print link
        r = requests.get(link)
        soup = BeautifulSoup(r.text) 
        paper_list = []
        i = 0

        file_name = self.get_file_name("eecs/papers/" + self.school.lower() + '/' + conference + year, '')
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for dl in soup.find_all('dl'):
            soup1 = BeautifulSoup(dl.prettify())
            for dt in soup1.find_all('dt'):
                title = dt.text.strip().replace('\n', '')
                #if title.startswith('('):
                #    continue
                if title.find('(') != -1:
                    title = title[0 : title.find('(')].strip()
                paper_list.append(title)
            if len(soup1.find_all('dd')) != len(soup1.find_all('dt')):
                i += len(soup1.find_all('dt'))
                continue
            for dd in soup1.find_all('dd'):
                author_list = []
                if dd.text.find('),') != -1:
                    for author in self.util.removeDoubleSpace(dd.text.strip().replace('\n', '')).split('),'):
                        author_list.append(author + ')')
                elif dd.text.find(',') != -1:
                    for author in self.util.removeDoubleSpace(dd.text.strip().replace('\n', '')).split(','):
                        author_list.append(author)
                else:
                    author_list.append(self.util.removeDoubleSpace(dd.text.strip().replace('\n', '')))

                new_author_list = []
                for au in author_list:
                    if au == '' or au.find(')') != -1:
                        continue
                    if au.find('(') != -1:
                        new_author_list.append(au[0 : au.find('(')].strip())
                    else:
                        new_author_list.append(au)

                if paper_list[i] != '':
                    self.count += 1
                    paper_id = conference + year + '-' + str(self.count)
                    self.write_db(f, paper_id, paper_list[i], '', 'author:' + ', '.join(new_author_list))

                    print paper_list[i] + '  ' + ','.join(author_list)
                i += 1
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n" 

    def doWork(self):
        r = requests.get('http://kesen.realtimerendering.com/')
        for line in r.text.split('\n'):
            if line.startswith('<li><a') and line.lower().find('.htm') != -1 and line.find('http://') == -1:
                data = line[line.find('"') + 1 : line.find('"', line.find('"') + 1)]
                if data.find('20') == -1:
                    continue
                conference = data[0 : data.find('20')]
                year = ''
                if data.lower().find('paper') != -1:
                    year = data[data.find('20') : data.lower().find('paper')]
                else:
                    year = data[data.find('20') : data.find('.htm')]
                #if year != '2017':
                #    continue
                print conference + ' -  - - - ' + year
                self.getPapers(conference, year, 'http://kesen.realtimerendering.com/' + data)

start = GraphPapersSpider()
start.doWork()
