#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from spider import *
sys.path.append("..")
from utils import Utils

class ProjectsSpider(Spider):
    def __init__(self):
        Spider.__init__(self)
        self.school = "projects"
        self.utils = Utils()

    def doWork(self):
        self.getDARPAProjects() 
        self.getDARPAOpenProjects()
        self.getAIProjects()
        self.getDotNetFoundationProjects()
        self.getMicrosoftResearch()
        self.getAICProjects()
        self.getDARPAWikiProjects()
        self.getSRIProject()
        self.getOpenSourceRobotProjects()      
        self.getMitMediaProjects()
        self.getSocialRobotProjects()
        self.getSpeechRecognitionprojects()

    def getSpeechRecognitionprojects(self):
        r = requests.get('https://en.wikipedia.org/wiki/List_of_speech_recognition_software')
        soup = BeautifulSoup(r.text)

        file_name = self.get_file_name("eecs/projects/speech-recognition", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
        
        for tr in soup.find_all('tr'):
            if tr.td != None and tr.td.div == None:
                title = tr.td.text.strip()
                url = ''
                if tr.td.a != None:
                    if tr.td.a['href'].startswith('http') == False:
                        url = "https://en.wikipedia.org" + tr.td.a['href']
                    else:
                        url = tr.td.a['href']
                if title.startswith('This') or title.startswith('Application'):
                    continue;
                if title.find('\n') != -1:
                   
                    title = title[0 : title.find('\n')].strip()
                self.count += 1
                self.write_db(f, "sr-projects-" + str(self.count), title, url)
                print title
                if title.startswith('Windows'):
                    break;
        for li in soup.find_all('li'):
            if li.a != None and li.a.span != None:
                continue
            title = li.text.strip().replace('\n', '')
            url = ''
            if li.a != None:
                if li.a['href'].startswith('http') == False:
                    url = "https://en.wikipedia.org" + li.a['href']
                else:
                    url = li.a['href']
            if title.find("—") != -1:
                title = title[0 : title.find("—")].strip()
            if title.find(" – ") != -1:
                title = title[0 : title.find(" – ")].strip()
            if title.find(" - ") != -1:
                title = title[0 : title.find(" - ")].strip()
            if title.find("(") != -1:
                title = title[0 : title.find("(")].strip()
            if title.find("[") != -1:
                title = title[0 : title.find("[")].strip()
            if len(title) > 20:
                title = title[0 : 25] + "..."
            print title
            self.count += 1
            self.write_db(f, "sr-projects-" + str(self.count), title, url)
            if title.startswith('Yap Speech'):
                break
            title = ''

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def getSocialRobotProjects(self):
        r = requests.get('https://en.wikipedia.org/wiki/Social_robot')
        soup = BeautifulSoup(r.text)
        start = False
        end = False

        file_name = self.get_file_name("projects/SOCIAL-ROBOT", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for a in soup.find_all('a'):
             if a.text.startswith('iCat'):
                 start = True
             if a.text.startswith('Haapie'):
                 end = True
             if start:
                 print a.text
                 self.count += 1
                 link = a['href']
                 if link.startswith('http') == False:
                     link = 'https://en.wikipedia.org' + link
                 self.write_db(f, 'social-robot-project-' + str(self.count), a.text, link)
             if end:
                 break
        self.count += 1
        self.write_db(f, 'social-robot-project-' + str(self.count), 'kismet','https://en.wikipedia.org/wiki/Kismet_(robot)')
        self.count += 1
        self.write_db(f, 'social-robot-project-' + str(self.count), 'jibo', 'https://www.jibo.com/')
        self.count += 1
        self.write_db(f, 'social-robot-project-' + str(self.count), 'pepper', 'https://www.aldebaran.com/en/a-robots/who-is-pepper')
        self.count += 1
        self.write_db(f, 'social-robot-project-' + str(self.count), 'NAO', 'https://www.aldebaran.com/en/humanoid-robot/nao-robot')
        self.count += 1
        self.write_db(f, 'social-robot-project-' + str(self.count), 'AIBO', 'https://en.wikipedia.org/wiki/AIBO')
        self.count += 1
        self.write_db(f, 'social-robot-project-' + str(self.count), 'furby', 'http://www.hasbro.com/en-us/brands/furby')
        self.count += 1
        self.write_db(f, 'social-robot-project-' + str(self.count), 'PaPeRo', 'https://en.wikipedia.org/wiki/PaPeRo')
        self.count += 1
        self.write_db(f, 'social-robot-project-' + str(self.count), 'kibo', 'http://kibo-robo.jp/en/')
        self.count += 1
        self.write_db(f, 'social-robot-project-' + str(self.count), 'rapiro', 'http://www.rapiro.com/') 
        self.count += 1
        self.write_db(f, 'social-robot-project-' + str(self.count), 'buddy', 'https://www.indiegogo.com/projects/buddy-your-family-s-companion-robot#/story')
        self.count += 1
        self.write_db(f, 'social-robot-project-' + str(self.count), 'joe robot', 'https://en.wikipedia.org/wiki/Joe_Robot')

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def getMitMediaProjects(self):
        r = requests.get('https://www.media.mit.edu/research/groups-projects')
        soup = BeautifulSoup(r.text)
        for span in soup.find_all('span', class_='field-content'):
            if span.a != None and span.a.text.startswith('more') == False:
                subject = span.a.text.strip().lower().replace(' ', '-')
                print subject
                file_name = self.get_file_name("projects/MIT-MEDIA-LAB/" + subject, self.school)
                file_lines = self.countFileLineNum(file_name)
                f = self.open_db(file_name + ".tmp")
                self.count = 0
 
                r = requests.get('https://www.media.mit.edu' + span.a['href'])
                sp = BeautifulSoup(r.text)
                for li in sp.find_all('li'):
                    if li.div != None and li.div.h2 != None:
                        link = ''
                        title = ''
                        desc = ''
                        sp1 = BeautifulSoup(li.div.prettify())
                        for a in sp1.find_all('a'):
                            if a.text.strip() == 'view site':
                                link = a['href']
                        title = li.div.h2.text.strip()
                        print title
                        desc = 'description:' + self.utils.removeDoubleSpace(li.div.div.text.strip().replace('\n', ''))
                        self.count += 1
                        self.write_db(f, "mit-media-" + subject + '-' + str(self.count), title, link, desc)
                self.close_db(f)
                if file_lines != self.count and self.count > 0:
                    self.do_upgrade_db(file_name)
                    print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
                else:
                    self.cancel_upgrade(file_name)
                    print "no need upgrade\n"

    def getOpenSourceRobotProjects(self):
        r = requests.get('https://en.wikipedia.org/wiki/Open-source_robotics')
        soup = BeautifulSoup(r.text)
        soup = BeautifulSoup(soup.find('table', class_='wikitable').prettify())

        file_name = self.get_file_name("eecs/projects/" + "open-source-robot", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for a in soup.find_all('a'):
            title = self.utils.removeDoubleSpace(a.text.strip().replace('\n', ''))
            if title.startswith('[') or title == 'Arduino' or title == 'Self-balancing robot' or title == 'Modular design':
                continue
            print title
            self.count += 1
            self.write_db(f, "open-source-robot-project-" + str(self.count), title, 'https://en.wikipedia.org' + a['href'])

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"
           
    def getSRIProject(self):
        r = requests.get("http://www.sri.com/work/projects")
        soup = BeautifulSoup(r.text)
        for a in soup.find_all('a'):
            if a['href'].startswith('/work/projects/'):
                if a.parent != None and a.parent.prettify().startswith('<span'):
                    subject = a.text.replace(' ', '-')
                    file_name = self.get_file_name(self.school + "/SRI/" + subject, self.school)
                    file_lines = self.countFileLineNum(file_name)
                    f = self.open_db(file_name + ".tmp")
                    self.count = 0
                    r2 = requests.get('http://www.sri.com' + a['href'])
                    soup2 = BeautifulSoup(r2.text)
                    for div in soup2.find_all('div', class_='events_inner'):
                        soup3 = BeautifulSoup(div.prettify())
                        title = soup3.find('div', class_='events_inner_title').text.strip()
                        link = 'http://www.sri.com' + soup3.find('div', class_='events_inner_title').a['href']
                        desc = 'description:' + soup3.find('div', class_='events_inner_teaser').text.strip()
                        print title
                        self.count += 1
                        self.write_db(f, 'sri-project-' + str(self.count), title, link, desc)
                    self.close_db(f)
                    if file_lines != self.count and self.count > 0:
                        self.do_upgrade_db(file_name)
                        print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
                    else:
                        self.cancel_upgrade(file_name)
                        print "no need upgrade\n"    


    def getAICProjects(self):
        r = requests.get('http://www.ai.sri.com/project_list/mode=All&sort=titleAsc')
        soup = BeautifulSoup(r.text)
        pages = 0

        file_name = self.get_file_name("eecs/" + self.school + "/" + "AIC", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for a in soup.find_all('a'):
            if a.text.strip() == 'End':
                pages = int(a['href'][len(a['href']) - 1 : ])

        for page in range(0, pages + 1):
            r2 = requests.get('http://www.ai.sri.com/project_list/mode=All&sort=titleAsc&page=' + str(page))
            soup2 = BeautifulSoup(r2.text)
            for td in soup2.find_all('td', class_='project'):
                if td.h2 != None:
                    title = td.h2.a.text
                    desc = "description:" + self.utils.removeDoubleSpace(td.p.text.replace('\n',''))
                    print title
                    self.count += 1
                    self.write_db(f, 'aic-project-' + str(self.count), title, 'http://www.ai.sri.com' + td.h2.a['href'], desc)
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"


    def getMicrosoftResearch(self):
        file_name = self.get_file_name("eecs/" + self.school + "/" + "microsoft-research", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
        for page in range(1, 13):
            r = requests.get("http://research.microsoft.com/apps/catalog/default.aspx?p=" + str(page) + "&sb=no&ps=100&t=projects&sf=&s=&r=&vr=&ra=")
            soup = BeautifulSoup(r.text)
            for div in soup.find_all('div', class_='l'):
                sp = BeautifulSoup(div.prettify())
                name_div = sp.find('div', class_='name')
                desc_div = sp.find('div', class_='desc')
                title = name_div.a.text.strip()
                desc = "description:" + self.utils.removeDoubleSpace(desc_div.text.strip().replace('\n', ''))
                print title
                self.count += 1
                self.write_db(f, 'ms-research-' + str(self.count), title, 'http://research.microsoft.com' + name_div.a['href'], desc)
               
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"
        
    def getDotNetFoundationProjects(self):
        r = requests.get("http://www.dotnetfoundation.org/projects")
        soup = BeautifulSoup(r.text)

        file_name = self.get_file_name("eecs/" + self.school + "/" + "DotNetFoundation", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for td in soup.find_all("td", class_="project-cell"):
            link = "http://www.dotnetfoundation.org" + td.div.span.a['href']
            title = td.text.strip()
            self.count += 1
            self.write_db(f, 'DotNetFoundation-project-' + str(self.count), title, link, '')

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def getDARPAWikiProjects(self):
        r = requests.get("https://en.wikipedia.org/wiki/DARPA")
        soup = BeautifulSoup(r.text)
        start = False
        end = False

        file_name = self.get_file_name("projects/" + "DARPA-WIKI", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for li in soup.find_all("li"):
            if li.a != None:
                if li.a.text == "4MM":
                    start = True
                if li.a.text == "Project Vela":
                    end = True
            if start:
                title = li.text.strip()
                desc = ""
                link = ""
                if li.a != None:
                    link = "https://en.wikipedia.org" + li.a['href']
                if title.find(':') != -1:
                    desc = "description:" + title[title.find(':') + 1 :].strip()
                    title = title[0 : title.find(':')]
                print title
                self.count += 1
                self.write_db(f, "darpa-wiki-project-" + str(self.count), title, link, desc)

            if end:
                break

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def getAIProjects(self):
        r = requests.get("https://en.wikipedia.org/wiki/List_of_artificial_intelligence_projects")
        soup = BeautifulSoup(r.text)
        start = False
        end = False

        file_name = self.get_file_name("eecs/" + self.school + "/" + "ai", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for li in soup.find_all("li"):
            if li.a != None:
                if li.a.text == "aHuman Project":
                    start = True
                if li.a.text == "Watson":
                    end = True
            if start:
                title = li.text.strip()
                desc = ""
                link = ""
                if li.a != None:
                    link = "https://en.wikipedia.org" + li.a['href']
                if title.find(',') != -1:
                    desc = "description:" + title[title.find(',') + 1 :].strip()
                    title = title[0 : title.find(',')]
                print title
                self.count += 1
                self.write_db(f, "ai-project-" + str(self.count), title, link, desc)

            if end:
                break

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"


    def getDARPAOpenProjects(self):
        #r = requests.get("https://en.wikipedia.org/wiki/DARPA")
        f = open("index.html", "r")
        html = f.read()
        soup = BeautifulSoup(html)
        file_name = self.get_file_name(self.school + "/" + "DARPA-open", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for tr in soup.find_all('tr'):
            sp = BeautifulSoup(tr.prettify())
            count = 0
            title = ""
            desc = "description:"
            for line in tr.text.split("\n"):
                line = line.strip()
                if line == "":
                    continue
                count += 1
                if count == 1:
                    title = line
                else:
                    desc += line + " "
            if title == "DARPA Program":
                continue
            print title
            self.count += 1
            self.write_db(f, "darpa-open-project-" + str(self.count), title, "", desc)
                

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def getDARPAProjects(self):
        #r = requests.get("https://en.wikipedia.org/wiki/DARPA")
        f = open("2.htm", "r")
        html = f.read()
        soup = BeautifulSoup(html)
        file_name = self.get_file_name(self.school + "/" + "DARPA-history", self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for div in soup.find_all('div', class_='listing__right'):
            title = div.div.text + " " + div.h2.a.text
            #desc = "description:" + div.div.text.replace("\n", "")
            print title
            self.count += 1
            self.write_db(f, "darpa-history-project-" + str(self.count), title, div.h2.a['href'], "")

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"
start = ProjectsSpider()
start.doWork()
