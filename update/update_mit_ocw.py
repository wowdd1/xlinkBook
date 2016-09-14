#!/usr/bin/env python
    
#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07
    
from spider import *
import time

class MitOcwSpider(Spider):

    def __init__(self):
        Spider.__init__(self)    
        self.school = "mit-ocw"
        self.url = "http://ocw.mit.edu"
    #ocw
    #"""

    def getTextBookFormHtml(self, html):
        soup = BeautifulSoup(html)
        result = ''
        for p in soup.find_all('p'):
            if p.text.lower().find('isbn:') != -1:
                result += 'textbook:' + p.text.strip()[0 : p.text.strip().lower().find('isbn:') - 1].replace('\n', '').strip() + ' ' 
        return result

    def getTextBook(self, url, course_num):
        r = requests.get(url + '/readings/')
        if r.status_code != 404:
            return self.getTextBookFormHtml(r.text)
        r = requests.get(url + '/syllabus/')
        if r.status_code != 404:
            return self.getTextBookFormHtml(r.text) 
        return ''

    def getDescription(self, url):
        r = requests.get(url)
        jobj = None
        try:
            jobj = json.loads(r.text)
        except Exception as e:
            return ''
        return 'level:' + jobj['level'] + ' instructors:' + jobj['instructors'].replace('Prof.','').strip() + \
                  ' term:' + jobj['sem'] + ' features:' + jobj['features'] + ' description:' + re.sub(r'[\x00-\x1f]', '', jobj['description'].replace('\n', ''))

    def getDescription2(self, url):
        r = requests.get(url)
	if r.text != None and r.text != '':
            jobj = json.loads(r.text)
            return 'level:' + jobj['level'] + ' features:' + jobj['features']
        else:
	    return ''

    def getOcwLinks(selfi, subject):
        ocw_links = {}
        url = ('http://ocw.mit.edu/courses/' + subject.strip().replace(' ', '-')).replace(',', '').lower()
        print 'getOcwLinks in MitOcwSpider, url:' + url
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        i = 0
        course_num = ''
        link = ''
        for a in soup.find_all("a", class_="preview"):
            i = i + 1
            if i == 1:
                course_num = a.string.replace("\n", "").strip()
                link = 'http://ocw.mit.edu' + str(a["href"])
                if ocw_links.get(course_num, '') == '':
                    ocw_links[course_num] = link
            if i >= 3:
                i = 0
        return ocw_links
 
    def getDescriptionApiUrl(self, url):
        return url + '/index.json?' + str(time.time()).replace('.', '')

    def getMitOcwCourse(self, subject, url):
        if self.need_update_subject(subject) == False:
            return
        print "processing " + subject + " url " + url
        file_name = self.get_file_name(subject, self.school)
    
        file_lines = self.countFileLineNum(file_name)
        count = 0
        f = self.open_db(file_name + ".tmp")
    
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        course_num = ""
        title = ""
        link = ""
        description = ""
        i = 0
        print "processing html and write data to file..."
        for a in soup.find_all("a", class_="preview"):
            i = i + 1
            if i == 1:
                course_num = a.string.replace("\n", "").strip()
                link = self.url + str(a["href"])
                description = ''
                book = self.getTextBook(link, course_num)
                if book != '':
                    description += book

                description +=  self.getDescription(self.getDescriptionApiUrl(link))
                
            if i == 2:
                title = a.string.replace("\n", "").replace("               ", "").strip()
                count = count + 1
                print course_num + ' ' + title + ' ' + link
                self.write_db(f, course_num, title, link, description)
    
                link = ''
                title = ''
                course_num = ''
                description = ''
            if i >= 3:
                i = 0
    
        self.close_db(f)
        if file_lines != count and count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"
    
    def doWork(self):
        print "downloading ocw course info"
        #r = requests.get("http://ocw.mit.edu/courses/electrical-engineering-and-computer-science/")
        r = requests.get("http://ocw.mit.edu/courses/find-by-department")
        soup = BeautifulSoup(r.text);
    
    
        for li in soup.find_all("li"):
            if li.a != None and str(li.a["href"]).startswith("/courses") and str(li.a["href"]).find("find") == -1:
                subject = str(li.a.string).strip()
                if subject.startswith("Audio") or subject.startswith("Find") or subject.startswith("Online Textbooks") \
                    or subject.startswith("New Courses") or subject.startswith("Most Visited Courses") or subject.startswith("OCW Scholar Courses") \
                    or subject.startswith("This Course at MIT") or subject.startswith("Translated Courses"):
                    continue;
                self.getMitOcwCourse(subject, self.url + str(li.a["href"]).strip())
                #print li.a.string
def main(argv):    
    start = MitOcwSpider();
    start.doWork()

if __name__ == '__main__':
    main(sys.argv)
