#!/usr/bin/env python
    
#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07
    
from spider import *
from update_berkeley_webcast import BerkeleyWebcastSpider
from update_berkeley_catalog import BerkeleyCatalogSpider
sys.path.append("..")
from utils import Utils

py3k = sys.version_info[0] >= 3
if py3k:
    from html.parser import HTMLParser
else:
    from HTMLParser import HTMLParser

class TableHandler(HTMLParser):
    def __init__(self, **kwargs):
        HTMLParser.__init__(self)
        self.kwargs = kwargs
        self.active = None
        self.last_content = ""
        self.rows = []
        self.found_first_valid_num = False

    def handle_starttag(self,tag, attrs):
        self.active = tag

    def handle_endtag(self,tag):
        #if tag in ["th", "td"]:
        #    print self.last_content.strip()
        #if tag in ['tr']:
        #    self.last_content = " "

        self.active = None
    def valid_course_num(self, text):
        if text.find(' ') == -1 and text != '&' and text != 'Previous' and text != 'unknown' and text != 'Neural' and text != 'Mechatronics' and text != 'Cryptography':
            return True
        return False

    def handle_data(self, data):
        data = data.replace('\n', '').strip()
        if len(data) == 0 or data == '[' or data == ']' or data == 'archives':
            return

        if self.valid_course_num(data):
            if self.found_first_valid_num:
                #print self.last_content
                self.rows.append(self.last_content)
               
            if data[0 : 2] == 'CS': 
                self.found_first_valid_num = True
            self.last_content = ""
 
        #print data.strip()
        if data[0: 4] == 'Last':
            return
        if data.startswith('Previous') or data.startswith('non-EECS'):
            return

        self.last_content += data + ' '


class BerkeleyEECSSpider(Spider):

    def __init__(self):
        Spider.__init__(self)
        self.school = "berkeley"
        self.subject = "eecs"
        self.deep_mind = True
        self.berkeleyWebcastSpider = BerkeleyWebcastSpider()
        self.berkeleyCatalogSpider = BerkeleyCatalogSpider()
        self.utils = Utils()

    def getLink(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        links = []
        for a in soup.find_all('a'):
            if a['href'][0 : 2] == './':
                links.append(url.replace('archives.html', '') + a['href'][2:])
        return links[len(links) - 1]
    
    def processBerkeleyData(self, f, tr):
        if self.need_update_subject(self.subject) == False:
            return
        i = 0
        title = ""
        link = ""
        for td in tr.children:
           if i == 3:
               title = title + td.a.string + " "
           if i == 5:
               title = title + td.u.string
               link = "http://www-inst.eecs.berkeley.edu" + td.a["href"]
               link = self.getLink(link)
           i = i + 1
        if i > 4:
            self.count = self.count + 1
            self.write_db(f, title[0:title.find(" ")], title[title.find(" "):], link)

    def genUrl(self, course_num):
        return 'http://www-inst.eecs.berkeley.edu/~' + course_num.lower() + '/archives.html'    

    def getRealUrl(self, url):
        r = None
        try:
            r = requests.get(url)
        except Exception , e:
            print e
            return url
        soup = BeautifulSoup(r.text)
        link_dict = {}
        for a in soup.find_all('a'):
            if a.attrs.get('href', '') != '' and a['href'][0 : 2] == './':
                key = a.text.strip().replace('Spring ', '').replace('Summer ', '').replace('Fall ', '').replace('Winter ', '')
                link_dict[key] = (url.replace('archives.html', '') + a['href'][2:])
        sorted_keys = sorted(link_dict)

        for i in range(len(sorted_keys) - 1, -1 , -1):
            test_url = link_dict[sorted_keys[i]]
            try:
                r = requests.get(test_url)
                if r.status_code == 200:
                    soup = BeautifulSoup(r.text)
                    for a in soup.find_all('a'):
                        if a.text.strip() == url:
                            #print test_url + ' not match'
                            break
                    #print 'match ' + test_url
                    return test_url
            except Exception , e:
                print e
        if len(sorted_keys) > 0:
            return link_dict[sorted_keys[len(sorted_keys) - 1]]
        else:
            return url

    def doWork(self):
        #berkeley
        #"""
        print "downloading berkeley course info"
        file_name = self.get_file_name(self.subject, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        r = requests.get("http://www-inst.eecs.berkeley.edu/classes-eecs.html")

        course_id = ''
        course_name = ''
        url = ''
        for item in r.text.split('\n'):
            if item.find('colspan') != -1:
                continue
            if item.find('<') == -1:
                continue

            if item.find('href') != -1 and item.find('html') == -1:
                course_id = self.utils.clearHtmlTag(item).strip()
                #url = item[item.find('/'): item.find('>', item.find('/')) - 1]
                url = self.genUrl(course_id)

                continue
            if course_id != '' and item.find('td') != -1 and item.find('html') == -1:
                course_name = self.utils.clearHtmlTag(item).strip()
                if course_name.find('(') != -1 and course_name.startswith('(') == False:
                    course_name = course_name[0 : course_name.find('(')].strip()
            #print item
            if item.find('/tr') != -1:
                if len(course_id) < 10:
                    print course_id
                    print course_name
                    print url
                    self.count += 1
                    self.write_db(f, course_id, course_name, url, '')

                course_id = ''
                course_name = ''
                url = ''

        soup = BeautifulSoup(r.text)
        parser = TableHandler()
        parser.feed(r.text)

    
        print "processing html and write data to file..."
        #'''
        for tr in soup.find_all("tr"):
            #tr =  table.tr
            #self.processBerkeleyData(f, tr)
    
            #for next_tr in tr.next_siblings:
            #    if next_tr.string == None:
            #        self.processBerkeleyData(f, next_tr)
            print tr.text
            #soup2 = BeautifulSoup(table.text)
            #print table.text
            #for tr in soup2.find_all('tr'):
            #    print tr.text
    
        '''
        print 'get webcast info...'
        webcast_dict = self.berkeleyWebcastSpider.getWebcastDict(['Computer Science', 'Electrical Engineering'])
        print 'get course dict from catalog...'
        course_dict = self.berkeleyCatalogSpider.getCourseDict(['Computer Science', 'Electrical Engineering'])
        for row in parser.rows:
            url = self.genUrl(row[0: row.find(" ")])
            print row 
            self.count = self.count + 1
            if self.deep_mind:
                url = self.getRealUrl(url)
            description = ''
            key = row[0:row.find(" ")]
            if webcast_dict.get(key , '') != '':
                if course_dict.get(key , '') != '' and course_dict[key].get_prereq() != None:
                    description = 'prereq:' + course_dict[key].get_prereq() + ' '
                description = 'instructors:' + webcast_dict[key].get_lecturer() + ' videourl:' + webcast_dict[key].get_youTube() + " " \
                               + description +  'term:' + webcast_dict[key].get_semester() \
                               + ' description:' + webcast_dict[key].get_descr()
            elif course_dict.get(key , '') != '':
                if course_dict[key].get_instructors() != None:
                    description += 'instructors:' + course_dict[key].get_instructors() + ' '
                if course_dict[key].get_prereq() != None:
                    description += 'prereq:' + course_dict[key].get_prereq() + ' '
                if course_dict[key].get_description() != None:
                    description += 'description:' + course_dict[key].get_description()
            self.write_db(f, row[0:row.find(" ")], row[row.find(" "):].strip(), url, description)

        '''
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"
    
start = BerkeleyEECSSpider();
start.doWork() 
