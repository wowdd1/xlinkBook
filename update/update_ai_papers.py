#!/usr/bin/env python


from spider import *
sys.path.append("..")
from utils import Utils
from record import Record

class AiPapersSpider(Spider):
    def __init__(self):
        Spider.__init__(self)
        self.school = 'aipapers'
        self.util = Utils()
        self.category = self.category_obj.paper

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
            file_name = self.get_file_name("eecs/papers/" + self.school.lower() + '/' + key, "scholaroctopus")
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
        #r = self.requestWithProxy('http://cvpapers.com')
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
                if a['href'].startswith('http'):
                    continue

                r = requests.get('http://cvpapers.com/' + a['href'])
                #r = self.requestWithProxy('http://cvpapers.com/' + a['href'])

                if year.find('NEW') != -1:
                    year = year.replace('NEW', '').strip()
                print conference + ' ' + year
                soup = BeautifulSoup(r.text)
                paper_list = []
                if year != '2017':
                    continue

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
            #if int(year) > 1986:
            if int(year) > 2015:
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

    def getNlpPaper(self):
        r = requests.get('http://www.aclweb.org/anthology/')
        soup = BeautifulSoup(r.text)
        th_list = []
        td_list = []
        for th in soup.find_all('th'):
            th_text = th.text
            if th_text.find(":") != -1:
                th_text = th_text.replace(":", "")
            if th_text.find("*") != -1:
                th_text = th_text.replace("*", "")
            if th_text.find("/") != -1:
                th_text = th_text.replace("/", "-")
            th_list.append(th_text)
        for td in soup.find_all('td'):
            td_list.append(td.prettify())

        print len(th_list)
        print len(td_list)
        for i in range(0, len(th_list)):
            if th_list[i] == "In Progress":
                continue
            print th_list[i]
            soup2 = BeautifulSoup(td_list[i])
                    
            for a in soup2.find_all('a'):
                if a['href'][1 : 2] == "/":
                    file_name = self.get_file_name("eecs/papers/" + self.school.lower() + '/' + th_list[i] + "-" + a.text.strip(), "scholaroctopus")
                    file_lines = self.countFileLineNum(file_name)
                    f = self.open_db(file_name + ".tmp")
                    self.count = 0

                    print a.text.strip() + " " + a['href']
                    base_url = 'http://www.aclweb.org/anthology/' + a['href']
                    r = requests.get(base_url)
                    soup3 = BeautifulSoup(r.text)
                    if 'CoNLL' == th_list[i]:
                        for li in soup3.find_all('li'):
                            if li.a != None and li.i != None and li.b != None:
                                print li.a.text + ' ' + li.i.text + ' ' + li.b.text
                                self.writeNlpLine(f, li.a.text, li.i.text.replace('\n', ''), li.b.text.replace('\n', ''), base_url + li.a['href'])
                                self.count = self.count + 1
                    else:
                        for p in soup3.find_all('p'):
                            if p.a != None and p.i != None and p.b != None:
                                print p.a.text + ' ' + p.i.text + ' ' + p.b.text
                                self.writeNlpLine(f, p.a.text, p.i.text.replace('\n', ''), p.b.text.replace('\n', ''), base_url + p.a['href'])
                                self.count = self.count + 1

                    self.close_db(f)
                    if file_lines != self.count and self.count > 0:
                        self.do_upgrade_db(file_name)
                        print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
                    else:
                        self.cancel_upgrade(file_name)
                        print "no need upgrade\n"

            #print '------'

    def writeNlpLine(self, f, paper_id, title, author, url):
        self.write_db(f, paper_id, title, url, "author:" + author)

    def getJMLRPaper(self):
        r = requests.get("http://jmlr.csail.mit.edu/papers/")
        soup = BeautifulSoup(r.text)
        for p in soup.find_all('p'):
            if p.a != None and p.a.font != None:
                topic = p.a['href']
                url = "http://jmlr.csail.mit.edu/papers/" + p.a['href']
                if topic.find('/') != -1:
                    topic = topic[topic.find('/') + 1 : topic.find('.')]
                self.getJMLRPapers(url, topic)
    def getJMLRPapers(self, url, topic):
        print topic
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        file_name = self.get_file_name("eecs/papers/" + self.school.lower() + '/jmlr'  + "-" + topic, "scholaroctopus")
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for dl in soup.find_all('dl'):
            title = dl.dt.text.strip().replace("\n", "")
            if title.find('(') != -1:
                title = title[0 : title.find('(')].strip()
            authors = dl.dd.b.text
            link = dl.dd.a['href'].strip()
            if link[0 : 4] != "http":
                if link[0 : 1] != '/':
                    link = url + '/' + link
                else:
                    link = url[0 : url.find('/')] + link
            print title
            print authors
            #print link
            self.count += 1
            self.write_db(f, 'jmlr-' + topic + '-' + str(self.count), title, link, "author:" + authors)
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def getIJCAIPaper(self):
        self.getIJCAIPastPapers()

    def getIJCAIPastPapers(self):
        r = requests.get("http://ijcai.org/Past_Proceedings")
        soup = BeautifulSoup(r.text)
        for a in soup.find_all('a'):
            if (a.text == "Proceedings" or a.text.find('vol')) != -1 and a['href'].startswith('http'):
                year = a['href'].replace('http://ijcai.org/proceedings/', '')
                topic = 'ijcai-' + year
                self.getIJCAIPapers(a['href'], topic, year)

    def getIJCAIPapers(self, url, topic, year):
        print url
        print topic
        print year
        r = requests.get(url)
        #print r.text

        file_name = self.get_file_name("eecs/papers/" + self.school.lower() + '/' + topic.lower(), "scholaroctopus")
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        soup = BeautifulSoup(r.text)
        for a in soup.find_all('a'):
            if a['href'].find('pdf') != -1:
                title = self.util.removeDoubleSpace(a.text.replace('\n', '')).strip()
                print title
                self.count += 1
                self.write_db(f, topic.lower() + '-' + str(self.count), title, a['href'])
        #for line in r.text.spilt("\n"):
        #    if line.find("p>") != -1:
        #        print line
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def getRSSPaper(self):
        r = requests.get("http://www.roboticsproceedings.org/")
        soup = BeautifulSoup(r.text)
        topic = ""
        for li in soup.find_all("li"):
            if li.attrs.has_key("class"):
                if li["class"][0] == "label" and li.text.startswith("RSS"):
                    topic = li.text.replace(" ", "-")
                if li["class"][0] == "menu" and li.a != None and li.a["href"].find("index") != -1 and li.text.startswith("Content"):
                    self.getRSSPapers("http://www.roboticsproceedings.org/" + li.a["href"], topic)

    def getRSSPapers(self, url, topic):
        file_name = self.get_file_name("eecs/papers/" + self.school.lower() + '/' + topic, "scholaroctopus")
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        for tr in soup.find_all("tr"):
            if tr.td != None and tr.td.a != None and tr.td.i != None:
                title = tr.td.a.text.replace("\n", '')
                authors = tr.td.i.text
                link = url.replace("index.html", tr.td.a["href"].replace(".html", ".pdf"))
                print title
                self.count += 1
                self.write_db(f, topic + "-" + str(self.count), title, link, "author:" + authors)

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def getCVFoundationPapers(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        title_list = []
        author_list = []
        link_list = []
        records = []

        for dt in soup.find_all('dt', class_='ptitle'):
            title_list.append(dt.text.strip())
        count = 0
        for dd in soup.find_all('dd'):
            if count % 2 == 0:
                author_list.append(self.util.removeDoubleSpace(dd.text.strip().replace('\n', '')).replace(',', ', '))
            else:
                if dd.a['href'].find('openaccess') == -1:
                    link_list.append("http://www.cv-foundation.org/openaccess/" + dd.a['href'])
                else:
                    link_list.append("http://www.cv-foundation.org" + dd.a['href'])
            count += 1
        for i in range(0, len(title_list)):
            #print i
            #print title_list[i]
            #print author_list[i]
            #print link_list[i]
            records.append(Record(' | ' + title_list[i] + ' | ' + link_list[i] + ' | ' + "author:" + author_list[i]))
        return records

    def saveCVFoundationPapers(self, records, year, conf):

        file_name = self.get_file_name("eecs/papers/" + self.school.lower() + '/' + conf + '-' + year, "scholaroctopus")
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
        for record_list in records:
            for record in record_list:
                self.count += 1
                print record.get_title().strip()
                self.write_db(f, conf + '-' + year + '-' + str(self.count), record.get_title().strip(), record.get_url().strip(), record.get_describe().strip())
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def getCVFoundation(self):
        r = requests.get('http://www.cv-foundation.org/openaccess/menu.py')
        soup = BeautifulSoup(r.text)
        for dd in soup.find_all('dd'):
            title = dd.text[0: dd.text.find(',')].strip()
            print title
            year = title[title.find(' ') :].strip()
            conf = title[0 : title.find(' ')].strip().lower()
            
            records = []
            sp = BeautifulSoup(dd.prettify())
            for a in sp.find_all('a'):
                if a.text.strip().startswith('Main'):
                    records.append(self.getCVFoundationPapers(a['href']))
                    print 'Main'
                else:
                    r2 = requests.get(a['href'])
                    sp2 = BeautifulSoup(r2.text)
                    for a in sp2.find_all('a'):
                        if a['href'].endswith('.py') and a.text != 'Back':
                            print a.text
                            records.append(self.getCVFoundationPapers(a['href']))

            self.saveCVFoundationPapers(records, year, conf)
                

start = AiPapersSpider()
#start.getIcmlPaper()

start.doWork()
start.getCvPaper()
start.getNipsPaper()
start.getIcmlPaper()
start.getNlpPaper()
start.getJMLRPaper()
start.getRSSPaper()
start.getIJCAIPaper()
start.getCVFoundation()

#TODO
#ICLR http://www.iclr.cc/doku.php?id=ICLR2017:main&redirect=1
#TPAMI http://dblp.uni-trier.de/db/journals/pami/
#AI http://dblp.uni-trier.de/db/journals/ai/
#IJCV http://dblp.uni-trier.de/db/journals/ijcv/

#IJCAI2015 http://ijcai.org/proceedings/2015
#ijrr http://www.ijrr.org/
#ICRA http://ieeexplore.ieee.org/xpl/conhome.jsp?punumber=1000639
#IROS http://ieeexplore.ieee.org/xpl/conhome.jsp?punumber=1000393
#ROBIO ...
