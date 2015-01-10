#! /usr/bin/env python


from spider import *

#SCImago Journal Rank
class SJRSpider(Spider):

    area_dict = {}
    category_dict = {}
    country_dict = {}
    year_dict = {}
    order_dict = {}

    def __init__(self):
        Spider.__init__(self)
        self.school = "sjr"


    def initOptionDict(self, selectId, optionDict, html):
        soup = BeautifulSoup(html)
        for option in soup.find("select", id="selectId").children:
            if str(option).strip() == "" or str(option).find("value") == -1:
                continue
            key, value = self.getKeyValue(str(option))
            optionDict[key] = value
            #print key + " " + value   

    def processData(self, area, category, country, year, order):
        url = "http://www.scimagojr.com/journalrank.php?area=" + area + "&category=" + category + "&country=" + country + "&year=" + year + "&order=" + order + "&min=0&min_type=cd"
        print "processing " + url
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        file_name = self.get_file_name("eecs/sjr/" + self.category_dict[category], self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0

        for a in soup.find_all("a", title="view journal details"):
            self.count += 1
            url = "http://www.scimagojr.com/" + a["href"]
            print str(self.count) + " " + a.text + " " + url
            self.write_db(f, "sjr-" + category + "-" + str(self.count), a.text, url)
        
        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def doWork(self):
        #r = requests.get("http://www.scimagojr.com/journalrank.php")
        r = requests.get("http://www.scimagojr.com/journalrank.php?area=1700&category=0&country=all&year=2013&order=sjr&min=0&min_type=cd")       
        self.initOptionDict("area", self.area_dict, r.text)  
        self.initOptionDict("category", self.category_dict, r.text)  
        self.initOptionDict("country", self.country_dict, r.text)  
        self.initOptionDict("year", self.year_dict, r.text)  
        self.initOptionDict("order", self.order_dict, r.text)  
        
        for area in self.area_dict.keys():
            if area == "1700":
                for category in self.category_dict.keys():
                    if category.lower().find("all") == -1:
                        self.processData(area, category, "all", "2013", self.order_dict.keys()[0])

start = SJRSpider()
start.doWork()
