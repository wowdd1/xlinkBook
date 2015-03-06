#!/usr/bin/env python


from spider import *

class ClassCentralSpider(Spider):

    def __init__(self):
        Spider.__init__(self)
        self.school = 'class_central'
        self.base_url = 'https://www.class-central.com'

    def processSubject(self, subject, sub_subject, url):
        print 'process ' + sub_subject
        file_name = self.get_file_name(subject + '/' + self.school + '/' + sub_subject, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        page = '1'
        while True:
            next_url = url + '?sort=rating-up&page=' + page
             
            print 'process ' + next_url
            r = requests.get(next_url)
            jobj = json.loads(r.text)

            soup = BeautifulSoup(jobj['table'])
            for tr in soup.find_all('tr'):
                if tr.attrs.has_key('itemtype'):
                    sp = BeautifulSoup(tr.prettify())
                    link = sp.find('a', class_='course-name')
                    name = link.text.strip()
                    self.count += 1
                    num = 'cc-' + url[url.find('subject/') + 8 :] + '-' + str(self.count)
                    print num + ' ' + name 
                    self.write_db(f, num, name, self.base_url + link['href'])
            next_div = soup.find('div', id='show-more-courses')
            if next_div == None or (next_div != None and next_div['style'].find('display: none') != -1):
                break
            page = next_div['data-page']
                
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n" 

    def doWork(self):
        r = requests.get('https://www.class-central.com/')
        soup = BeautifulSoup(r.text)
        for div in soup.find_all('div', class_='single-category col-xs-6 col-md-4'):
            subject = div.div.a.text.strip()
            if self.need_update_subject(subject):
                if div.ul != None:
                    sp = BeautifulSoup(div.prettify())
                    for li in sp.find_all('li'):
                        self.processSubject(subject, li.text.strip(), self.base_url + '/maestro' + li.a['href'])
                else:
                    self.processSubject(subject, subject, self.base_url + '/maestro' + div.div.a['href'])

start = ClassCentralSpider()
start.doWork()
