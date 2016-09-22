#!/usr/bin/env python

from spider import *
import time

class UniversityRankSpider(Spider):

    def __init__(self):
        Spider.__init__(self)
        self.subject = 'rank'

    def processQSData(self):
        self.school = 'QS'
        base_url = 'http://www.topuniversities.com'
        r = requests.get(base_url + '/subject-rankings')
        soup = BeautifulSoup(r.text)
        for div in soup.find_all('div', class_='link'):
            sp = BeautifulSoup(div.prettify())
            for li in sp.find_all('li'):
                #if self.need_update_subject(li.text.strip()) == False:
                #    continue
                print li.text.strip() + " " + li.a['href']
                url = li.a['href']
                if url.startswith('http') == False:
                    url = base_url + url
                r = requests.get(url)
                if r.text.find('flat_file') != -1:
                    sub = li.a['href'].strip()
                    while sub.find('/') != -1:
                        sub = sub[sub.find('/') + 1 :]

                    file_name = self.get_file_name(self.subject + '/' + self.school + '/' + sub, self.school)
                    file_lines = self.countFileLineNum(file_name)
                    f = self.open_db(file_name + ".tmp")
                    self.count = 0

                    pos = r.text.find('flat_file')
                    data_url = r.text[r.text.find('http', pos) : r.text.find('",', pos)].replace('\\', '')
                    sub = data_url
                    while sub.find('/') != -1:
                        sub = sub[sub.find('/') + 1 :]
                    sub = sub[0 : sub.find('.txt')]
                    r = requests.get(data_url)
                    jobj = json.loads(r.text)
                    for obj in jobj:
                        print obj['rank'] + ' ' + obj['title']
                        self.count += 1
                        self.write_db(f, self.school.lower() + '-' + sub + '-' + obj['rank'], obj['title'], '')

                    self.close_db(f)
                    if file_lines != self.count and self.count > 0:
                        self.do_upgrade_db(file_name)
                        print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
                    else:
                        self.cancel_upgrade(file_name)
                        print "no need upgrade\n"

    def processTimesHigherEducationData(self):
        self.school = 'TimesHigherEducation'

        urlDict = {'Physical sciences' : 'https://www.timeshighereducation.com/sites/default/files/datatables_json/the_wur_datatables-panel_pane_1-bfd5c82ec91d45711402c806f2d8fba3.json',\
                   'Engineering technology' : 'https://www.timeshighereducation.com/sites/default/files/datatables_json/the_wur_datatables-panel_pane_1-f369c4f4d024fe736b98e1c1933f302c.json',\
                   'Social sciences' : 'https://www.timeshighereducation.com/sites/default/files/datatables_json/the_wur_datatables-panel_pane_1-105c8bf883b26f5bdb13a6862a77c709.json',\
                   'Life sciences' : 'https://www.timeshighereducation.com/sites/default/files/datatables_json/the_wur_datatables-panel_pane_1-ada0b99e3056c85b43b74b5bf1dd0688.json',\
                   'Arts humanities' : 'https://www.timeshighereducation.com/sites/default/files/datatables_json/the_wur_datatables-panel_pane_1-3f868daadcc97eaefecc84c459d9348a.json',\
                   'Clinical pre-clinical health' : 'https://www.timeshighereducation.com/sites/default/files/datatables_json/the_wur_datatables-panel_pane_1-085f64cf3b9082d99ccbcdd38f980edc.json'}


        for subject, url in [(k, urlDict[k]) for k in urlDict.keys()]:
            print subject
            r = requests.get(url)
            jobj = json.loads(r.text)
            file_name = self.get_file_name(self.subject + '/' + self.school + '/' + subject, self.school)
            file_lines = self.countFileLineNum(file_name)
            f = self.open_db(file_name + ".tmp")
            self.count = 0
            for obj in jobj['data']:
                #print obj
                print obj['rank'] + " " + obj['title']
                self.count += 1
                self.write_db(f, 'the-' + subject.lower().replace(' ', '-') + "-" + obj['rank'], obj['title'], 'https://www.timeshighereducation.com' + obj['path'])

            self.close_db(f)
            if file_lines != self.count and self.count > 0:
                self.do_upgrade_db(file_name)
                print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
            else:
                self.cancel_upgrade(file_name)
                print "no need upgrade\n"

    def processARWUData(self):
        self.school = 'arwu'
        r = requests.get('http://www.shanghairanking.com/index.html')
        soup = BeautifulSoup(r.text)
        sub = {}
        sublist = []
        for div in soup.find_all('div', class_='sublist'):
            sp = BeautifulSoup(div.prettify())
            data = []
            for li in sp.find_all('li'):
                data.append(li.text)
            sublist.append(data)

        count = 0
        for ul in soup.find_all('ul', class_='tabbtn'):
            for line in ul.text.strip().split('\n'):
                sub[line.strip()] = sublist[count]
                count += 1
            
        for s in sub.keys():
            print s
            #if self.need_update_subject(s) == False:
            #    continue
            file_name = self.get_file_name(self.subject + '/' + self.school + '/' + s, self.school)
            file_lines = self.countFileLineNum(file_name)
            f = self.open_db(file_name + ".tmp")
            self.count = 0

            for item in sub[s]:
                title = item.strip().replace('\n', '')
                title = title[title.find(' ') :].strip()
                self.count += 1
                print title
                self.write_db(f, self.school + '-' + s + '-' + str(self.count), title, '')

            self.close_db(f)
            if self.count > 0:
                self.do_upgrade_db(file_name)
                print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
            else:
                self.cancel_upgrade(file_name)
                print "no need upgrade\n"

    def processUsnewsData(self):
        self.school = 'usnews'
        sub_list = ["Agricultural-Sciences",\
                "Arts-Humanities",\
                "Biology-Biochemistry",\
                "Chemistry",\
                "Clinical-Medicine",\
                "Computer-Science",\
                "Economics-Business",\
                "Engineering",\
                "Environment-Ecology",\
                "Geosciences",\
                "Immunology",\
                "Materials-Science",\
                "Mathematics",\
                "Microbiology",\
                "Molecular-Biology-Genetics",\
                "Neuroscience-Behavior",\
                "Pharmacology-Toxicology",\
                "Physics",\
                "Plant-Animal-Science",\
                "Psychiatry-Psychology",\
                "Social-Sciences-Public-Health",\
                "Space-Science"]
        for sub in sub_list:
            #if self.need_update_subject(sub) == False:
            #    continue
            r = requests.get('http://www.usnews.com/education/best-global-universities/search?region=&subject=' + sub.lower() + '&name=')
            soup = BeautifulSoup(r.text)
            file_name = self.get_file_name(self.subject + '/' + self.school + '/' + sub, self.school)
            file_lines = self.countFileLineNum(file_name)
            f = self.open_db(file_name + ".tmp")
            self.count = 0
            print 'processing ' + sub
            for h2 in soup.find_all('h2', class_='h-taut'):
               print h2.a.text
               self.count += 1
               self.write_db(f, self.school + '-' + sub + '-' + str(self.count), h2.a.text, h2.a['href'])

            self.close_db(f)
            if self.count > 0:
                self.do_upgrade_db(file_name)
                print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
            else:
                self.cancel_upgrade(file_name)
                print "no need upgrade\n"

    def doWork(self):
        self.processQSData()
        self.processTimesHigherEducationData()
        self.processARWUData()
        self.processUsnewsData()


start = UniversityRankSpider()
start.doWork()
