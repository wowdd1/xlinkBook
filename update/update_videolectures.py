#!/usr/bin/env python

from spider import *
import re
sys.path.append("..")
from record import Record

class VideolecturesSpider(Spider):

    def __init__(self):
        Spider.__init__(self)
        self.school = 'videolectures'
        self.type_map = {'Lecture ' : 'vl',\
                         'Tutorial' : 'vtt',\
                         'Keynote' : 'vkn',\
                         'Interview' : 'viv',\
                         'Other' : '__'}
        self.subject_cid_map = {'Machine Learning' : '16',\
                                'Data Mining' : '36',\
                                'Computer Vision' : '71',\
                                'Network Analysis' : '28',\
                                'Data Visualisation' : '41',\
                                'Natural Language Processing' : '144',\
                                'Pattern Recognition' : '395',\
                                'Text Mining' : '37',\
                                'Web Mining' : '127',\
                                'Robotics' : '69',\
                                'Artificial Intelligence' : '136',\
                                'Big Data' : '602',\
                                'Semantic Web' : '27',\
                                'Web Search' : '163',\
                                'Optimization Methods' : '232'}
    def findLastPage(self, soup):
        max_page = 1
        for a in soup.find_all('a'):
            if a.text == ' Last ':
                max_page = int(a['href'][a['href'].find('(') + 1 : a['href'].find(')')])
                break
        return max_page

    def processEventData(self, subject):
        r = requests.get('http://videolectures.net/site/ajax/drilldown/?t=evt&cid=13&w=5')
        soup = BeautifulSoup(r.text)
        max_page = self.findLastPage(soup)

        file_name = self.get_file_name('eecs/' + self.school + '/' + subject, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
        urls_list = []

        for page in range(1, max_page + 1):
            r = requests.get('http://videolectures.net/site/ajax/drilldown/?o=top&t=evt&p=' + str(page) + '&cid=13&w=5')
            soup = BeautifulSoup(r.text)
            for a in soup.find_all('a'):
                if a.attrs.has_key('lang'):
                    urls_list.append('http://videolectures.net' + a['href'])        
            i = 0
            title = ''
            desc = ''
            for span in soup.find_all('span'):
                i += 1
                if i == 1:
                    print title
                    title = span.text.strip()
                if i == 2:
                    desc = 'description:' + span.text.strip() + ' '
                if i == 3:
                    desc += span.text.strip()
                    self.count += 1
                    self.write_db(f, subject + '-' + str(self.count), title, urls_list[self.count - 1], desc)
                    i = 0

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def processData(self, subject):
        file_name = self.get_file_name('eecs/' + self.school + '/' + subject, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
 
        print 'processing ' + subject
        for s in self.type_map.keys():
            r = requests.get('http://videolectures.net/site/ajax/drilldown/?t=' + self.type_map.get(s) + '&cid=' + self.subject_cid_map.get(subject) + '&w=5')
            soup = BeautifulSoup(r.text)
            max_page = self.findLastPage(soup)

            for page in range(1, max_page + 1):
                r = requests.get('http://videolectures.net/site/ajax/drilldown/?o=top&t=' + self.type_map.get(s) + '&p=' + str(page) + '&cid=' + self.subject_cid_map.get(subject) + '&w=5')
                soup = BeautifulSoup(r.text)
                for div in soup.find_all('div', class_='lec_thumb'):
                    instructors = ''
                    title = div.a.span.span.text.strip()        
                    url = 'http://videolectures.net' + div.a['href']
                    soup1 = BeautifulSoup(div.prettify())
                    div = soup1.find('div', class_='author')
                    if div != None and div.span != None:
                        instructors = 'instructors:' + div.span.text.strip()
                    self.count += 1
                    vl_num = 'vl-' + str(self.subject_cid_map.get(subject)) + '-' + str(self.count)
                    print vl_num + ' ' + title
                    self.write_db(f, vl_num, title, url, instructors)

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def upFirstChar(self, text):
        result = ''
        for i in range(0, len(text)):
            if (i > 0 and text[i - 1] == ' ') or i == 0:
                result += str(text[i]).upper()
            else:
                result += text[i]

        return result.strip()

    def getNameAndDescription(self, url):
        name = ''
        homepage = ''
        desc = ''
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        span_name = soup.find('span', class_='auth_name')
        span_desc = soup.find("span", id="auth_desc_edit")

        if span_name != None and span_name.a != None:
            name = span_name.a.text.replace('  ',' ').strip()
            homepage = span_name.a['href']
            desc += 'homepage:' + homepage + ' '

        if span_desc != None:
            desc += 'description:' + span_desc.text.replace('\n', ' ').strip()

        return name, desc
            
         
        
    def processUserData(self):
        print 'processing user data'
        file_name = self.get_file_name('eecs/' + self.school + '/user', self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
        user_dict= {}

        for page in range(1, 24):
            r = requests.get('http://videolectures.net/site/list/authors/?page=' + str(page))
            soup = BeautifulSoup(r.text)
            for tr in soup.find_all('tr'):
                if tr.text.find('Author') == -1:
                    soup1 = BeautifulSoup(tr.prettify())
                    video_pos = tr.text.find('video')
                    views_pos = tr.text.find('views')
                    url = 'http://videolectures.net' + soup1.find('a')['href']
                    desc = ''
                    vl_id = ''
                    title = self.upFirstChar(soup1.find('a')['href'][1:].replace('/','').replace('_', ' '))
                    self.count += 1
                    if tr.text.find('videos') != -1:
                        vl_id = str(tr.text[video_pos + 6 : views_pos].strip()) + '-' + str(self.count)
                    else:
                        vl_id = str(tr.text[video_pos + 5 : views_pos].strip()) + '-' + str(self.count)
                    desc = 'organization:' + tr.text[views_pos + 5 :]

                    if views_pos == -1:
                        vl_id = '0' + '-' + str(self.count)
                        desc = 'organization:' + tr.text[video_pos + 5 :]
                    print vl_id + ' ' + title
                    user_dict[vl_id] = Record(self.get_storage_format(vl_id, title, url, desc))
        self.count = 0
        for item in sorted(user_dict.items(), key=lambda user_dict:int(user_dict[1].get_id()[0 : user_dict[1].get_id().find('-')].strip()), reverse=True):
            self.count += 1
            name = ''
            desc = ''
            if self.count <= 100 and item[1].get_url().strip().startswith('http'):
                name, desc = self.getNameAndDescription(item[1].get_url().strip()) 
            uid = 'vl-' + item[1].get_id()[0 : item[1].get_id().find('-')] + '-' + str(self.count)
            if name == '':
                name = item[1].get_title().strip()
            #print uid + ' ' + name
            self.write_db(f, uid, name, item[1].get_url().strip(), item[1].get_describe().strip() + ' ' + desc)
            
                 
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def doWork(self):
        self.processEventData('event')
        for subject in self.subject_cid_map.keys():
            self.processData(subject)
        self.processUserData()


start = VideolecturesSpider()
start.doWork()

