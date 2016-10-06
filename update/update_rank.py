#!/usr/bin/env python
# -*- coding: utf-8 -*-
#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07

from spider import *
sys.path.append("..")
from utils import Utils

class BaikeSpider(Spider):

    def __init__(self):
        Spider.__init__(self)
        self.subject = 'rank'
        self.school = "baike"


    def processNobelprize(self):
        subjects = ['physics', 'chemistry', 'medicine', 'literature', 'peace', 'economic-sciences']

        for subject in subjects:

            file_name = self.get_file_name(self.subject + "/nobel/" + subject, 'nobel')
            file_lines = self.countFileLineNum(file_name)
            f = self.open_db(file_name + ".tmp")
            self.count = 0

            r = requests.get('http://www.nobelprize.org/nobel_prizes/' + subject + '/laureates/')
            soup = BeautifulSoup(r.text)
            for div in soup.find_all('div', class_='by_year'):
                if div.h3 == None or div.h6 == None or div.p == None:
                    continue
                year = div.h3.text.strip()
                year = year[year.rfind(' ') :].strip()
                print year
                soup2 = BeautifulSoup(div.prettify())
                author = ""
                desc = ""
                for a in soup2.find_all('a'):
                    if a['href'].find('html') == -1:
                        continue
                    author += a.text.strip() + ', '
                for p in soup2.find_all('p'):
                    if p.text.strip() == "":
                        continue
                    desc += p.text.strip().replace('\n', '').replace('"', '') + ", "
                author = author[0 : len(author) - 2]
                desc = desc[0 : len(desc) - 2]
                #print div.h6.text.strip().replace(' and', ',')
                #print div.p.text.strip().replace('\n', '').replace('"', '')
                self.count += 1
                self.write_db(f, 'nobel-' + subject + '-' + year, year + ' ' + author, 'http://www.nobelprize.org' + div.a['href'], 'winner:' + author + " description:" + desc)

            self.close_db(f)
            if file_lines != self.count and self.count > 0:
                self.do_upgrade_db(file_name)
                print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
            else:
                self.cancel_upgrade(file_name)
                print "no need upgrade\n"

    def processFieldsMedal(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        desc = ''
        winner = ''
        year = ''
        file_name = self.get_file_name(self.subject + "/fieldsmedal", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for tr in soup.find_all('tr'):
            data = tr.text.split('\n')
            id = data[1].strip()
            if tr.td != None and tr.td.text.find('University') != -1:
                break
            soup2 = BeautifulSoup(tr.prettify())
            if id.isdigit():
                if data[3] == 'Awarded for' or data[len(data) - 2] == 'Presented by':
                    continue
                if desc != '':
                    print winner[0 : len(winner) - 2]
                    print desc[0 : len(desc) - 2]
                    print ''

                    self.count += 1
                    self.write_db(f, "fieldsmedal-" + year, year + ' ' + winner[0 : len(winner) - 2], '', 'winner:' + winner[0 : len(winner) - 2] + ' description:' + desc[0 : len(desc) - 2])

                    winner = ''
                    desc = ''
                    year = ''
                #print data[1] + ' ' + data[3]
                year = id
                winner += data[3] + ', '
                desc += data[3] + ':' + data[len(data) - 2].replace('\n', '').replace('"', '') + ' ' 
                continue 
            if (tr.td != None and tr.td.a != None and tr.td.a.has_key('title')):
                #print data[1]
                if data[1] == 'Awarded for' or tr.text.find('Presented by') != -1:
                    continue
                winner += data[1] + ', '
                desc += data[1] + ':' + data[len(data) - 2].replace('\n', '').replace('"', '') + ' '

        if desc != '':
            self.count += 1
            self.write_db(f, "fieldsmedal-" + year, year + ' ' + winner[0 : len(winner) - 2], '', 'winner:' + winner[0 : len(winner) - 2] + ' description:' + desc[0 : len(desc) - 2])


        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def processWolfPrizeMathematics(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        desc = ""
        year = ''
        winner = ''

        file_name = self.get_file_name(self.subject + "/wolfprize-mathematics", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for tr in soup.find_all('tr'):
            data = tr.text.split('\n')
            #print data
            if data[2].find('No award') != -1 or data[1].find('Year') != -1 or data[1].find('Citation') != -1:
                continue
            if data[1] == '':
                break
            if data[1].startswith('1') or data[1].startswith('2'):
                if desc != '':
                    winner = winner[0 : len(winner) - 2]
                    desc = desc.strip()
                    print year + ' ' +  winner
                    print desc
                    self.count += 1
                    self.write_db(f, 'wolfprize-math-' + year, year + ' ' + winner, '', 'winner:' + winner + ' description:' + desc)
                    year = ''
                    winner = ''
                    desc = ''
                year = data[1].strip()
                winner += data[2].strip() + ', ' 
                desc += data[2].strip() + ':' + data[len(data) - 2].strip() + ' '
            else:
                winner += data[1].strip() + ', '
                desc += data[2].strip() + ':' + data[len(data) - 2].strip() + ' '
        if desc != '':
            winner = winner[0 : len(winner) - 2]
            desc = desc.strip()
            print year + ' ' +  winner
            print desc
            self.count += 1
            self.write_db(f, 'wolfprize-math-' + year, year + ' ' + winner, '', 'winner:' + winner + ' description:' + desc)
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def processBreakthroughPrize(self):
        data = {'1' : 'Fundamental-Physics',\
                '2' : 'Life-Sciences',\
                '3' : 'Mathematics'}

        for k, v in data.items():
            data2 = None
            if k == '1':
                data2 = {'P4' : 'Special-Breakthrough-Prize',\
                         'P2' : 'New-Horizons-Prize',\
                         'P3' : 'Physics-Frontiers-Prize',\
                         'P1' : 'Breakthrough-Prize'}

            elif k == '2':
                data2 = { 'P1' : 'Breakthrough-Prize'}
            elif k == '3':
                data2 = { 'P1' : 'Breakthrough-Prize',\
                          'P2' : 'New-Horizons-Prize'}
            oldv = v
            for k2, v2 in data2.items():
                v = oldv
                v = v + '-' + v2
                r = requests.get('https://breakthroughprize.org/Laureates/' + k + '/' + k2)
                soup = BeautifulSoup(r.text)
                ul = None
                for u in soup.find_all('ul', class_='filter'):
                    if u.li.text.strip().startswith('20'):
                        ul = u
                        break
                soup2 = BeautifulSoup(ul.prettify())
                years = []
                for li in soup2.find_all('li'):
                    years.append(li.text.strip())

                file_name = self.get_file_name(self.subject + "/breakthroughprize/" + v.lower(), 'breakthroughprize')
                file_lines = self.countFileLineNum(file_name)
                f = self.open_db(file_name + ".tmp")
                self.count = 0


                for year in years:
                    url = 'https://breakthroughprize.org/Laureates/' + k +'/' + k2 + '/Y' + year
                    r = requests.get(url)
                    soup = BeautifulSoup(r.text)
                    ul = None
                    for u in soup.find_all('ul', class_='people'):
                        if u.li != None and u.li.span != None:
                            ul = u
                            break
                    soup2 = BeautifulSoup(ul.prettify())
                    winner = ''
                    for li in soup2.find_all('li'):
                        #print li.prettify()
                        title = li.span.a.text.strip()
                        if title.find('and the') != -1:
                            title = title[0 : title.find('and the')]

                        winner += title.strip() + ', '
                    winner = winner[0 : len(winner) - 2]
                    print winner
                    self.count += 1
                    self.write_db(f, 'breakthroughprize-' + v.lower() + '-' + year, year + ' ' + winner, url, 'winner:' + winner)
                
                self.close_db(f)
                if file_lines != self.count and self.count > 0:
                    self.do_upgrade_db(file_name)
                    print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
                else:
                    self.cancel_upgrade(file_name)
                    print "no need upgrade\n"


    def processBaikeData(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        file_name = self.get_file_name(self.subject + "/programmer", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
        p_all = soup.find_all("p")

        for p in p_all:
            if p.prettify()[0:60].find("Peter Norvig") != -1:
                for line in p.prettify().replace('<br>', '').replace('</br>', '').replace('<br/>', '').replace('<p>', '').replace('</p>', '').split("\n"):
                    line = line.strip()
                    if line != "" and line != "# Name Description":
                        pos_1 = line.find(" ")
                        pos_2 = line.find(" ", pos_1 + 1)
                        pos_3 = line.find(" ", pos_2 + 1)
                        print line[0 : pos_1] + " " + line[pos_1 + 1 : pos_3] + " " + line[pos_3 + 1 :]
                        self.write_db(f, line[0 : pos_1], line[pos_1 + 1 : pos_3], "", 'description:' + line[pos_3 + 1 :])
                        self.count += 1

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def processWikiTuringData(self, url):

        file_name = self.get_file_name(self.subject + "/Turing-Award", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        for tr in soup.find_all("tr"):
            if tr.th != None and tr.text.strip()[0:1] == "1" or tr.text.strip()[0:1] == "2":
                i = 0
                link = "http://en.wikipedia.org" + str(tr.td.a["href"])
                year = ""
                title = ""
                remark = ""
                for line in tr.text.strip().split("\n"):
                    i += 1
                    #print '---' + str(i) + " " + line
                    if i == 1:
                        year = line
                        continue
                    if len(line) < 50:
                        title += " " + line
                        continue
                    if line.startswith("For") or len(line) > 50:
                        #if i != 3:
                        print year + " " + title + " " + link
                        remark = 'winner:' + title.strip().replace(' and', ',')+ ' description:' + line
                        self.count += 1
                        self.write_db(f, 'turing-' + year, year + ' ' + title.strip(), link, remark)
                        i = 0
                        continue

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def processWikiPioneerData(self, url):

        file_name = self.get_file_name(self.subject + "/Computer-Pioneer-Award", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        title = ""
        for tr in soup.find_all("tr"):
            #print tr.text.strip()         
            if tr.text.strip()[0:1] == "1" or tr.text.strip()[0:1] == "2":
                title = title.strip()
                if len(title) > 0 and title[0:1] == "1" or title[0:1] == "2":
                    self.write_db(f, title[0: title.find(" ")], title[title.find(" ") + 1 :], "")
                    print title
                    self.count += 1
                title = ""
                for line in tr.text.strip().split("\n"):
                    title += " " + line.strip()

            else:
                title += " " + tr.text.replace("\n", " ").strip()

        title = title.strip()
        if len(title) > 0 and title[0:1] == "1" or title[0:1] == "2":
            self.write_db(f, title[0: title.find(" ")], title[title.find(" ") + 1 :], "")
            print title
            self.count += 1
                
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"


    def processComputerScienceData(self, url):
        r = requests.get(url)
        utils = Utils()
        user_url = ''
        last_line = ''
        last_citations = ''
        remark = 'description:'
        file_name = self.get_file_name("eecs/people/computer-science-citations", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
        good_line = False 

        for line in r.text.split('\n'):
            good_line = False 
            remark = 'description:'
            if line.strip() == '':
                continue
            if line.find('<') != -1 and line.find('>') != -1:
                line = utils.clearHtmlTag(line).strip()
            else:
                line = line.strip()
            if len(line) < 5 or line.find('<a href') != -1:
                last_line = line
                continue
            if last_line != '':
                if last_line[0 : 1].isdigit():
                    good_line = True
                    line = utils.clearHtmlTag(last_line + ' ' + line)
                last_line = ''
            else:
                if line[0 : 1].isdigit() and line.find('(') > 0:
                    good_line = True
                    line = utils.removeDoubleSpace(line.replace('\n', ''))
            
            if good_line == False:
                continue 
            citations = line[0 : line.find(" ")]
            person = line[line.find(" ") + 1 : line.find("(")]
            place = line[line.find('(') + 1 : line.find(')')]
            info = line[line.find(')') + 2 :].strip()
            #print citations
            title = person
            #print info
            remark +=  citations + ' citations, ' + info
            if citations != last_citations:
                self.count += 1
            last_citations = citations
	    if title.find('>') != -1:
		title = title[title.find('>') + 1 :].strip()
            self.write_db(f, 'csc-' + str(self.count), title, '', 'university:' + place + ' ' + remark)

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def processTop100Scientific(self, url):
        file_name = self.get_file_name(self.subject + "/top100-scientific", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        for tr in soup.find_all('tr'):
            if tr.td.text.isnumeric():
                count = 0
                desc = ""
                title = ""
                for line in tr.prettify().split('\n'):
                    count += 1
                    if count == 6:
                        title = line.strip()
                    if count == 9:
                        desc = 'description:' + line.strip()
                print title
                self.count += 1
                self.write_db(f, 'top100-scientific-' + str(self.count), title, '', desc)
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"
        
    def processLeaderOfCountry(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        start = False
        file_name = self.get_file_name(self.subject + "/head-of-country", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
        for tr in soup.find_all('tr'):
            textList = tr.text.split('\n')
            title = ''
            index = 0
            country = ''
            for text in textList:
                if text == '中国':
                    start = True
                if text == '通用名称':
                    title = ''
                    break
                index += 1
                if index == 2:
                    country = text.strip()
                if index == 3 or index == 2:
                    continue
                title += text.strip() + ' '
            if start and title != '':
                print title.strip()
                self.count += 1
                self.write_db(f, "head-of-country-" + str(self.count), country, '', 'description:' + title.strip())
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def processOldTR35(self):
        r = requests.get('http://www2.technologyreview.com/tr35/?year=1999')
        soup = BeautifulSoup(r.text)
        ul = soup.find('ul', class_='years')
        soup = BeautifulSoup(ul.prettify())
        for li in soup.find_all('li'):
            year = li.a.text.strip()
            if year == '2013':
                continue

            file_name = self.get_file_name(self.subject + "/mit-tr35/tr35-" + year + "#", '')
            file_name = file_name[0 : file_name.find('#')]
            file_lines = self.countFileLineNum(file_name)
            f = self.open_db(file_name + ".tmp")
            self.count = 0

            r2 = requests.get('http://www2.technologyreview.com/' + li.a['href'])
            sp = BeautifulSoup(r2.text)
            for div in sp.find_all('div', class_='item'):
                data = div.text.strip().replace('\t', '').split('\n')
                index = 0
                title = ''
                desc = 'description:'
                for d in data:
                    if d == '':
                        continue
                    index += 1
                    if index == 1:
                        title = d
                    else:
                        desc += d + ' '
                print title 
                print desc
                self.count += 1
                self.write_db(f, 'tr35-' + year + '-' + str(self.count), title, 'http://www2.technologyreview.com/' + div.a['href'], desc)
            self.close_db(f)
            if file_lines != self.count and self.count > 0:
                self.do_upgrade_db(file_name)
                print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
            else:
                self.cancel_upgrade(file_name)
                print "no need upgrade\n"

    def processTR35(self):
        utils = Utils()
        for i in range(0, 3):
            year = str(2013 + i)
            r = requests.get('http://www.technologyreview.com/lists/innovators-under-35/' + year)
            soup = BeautifulSoup(r.text)
            ul = soup.find('ul', class_='people')
            soup = BeautifulSoup(ul.prettify())

            file_name = self.get_file_name(self.subject + "/mit-tr35/tr35-" + year + "#", '')
            file_name = file_name[0 : file_name.find('#')]
            file_lines = self.countFileLineNum(file_name)
            f = self.open_db(file_name + ".tmp")
            self.count = 0

            for li in soup.find_all('li'):
                data = utils.removeDoubleSpace(li.text.strip().replace('\t', '').replace('\n', ''))
                title = data[0 : data.find(',')].strip()
                desc = 'description:' + data[data.find(',') + 1 :].strip() 
                print title
                print desc
                self.count += 1
                self.write_db(f, 'tr35-' + year + '-' + str(self.count), title, 'http://www.technologyreview.com/' + li.a['href'], desc)
            self.close_db(f)
            if file_lines != self.count and self.count > 0:
                self.do_upgrade_db(file_name)
                print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
            else:
                self.cancel_upgrade(file_name)
                print "no need upgrade\n"

    def processMacArthur(self, url):
        utils = Utils()
        r = requests.get(url)
        soup = BeautifulSoup(r.text)

        file_name = self.get_file_name(self.subject + "/macArthur-all-fellows", '')
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for table in soup.find_all('table', class_='multicol'):
            sp = BeautifulSoup(table.prettify())
            for li in sp.find_all('li'):
                url = ''
                if li.a != None:
                    url = 'https://en.wikipedia.org' + li.a['href']
                data = utils.removeDoubleSpace(li.text.strip().replace('\n', ''))
                title = data[0 : data.find(',')].strip()
                desc = "description:" + data[data.find(',') + 1 :].strip()
                print title
                self.count += 1
                self.write_db(f, 'macArthur-fellow-' + str(self.count), title, url, desc)

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def processTopVc(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text)

        file_name = self.get_file_name(self.subject + "/vc-silicon-valley", '')
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for h2 in soup.find_all('h2'):
            if h2.strong != None:
                title = h2.strong.text[h2.strong.text.find("）") + 1 : ].strip()
                print title
                self.count += 1
                self.write_db(f, "vc-" + str(self.count), title, '')

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"


    def processTopArtists(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text)

        file_name = self.get_file_name(self.subject + "/top-artists-from-20th-century", '')
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for tr in soup.find_all('tr'):
            if tr.a != None and tr.a.strong != None and tr.p != None:
                title = tr.a.text
                print title
                self.count += 1
                self.write_db(f, "artists-" + str(self.count), title, tr.a['href'])

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"


    def startupSpeakers(self):
        r = requests.get('http://www.startupschool.org/past/')
        soup = BeautifulSoup(r.text)

        file_name = self.get_file_name(self.subject + "/startup-speaker", '')
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for p in soup.find_all('p'):
            if p.a != None and p.a.b != None:
                print p.text
                url = "http:" + p.a['href']
                self.count += 1
                self.write_db(f, "startup-speaker-" + str(self.count), p.text.strip(), url)
        r = requests.get('http://www.startupschool.org/speakers/')
        soup = BeautifulSoup(r.text)
        for p in soup.find_all('p'):
            if p.strong != None and p.a != None:
                print p.strong.text
                url = "http:" + p.a['href']
                self.count += 1
                self.write_db(f, "startup-speaker-" + str(self.count), p.strong.text.strip(), url)

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"
    def processBloomberg(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        file_name = self.get_file_name(self.subject + "/bloomberg", '')
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for p in soup.find_all('p'):
            if p.b != None:
                title = p.text[p.text.find('.') + 1 : p.text.find('-')].strip()
                desc = 'description:' + p.text[p.text.find('-') + 1 :] .strip()
                print title
                #print desc
                self.count += 1
                self.write_db(f, 'bloomberg-' + str(self.count), title, '', desc)

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def processWatermanAward(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text)

        file_name = self.get_file_name(self.subject + "/waterman-award", '')
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for dl in soup.find_all('dl'):
            year = dl.dt.text
            title = dl.dd.a.text
            url = 'https://en.wikipedia.org' + dl.dd.a['href']
            print year + ' ' + title
            self.count += 1
            self.write_db(f, 'waterman-award-' + str(year), title, url)

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def doWork(self):
        self.processComputerScienceData('http://web.cs.ucla.edu/~palsberg/h-number.html')
        #self.processNobelprize()
        #self.processFieldsMedal('https://en.wikipedia.org/wiki/Fields_Medal')
        #self.processWikiTuringData("http://en.wikipedia.org/wiki/Turing_Award")
        #self.processBreakthroughPrize()
        #self.processWolfPrizeMathematics('https://en.wikipedia.org/wiki/Wolf_Prize_in_Mathematics')
        '''
        self.processWikiPioneerData("http://en.wikipedia.org/wiki/Computer_Pioneer_Award")
        self.processBaikeData("http://www.baike.com/wiki/IT%E4%B8%9A%E6%9C%80%E5%85%B7%E5%BD%B1%E5%93%8D%E5%8A%9B%E7%9A%84284%E4%BD%8D%E7%A8%8B%E5%BA%8F%E5%91%98")
        self.processTop100Scientific('http://www.adherents.com/people/100_scientists.html#')
        self.processLeaderOfCountry('https://zh.wikipedia.org/wiki/%E5%90%84%E5%9B%BD%E9%A2%86%E5%AF%BC%E4%BA%BA%E5%88%97%E8%A1%A8')
        self.processTR35()
        self.processOldTR35()
        self.processMacArthur('https://en.wikipedia.org/wiki/MacArthur_Fellows_Program')
        self.processTopVc('http://www.leiphone.com/news/201406/0725-annie-angel.html')
        self.processTopArtists('http://artscenetoday.com/artist_resources/times-top-200-artists/')
        self.startupSpeakers()
        self.processBloomberg('http://www.livemint.com/Politics/TGX2iczPnC5ofl2WKQR7FN/Narendra-Modi-in-Bloomberg-Markets-50-Most-Influential-list.html')
        self.processWatermanAward('https://en.wikipedia.org/wiki/Alan_T._Waterman_Award')
        '''

start = BaikeSpider()
start.doWork()
