#! /usr/bin/env python

from spider import *

class MicrosoftAcademicSearchSpider(Spider):
    def __init__(self):
        Spider.__init__(self)
        self.school = 'mas'
        self.subject = 'rank'
        self.base_url = 'http://academic.research.microsoft.com'

    def processSubType(self, subject, url):
        print 'processing ' + subject
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        entitytype_dict = {}
        for li in soup.find_all('li'):
            if li.a != None and li.a.attrs.has_key("entitytype"):
                #if li.a['entitytype'] == '1' or li.a['entitytype'] == '2':
                if li.a['entitytype'] == '3' or li.a['entitytype'] == '4':
                    entitytype_dict[li.a['entitytype']] = li.a.text.strip().lower()

        for li in soup.find_all('li'):
            if li.a != None and li.a.attrs.has_key("href") and li.a['href'].startswith('/?SearchDomain='):
                print 'processing ' + li.a.text

                arg_list = li.a['href'].split('&')
                top_domain_id = arg_list[0][arg_list[0].find('=') + 1 : ]
                sub_domain_id = arg_list[1][arg_list[1].find('=') + 1 : ]
                for entitytype in entitytype_dict.keys():
                    file_name = self.get_file_name(self.subject + '/' + self.school + '/'+ li.a.text.lower() + '-' + entitytype_dict.get(entitytype), self.school)
                    file_lines = self.countFileLineNum(file_name)
                    f = self.open_db(file_name + ".tmp")
                    self.count = 0

                    url = self.base_url + '/RankList?entitytype=' + entitytype + '&topDomainID=' + top_domain_id + '&subDomainID='\
                                   + sub_domain_id + '&last=0&start=1&end=100' 
                    print 'processing ' + entitytype_dict.get(entitytype) + ' ' + url
                    r = requests.get(url)
                    sp = BeautifulSoup(r.text)
                    r_id = ''
                    title = ''
                    url = ''
                    desc = ''
                    if entitytype == '2':
                        for div in sp.find_all('div', class_='content-narrow'):
                            sp1 = BeautifulSoup(div.prettify())
                            div = sp1.find('div', class_='title')
                            title = div.h3.a.text.strip()
                            url = div.h3.a['href']
                            div = sp1.find('div', 'inline-text')
                            if div != None:
                                desc = 'organization:' + div.a.text.strip()
                            self.count += 1
                            r_id = 'mas-' + entitytype_dict.get(entitytype)[0 : 1].lower() + '-' + str(top_domain_id) + '-' + str(sub_domain_id) + '-' +str(self.count)
                            print r_id + ' ' + title
                            self.write_db(f, r_id, title, url, desc)
                    else:
                        for td in sp.find_all('td', class_= 'rank-content'):
                            title = td.a.text
                            url = self.base_url + td.a['href']
                            self.count += 1
                            r_id = 'mas-' + entitytype_dict.get(entitytype)[0 : 1].lower() + '-' + str(top_domain_id) + '-' + str(sub_domain_id) + '-' + str(self.count)
                            print r_id + ' ' + title
                            self.write_db(f, r_id, title, url, desc)

                    self.close_db(f)
                    if file_lines != self.count and self.count > 0:
                        self.do_upgrade_db(file_name)
                        print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
                    else:
                        self.cancel_upgrade(file_name)
                        print "no need upgrade\n"                  

    def processOrganizations(self, subject, top_domain_id):
        print 'processing ' + subject
        url = self.base_url + '/RankList?entitytype=7&topDomainID=' + top_domain_id + '&subDomainID=0&last=0&start=1&end=100' 
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        file_name = self.get_file_name(self.subject + '/' + self.school + '/'+ subject + '-organizations', self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for td in soup.find_all('td', class_= 'rank-content'):
            title = td.a.text
            url = self.base_url + td.a['href']
            self.count += 1
            r_id = 'mas-o-' + str(top_domain_id) + '-0' + '-' + str(self.count)
            print r_id + ' ' + title
            self.write_db(f, r_id, title, url) 

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def doWork(self):
        r = requests.get(self.base_url)
        soup = BeautifulSoup(r.text)
        for li in soup.find_all('li'):
            if li.a != None and li.a.attrs.has_key("href") and li.a['href'].startswith('/?SearchDomain='):
                if self.need_update_subject(li.a.text):
                    arg = li.a['href'].split('&')[0]
                    self.processOrganizations(li.a.text, arg[arg.find('=') + 1 : ])
                    self.processSubType(li.a.text, self.base_url + li.a['href'])                



start = MicrosoftAcademicSearchSpider()
start.doWork()
