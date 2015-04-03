#!/usr/bin/env python


from spider import *
sys.path.append("..")
from utils import Utils

class ScholarOctopusSpider(Spider):
    def __init__(self):
        Spider.__init__(self)
        self.school = 'ScholarOctopus'
        self.util = Utils()

    def doWork(self, jobj=None):
        if jobj == None:
            r = requests.get('http://cs.stanford.edu/people/karpathy/scholaroctopus/out.json')
            jobj = json.loads(r.text)

        paper_dict = {}
        for paper in jobj:
            key = paper['conference'] + '-' + str(paper['year'])
            if paper_dict.get(key, '')  == '':
                paper_dict[key] = []
            paper_dict[key].append(paper)

        for key, v in sorted([(k,paper_dict[k]) for k in sorted(paper_dict.keys())]):
            #print key + ' paper:' + str(len(paper_dict[key]))
            print 'processing ' + key
            file_name = self.get_file_name("eecs/" + self.school.lower() + '/' + key, self.school.lower())
            file_lines = self.countFileLineNum(file_name)
            if file_lines == len(v):
                continue
            f = self.open_db(file_name + ".tmp")
            self.count = 0

            for paper in sorted(v, key=lambda item : item['title']):
                self.count += 1
                paper_id = key.lower() + '-' + str(self.count)
                self.write_db(f, paper_id, paper['title'].strip(), paper['pdf'], 'author:' + ', '.join(paper['authors']))
                print paper_id + ' ' + paper['title'].strip()

            self.close_db(f)
            if file_lines != self.count and self.count > 0:
                self.do_upgrade_db(file_name)
                print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
            else:
                self.cancel_upgrade(file_name)
                print "no need upgrade\n"

    def initPaperObj(self, conference, year):
        paper_obj = {}
        paper_obj['conference'] = conference
        paper_obj['x'] = 0.34087790145304875
        paper_obj['y'] = 0.25455838359147459
        paper_obj['year'] = year
        paper_obj['pdf'] = ''
        paper_obj['authors'] = ''
        paper_obj['title'] = ''
        return paper_obj

    def getCvPaper(self):
        conference = ''
        year = ''
        r = requests.get('http://cvpapers.com')
        sp = BeautifulSoup(r.text)
        ul = sp.find('ul')
        sp = BeautifulSoup(ul.prettify())
        for li in sp.find_all('li'):
            conference = li.text[0 : li.text.find(':')].strip().lower()
            if conference.find('(') != -1:
                conference = conference[0 : conference.find('(')].strip().lower()
            sp1 = BeautifulSoup(li.prettify())
            for a in sp1.find_all('a'):
                year = a.text.strip()
                if year.startswith('BMVC'):
                    continue

                r = requests.get('http://cvpapers.com/' + a['href'])
                print conference + ' ' + year
                soup = BeautifulSoup(r.text)
                paper_list = []

                i = 0
                for dl in soup.find_all('dl'):
                    if dl.parent.name == 'dl':
                        continue
                    soup1 = BeautifulSoup(dl.prettify())
                    paper_obj = {}
                    for dt in soup1.find_all('dt'):
                        paper_obj = self.initPaperObj(conference, year)
                        #print dt.text[0 : dt.text.find('(')].strip()
                        if dt.text.find('(') != -1 :
                            paper_obj['title'] = self.util.removeDoubleSpace(dt.text[0 : dt.text.find('(')].replace('\n','')).strip()
                        else:
                            paper_obj['title'] = self.util.removeDoubleSpace(dt.text.replace('\n',''))
                        soup2 = BeautifulSoup(dt.prettify())
                        for a in soup2.find_all('a'):
                            paper_obj[a.text.strip().lower()] = a['href']
                        if paper_obj.get('pdf','') == '':
                            paper_obj['pdf'] = 'https://scholar.google.com/scholar?hl=en&q=' + paper_obj['title']
                        paper_list.append(paper_obj)

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

                        paper_list[i]['authors'] = author_list
                        #print paper_list[i]['authors']
                        i += 1
                #print len(paper_list) 
                self.doWork(paper_list)

    def getNipsPaper(self):
        r = requests.get('http://papers.nips.cc/')
        soup = BeautifulSoup(r.text)
        paper_list = []
        for li in soup.find_all('li'):
            if li.a.text == 'Books':
                continue
            title = li.a.text[li.a.text.find('(') : ].replace('(', '').replace(')', '').strip().split(' ')
            conference = title[0]
            year = title[1]
            if int(year) > 2006:
                print 'process ' + ' '.join(title)
                r = requests.get('http://papers.nips.cc' + li.a['href'])
                sp = BeautifulSoup(r.text)
                for li in sp.find_all('li'):
                    if li.a.text == 'Books':
                        continue
                    sp2 = BeautifulSoup(li.prettify())
                    paper_obj = self.initPaperObj(conference, year)
                    author_list = []
                    for a in sp2.find_all('a', class_='author'):
                        author_list.append(a.text.strip())
                    paper_obj['authors'] = author_list
                    paper_obj['title'] = li.a.text
                    paper_obj['pdf'] = 'http://papers.nips.cc' + li.a['href'] + '.pdf'
                    paper_list.append(paper_obj)
                    #print paper_obj['title']
        self.doWork(paper_list)

    def getIcmlPaper(self):
        r = requests.get('http://machinelearning.wustl.edu/mlpapers/venues')
        paper_list = []
        text = r.text[r.text.find('<a href="./venue') :]
        links = text.split('</a>')
        for a in links:
            if a.find('ICML') != -1:
                url, title = a[a.find('./') : ].split('">')
                url = 'http://machinelearning.wustl.edu/mlpapers' + url[1 :]
                conference, year = title[title.find('(') + 1 : title.find(')')].split('-')
                conference = conference.lower()
                year = '20' + year
                if int(year) >2007:
                    continue
                r = requests.get(url)
                sp = BeautifulSoup(r.text)
                for a in sp.find_all('a'):
                    if a['href'].startswith('../papers'):
                        paper_obj = self.initPaperObj(conference, year)
                        paper_obj['pdf'] = 'http://machinelearning.wustl.edu/mlpapers' + a['href'][2:].replace('/papers/', '/paper_files/') + '.pdf'
                        paper_obj['title'] = a.text.replace('\n', '')
                        paper_list.append(paper_obj)
        self.doWork(paper_list)

start = ScholarOctopusSpider()
start.doWork()
start.getCvPaper()
start.getNipsPaper()
start.getIcmlPaper()
