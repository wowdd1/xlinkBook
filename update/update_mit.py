#!/usr/bin/env python
    
#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07
from spider import *
from update_mit_ocw import MitOcwSpider
sys.path.append("..")
from utils import Utils

class MitSpider(Spider):
    ocw_links = {}
    course_num_regex = re.compile(r'[0-9]+\.[0-9]+[a-z]*')
 
    def __init__(self):
        Spider.__init__(self)    
        self.school = "mit"
        self.ocw_spider = MitOcwSpider()
        self.deep_mind = True
   
    def initOcwLinks(self, subject):
        self.ocw_links = self.ocw_spider.getOcwLinks(subject)

    def getTextBook(self, course_num):
        terms = ['2014SP', '2013SP', '2012SP']
        for term in terms:
            r = requests.get('http://eduapps.mit.edu/textbook/books.html?Term=' + term + '&Subject=' + course_num)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text)
                table = soup.find('table', class_='displayTable')
                if table == None:
                    continue
                splits = table.text.strip()[table.text.strip().find('Price') + 6 :].strip().split('\n')
                if splits[0] == 'Course Has No Materials':
                    continue
                return 'textbook:' + splits[1] + ' (' + splits[0] + ')' + ' '
        return ''

    def getMitCourseLink(self, links, course_num):
        if course_num == "":
            return course_num
        if self.ocw_links.get(course_num, '') != '':
            return self.ocw_links[course_num]

        for link in links:
            if link.attrs.has_key("href") and link["href"].find(course_num) != -1 and link["href"].find("editcookie.cgi") == -1:
                return link["href"]
        return ""
    
    def processMitData(self, html, f, course_code):
        #print html
        soup = BeautifulSoup(html);
        links_all = soup.find_all("a")
        course_links = []
        utils = Utils()
        for link in links_all:
            if link.attrs.has_key("href") and False == link["href"].startswith("editcookie.cgi") \
               and False == link["href"].startswith("/ent/cgi-bin") and False == link["href"].startswith("javascript:") \
               and False == link["href"].startswith("m"):
                course_links.append(link)
        course_num = ""
        title = ""
        link = ""
        textbook = ''
        prereq = ''
        instructors = ''
        for line in html.split("\n"):

            if (line.strip().startswith('<br>') and utils.clearHtmlTag(line.strip())[1 : 2] == '.') or \
                line.find('Prereq:') != -1:
                if line.find('Prereq:') != -1:
                    all_prereq = self.course_num_regex.findall(line.lower())
                    all_prereq = list(set(all_prereq))
                    for p in all_prereq:
                        prereq += p + ' '
                    if len(all_prereq) > 0:
                        prereq = 'prereq:' + prereq
                    #print course_num + '---->' + prereq
                        
                if line.strip().startswith('<') and utils.clearHtmlTag(line.strip())[1 : 2] == '.':
                    instructors = 'instructors:' + utils.clearHtmlTag(line.strip()[0 : line.strip().find('</')]) + ' '

            if line.strip().find('<h3>') != -1 or \
                (line.strip().startswith('<br>') and (line.strip()[len(line.strip()) - 1 : ] == '.' or line.strip()[len(line.strip()) - 7 : ] == 'limited')):
                line = line[line.find('>', 3) + 1 : ]
                if line.find('</h3>') == -1:
                    #print line
                    if line[0 : line.find('.')] == course_code:
                        if course_num != '':
                            print course_num + " " + title + " " + link                     

                            if instructors != '' and remark.find('instructors:') == -1:
                                remark = instructors + ' ' + remark

                            self.count += 1
                            self.write_db(f, course_num, title, link, remark)
                            remark = ''
                            course_num = ""
                            title = ""
                            link = ""
                            textbook = ''
                            prereq = ''
                            instructors = ''

                        course_num = line.strip()[0 : line.strip().find(" ")]
                        textbook = ''
                        if self.deep_mind:
                            textbook = self.getTextBook(course_num)

                        if textbook == '' and self.deep_mind and self.ocw_links.get(course_num, '') != '':
                            textbook = self.ocw_spider.getTextBook(self.ocw_links[course_num], course_num)
 
                        title = line.strip()[line.strip().find(" ") + 1 : ]
                        if course_num.find(',') != -1:
                            course_num = line.strip()[0 : line.strip().find(" ", line.strip().find(" ") + 1)]
                            title = line.strip()[line.strip().find(" ", line.strip().find(" ") + 1) + 1 : ]
                        link = self.getMitCourseLink(course_links, course_num.strip())
                    else:
                        remark = ''
                        if self.deep_mind and self.ocw_links.get(course_num, '') != '':
                            remark = self.ocw_spider.getDescription(self.ocw_spider.getDescriptionApiUrl(self.ocw_links[course_num]))
                            if remark.find('description:') != -1:
                                remark = remark[0 : remark.find('description:')]

                        if textbook != '':
                            remark += textbook
                        if prereq != '':
                            remark += prereq

                        remark += 'description:' + line.strip() + ' ' 
        if course_num != '':
            self.count = self.count + 1
            self.write_db(f, course_num, title, link, remark)

    def doWork(self):
        #mit
        #"""
        r = requests.get('http://student.mit.edu/catalog/index.cgi')
        soup = BeautifulSoup(r.text);
        for a in soup.find_all('a'):
            if a['href'].find('http') == -1 and a['href'][0 : 1] == 'm' and a['href'][0 : 4] != 'mail':
                subject = a.text
                if subject.find('-') != -1:
                    subject = subject[subject.find('-') + 1 : ]
                if subject.find('(') != -1:
                    subject = subject[0 : subject.find('(')]
                subject = subject.strip()
                if self.need_update_subject(subject) == False:
                    continue 
        
                print 'init ocw course links'
                self.initOcwLinks(subject)


                print "downloading mit course info"
                file_name = self.get_file_name(subject, self.school)
                file_lines = self.countFileLineNum(file_name)
                f = self.open_db(file_name + ".tmp")
                self.count = 0
                print 'processing ' + a['href'] 
                r = requests.get("http://student.mit.edu/catalog/" + a['href'])
                print "processing html and write data to file..."
                course_code = a['href'][1 : a['href'].find('.html') - 1]
                #print 'course_code: ' + course_code
                self.processMitData(r.text, f, course_code)

                soup = BeautifulSoup(r.text);
                regex = re.compile(a['href'][0 : a['href'].find('.html') - 1] + '[b-z].html')
                for link in sorted(list(set(regex.findall(r.text)))):
                    print 'processing ' + link
                    r = requests.get("http://student.mit.edu/catalog/" + link)
                    self.processMitData(r.text, f, course_code) 
     
    
                self.close_db(f)
                if file_lines != self.count and self.count > 0:
                    self.do_upgrade_db(file_name)
                    print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
                else:
                    self.cancel_upgrade(file_name)
                    print "no need upgrade\n"
            #"""
   
start = MitSpider()
start.doWork() 
