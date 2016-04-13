#!/usr/bin/env python

#author: wowdd1
#mail: developergf@gmail.com
#data: 2014.12.07

from spider import *

class GoogleCodeSpider(Spider):
    use_proxy = False
    base_url = "https://code.google.com/hosting/"
    def __init__(self):
        Spider.__init__(self)
        self.school = "googlecode"

    def requestData(self, url):
        if self.use_proxy == True:
            return self.requestWithProxy(url)
        else:
            return requests.get(url)

    def processOnePageData(self, list_all, url):
        print 'processing ' + " " + url
        r = self.requestData(url)
        soup = BeautifulSoup(r.text)
        for td in soup.find_all("td"):
            star_index = td.prettify().find("Stars:")
            if star_index != -1 and star_index != None:
                star_num_1 = td.prettify().find('>', star_index)
                star_num_2 = td.prettify().find('<', star_num_1)
                stars = str(td.prettify()[star_num_1 + 1 : star_num_2]).strip()
                while (len(stars) > len(list_all)):
                    list_all.append([])
                    #print "resize list ----> stars: " + stars + " list_all len: " + str(len(list_all)) 
                list_all[len(stars) - 1].append(stars + " " + str(td.a.text).strip() + " " + "https://code.google.com" + str(td.a['href']).strip())
        return soup

    def processGoogleCodeData(self, lable, stars):
        
        url = self.base_url + "search?num=100&q=label%3A" + lable + "&filter=0&mode=&start=0"

        print 'geting ' + lable + " data"

        list_all = []
        soup = self.processOnePageData(list_all, url)
     
        for a in soup.find_all("a"):
            if str(a['href']).startswith("search?num=100") == True and str(a.text).startswith('Next') == False:
                self.processOnePageData(list_all, self.base_url + str(a['href']))

        for lt in list_all:
            lt.sort(reverse=True)
       
        file_name = self.get_file_name("eecs/projects/googlecode/" + lable, self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp") 
        self.count = 0
        pre = ""
        exit = False

        for i in range(len(list_all) - 1, -1, -1):
            if exit == True:
                break
            for item in list_all[i]:
                if item[0 : 15] == pre[0 : 15]:
                    pre = item
                    continue
                pre = item
                
                self.count += 1
                if int(item[0 : item.find(' ')].strip()) < stars:
                    exit = True
                    break
                title = item[item.find(' ') : item.find("- ")].strip()
                remark = item[item.find("- ") + 1 : item.find('http')].strip()
                self.write_db(f, "gc-" + item[0 : item.find(' ')].strip(), title, item[item.find('http') : ], remark)
                print item

        self.close_db(f)
        if self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"


    def doWork(self):
        print "tip: if you are in china, update google code info need you run goagent propy on local, then make use_proxy is True in this file,  or you can modify hosts file(see https://github.com/txthinking/google-hosts#%E4%BD%BF%E7%94%A8%E5%BD%93%E5%89%8D%E7%9A%84hosts)"
        r = self.requestData(self.base_url)
        soup = BeautifulSoup(r.text)
        for a in soup.find_all("a"):
            if str(a['href']).find('search') != -1:
                self.processGoogleCodeData(a.text, 100)




start = GoogleCodeSpider()
start.doWork()
