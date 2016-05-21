#!/usr/bin/env python
# -*- coding: utf-8 -*-

from spider import *



class CSDNBlogSpider(Spider):

    def __init__(self):
        Spider.__init__(self)

        self.subject = 'eecs'
        

    def doWork(self):
        data = {'laoluo' : ['http://blog.csdn.net/luoshengyang', ['计划', '启动篇']]}

        for k, v in data.items():
            user_agent = {'User-agent': 'Mozilla/5.0'}
            r = requests.get(v[0], headers = user_agent)
            soup = BeautifulSoup(r.text)
      
            for a in soup.find_all('a'):
                if a.text == "尾页":
                    print a['href']
                    end = a['href']
                    while (end.find('/') != -1):
                        end = end[end.find('/') + 1 :].strip()
                    print end 
                    url = "http://blog.csdn.net" + a['href'][0 : len(a['href']) - len(end)]
                    print url
                    file_name = self.get_file_name(self.subject + "/android-laoluo", "csdn")
                    file_lines = self.countFileLineNum(file_name)
                    f = self.open_db(file_name + ".tmp")
                    self.count = 0
                    self.getPages(f, k, url, "1", end, v[1])

                    self.close_db(f)
                    if file_lines != self.count and self.count > 0:
                        self.do_upgrade_db(file_name)
                        print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
                    else:
                        self.cancel_upgrade(file_name)
                        print "no need upgrade\n"

    def getPages(self, f, rID, url, start, end, keys=[]):
        parentID = ''
        for page in list(reversed(range(int(start), int(end) + 1))):
            #print str(page)
            user_agent = {'User-agent': 'Mozilla/5.0'}
            r = requests.get(url + str(page), headers = user_agent)
            soup = BeautifulSoup(r.text)
            for item in reversed(soup.find_all('div', class_='list_item article_item')):
                soup2 = BeautifulSoup(item.prettify())
                div_title = soup2.find('div', class_='article_title')
                link = "http://blog.csdn.net" + div_title.a['href']
                div_description = soup2.find('div', class_='article_description')
                div_message = soup2.find('div', class_='article_manage')
                if (div_title.text.strip().startswith('[') == False):
                    print div_title.text.strip() 
                    print div_description.text.strip()
                    soup3 = BeautifulSoup(div_message.prettify())
                    link_postdate = soup3.find('span', class_='link_postdate')
                    link_view = soup3.find('span', class_='link_view')
                    link_comments = soup3.find('span', class_='link_comments')

                    date = link_postdate.text.strip()
                    view = link_view.text.strip()[link_view.text.strip().find('(') : ]
                    comments = link_comments.text.strip()[link_comments.text.strip().find('(') : ]
                    self.count += 1
                    desc = "description:" + div_description.text.strip() + ' ' + link_postdate.text.strip() + ' ' + view + ' ' + comments
                    if len(keys) > 0:
                        if self.containKey(keys, div_title.text):
                            parentID = rID + "-" + str(self.count)
                        elif parentID != '':
                            desc = "parentid:" + parentID  + " "  + desc

                    self.write_db(f, rID + "-" + str(self.count), div_title.text.strip(), link, desc)

    def containKey(self, keys, text):
        for key in keys:
            if text.find(key) != -1:
                return True
        return False

start = CSDNBlogSpider()
start.doWork()

