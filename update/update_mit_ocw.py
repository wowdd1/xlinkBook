#!/usr/bin/env python
    
#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07
    
from spider import *
import time

class MitOcwSpider(Spider):
    video_audio_dict = {}
    online_book_dict = {}

    def __init__(self):
        Spider.__init__(self)    
        self.school = "mit-ocw"
        self.url = "http://ocw.mit.edu"
    #ocw
    #"""
    
    def initDict(self, url, dict_arg):
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        course_num = ''
        link = ''
        i = 0
        for a in soup.find_all("a", class_="preview"):
            i = i + 1
            if i == 1:
                course_num = a.string.replace("\n", "").strip()
                link = self.url + str(a["href"])             
                dict_arg[course_num] = link
            if i >= 3:
                i = 0
                course_num = ''
                link = ''

    def existViewOrAudio(self, course_num):
        if self.video_audio_dict.get(course_num, '') != '':
            return True
        return False

    def existOnlineBook(self, course_num):
        if self.online_book_dict.get(course_num, '') != '':
            return True
        return False

    def getTextBookFormHtml(self, html):
        soup = BeautifulSoup(html)
        result = ''
        for p in soup.find_all('p'):
            if p.text.lower().find('isbn:') != -1:
                result += p.text.strip()[0 : p.text.strip().lower().find('isbn:') - 1].replace('\n', '').strip() + ' ' 
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
        jobj = json.loads(r.text)
        description = ''
        return 'level:' + jobj['level'] + ' instructors:' + jobj['instructors'] + ' description:' + re.sub(r'[\x00-\x1f]', '', jobj['description'].replace('\n', ''))
 
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
                if self.existViewOrAudio(course_num):
                    description += 'video:yes '
                if self.existOnlineBook(course_num):
                    description += 'onlinebook:yes '
                book = self.getTextBook(link, course_num)
                if book != '':
                    description += 'textbook:' + book

                description +=  self.getDescription(link + '/index.json?' + str(time.time()).replace('.', ''))
                
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
        print 'init video and book dict' 
        self.initDict('http://ocw.mit.edu/courses/audio-video-courses/', self.video_audio_dict)
        self.initDict('http://ocw.mit.edu/courses/online-textbooks/', self.online_book_dict)

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
    
start = MitOcwSpider();
start.doWork()
